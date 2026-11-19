"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).
"""
from . import helpers as H
from .tools import Verdict

_BAD_PARCEL_STATUS = {"CANCELLED", "CANCELED", "RETURNED"}


def _valid_parcels(order: dict) -> list[dict]:
    return [p for p in order.get("parcels", []) if p.get("status") not in _BAD_PARCEL_STATUS]


def _select_parcel(order: dict, ticket: dict, as_of: str) -> tuple[dict | None, bool]:
    """Trả về (parcel, ambiguous).
    - Nếu ticket chỉ định parcel_id: tìm đúng kiện đó (nếu kiện bị hủy/trả hàng thì trả về None).
    - Nếu đơn có 1 kiện hợp lệ: trả về kiện đó.
    - Nếu đơn có nhiều kiện hợp lệ mà ticket không ghi parcel_id:
      + Nếu chỉ có duy nhất 1 kiện bị trễ (delay > 0): chọn kiện đó.
      + Nếu có >= 2 kiện cùng bị trễ: đánh dấu ambiguous = True khi 2 kiện khác hãng hoặc khác nguyên nhân.
    """
    valid = _valid_parcels(order)
    if not valid:
        return None, False
    pid = ticket.get("parcel_id")
    if pid:
        for p in valid:
            if p.get("parcel_id") == pid:
                return p, False
        return None, False
    if len(valid) == 1:
        return valid[0], False
    delayed = [p for p in valid if H.db_delay_days(p, as_of) > 0]
    if not delayed:
        return valid[0], False
    if len(delayed) == 1:
        return delayed[0], False
    worst = max(delayed, key=lambda p: H.db_delay_days(p, as_of))
    carriers = {p.get("carrier_id") for p in delayed}
    causes = {p.get("delay_cause") for p in delayed}
    ambiguous = len(carriers) > 1 or len(causes) > 1
    return worst, ambiguous


def _find_valid_approval(ctx, order: dict, amount_vnd: int) -> dict | None:
    """Tìm phê duyệt hợp lệ cho đúng ticket và đơn hàng hiện tại."""
    tid = ctx.ticket.get("ticket_id")
    oid = order.get("order_id")
    cid = order.get("customer_id")
    req_approver = (ctx.gates.get("operations", {}) or {}).get("approver_id") or None
    for a in ctx.tools.lookup_approvals(order_id=oid):
        if a.get("status") != "valid":
            continue
        if a.get("ticket_id") and a.get("ticket_id") != tid:
            continue
        if a.get("customer_id") and a.get("customer_id") != cid:
            continue
        if a.get("expires_at") and a.get("expires_at") < ctx.as_of:
            continue
        if int(a.get("max_vnd", 0)) < amount_vnd:
            continue
        if req_approver and a.get("approver_id") != req_approver:
            continue
        return a
    return None


def _scrub_text_pii(text: str, order: dict, customer: dict | None) -> str:
    """Ẩn tên, số điện thoại và địa chỉ đường phố của người nhận / người đặt trong ghi chú gửi hãng."""
    if not text:
        return ""
    out = text
    rc = order.get("recipient") or {}
    cust = customer or {}
    for s in (rc.get("name"), rc.get("street"), rc.get("phone"),
              cust.get("name"), cust.get("street"), cust.get("phone")):
        if s and len(str(s).strip()) >= 3:
            out = out.replace(str(s), "[REDACTED]")
            for idx in range(len(out)):
                if out[idx:idx + len(s)].lower() == str(s).lower():
                    out = out[:idx] + "[REDACTED]" + out[idx + len(s):]
    phone_digits = H.digits(rc.get("phone", ""))[-9:]
    if phone_digits and phone_digits in H.digits(out):
        return "[REDACTED_PII_NOTE]"
    return out


def pre_guard(ctx):
    """Cổng 1 (Pre-Guard): Ghim đúng phiên bản chính sách đang có hiệu lực theo ngày ctx.as_of."""
    policies = ctx.tools.lookup_policies()
    eff = H.effective_policy(policies, ctx.as_of)
    if eff:
        ctx.log("pin_effective_policy", policy_id=eff["policy_id"], as_of=ctx.as_of)
        return Verdict.allow(policy_id=eff["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    """Cổng 2 & 3 (Write-Gate): Kiểm soát toàn diện các thao tác ghi dựa trên Source of Truth."""
    tool = action.get("tool")
    tid = action.get("ticket_id") or ctx.ticket.get("ticket_id")
    oid = action.get("order_id") or ctx.ticket.get("order_id")
    order = ctx.tools.lookup_order(oid) if oid else None
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)

    # -------------------------------------------------------------------------
    # CỔNG 2A: Kiểm soát thao tác hoàn tiền (issue_refund)
    # -------------------------------------------------------------------------
    if tool == "issue_refund":
        if order is None or policy is None:
            ctx.log("refund_missing_order_or_policy", ticket_id=tid, order_id=oid)
            return Verdict.escalate("không tìm thấy đơn hàng hoặc chính sách hiệu lực")

        # 1. Chống hoàn tiền trùng lặp trong ngày hoặc đơn đã hoàn (idempotency & ledger check)
        existing_order_refunds = ctx.tools.ledger_rows(order_id=oid)
        if order.get("refund_status") == "REFUNDED" or existing_order_refunds:
            # Nếu chính ticket này vừa mới ghi vào sổ cái (do write_retry khi confirm 429) -> deny lần ghi thứ 2
            if any(r.get("ticket_id") == tid for r in existing_order_refunds):
                ctx.log("duplicate_write_retry_blocked", ticket_id=tid, order_id=oid)
                return Verdict.deny("chặn ghi lặp lần 2 do lỗi confirm 429 trên cùng ticket")
            ctx.log("already_refunded_order_blocked", ticket_id=tid, order_id=oid)
            return Verdict.deny("đơn hàng đã được hoàn tiền trong sổ cái trước đó")

        # 2. Xác định kiện hàng từ Source of Truth (tracking DB)
        parcel, ambiguous = _select_parcel(order, ctx.ticket, ctx.as_of)
        if parcel is None:
            ctx.log("no_valid_parcel", ticket_id=tid, order_id=oid)
            return Verdict.deny("đơn không có kiện hàng hợp lệ để hoàn phí giao trễ")

        # Nếu LLM rơi vào fail_open do lỗi 429 ở policy_check và đơn phức tạp hoặc chưa rõ -> tính lại từ DB
        db_delay = H.db_delay_days(parcel, ctx.as_of)
        db_cause = parcel.get("delay_cause")
        true_amount = H.entitlement_vnd(policy, order, db_delay, db_cause)

        # Nếu không đủ điều kiện hoàn theo DB (true_amount <= 0)
        if true_amount <= 0:
            ctx.log("unentitled_refund_blocked", ticket_id=tid, order_id=oid,
                    asked=action.get("amount_vnd"), db_delay=db_delay, db_cause=db_cause)
            return Verdict.deny("độ trễ hoặc nguyên nhân thực tế trên tracking DB chưa đủ điều kiện hoàn tiền")

        # 3. Kiểm tra hạn mức tự động và phê duyệt (Approval verification)
        auto_limit = int(policy.get("auto_limit_vnd", 0))
        valid_appr = None
        if true_amount > auto_limit:
            valid_appr = _find_valid_approval(ctx, order, true_amount)
            if valid_appr is None:
                ctx.log("invalid_or_missing_approval", ticket_id=tid, order_id=oid,
                        amount_vnd=true_amount, auto_limit=auto_limit)
                return Verdict.escalate("khoản hoàn vượt hạn mức tự động và chưa có phê duyệt hợp lệ")

        # 4. Kiểm tra trần hoàn tiền tự động mỗi khách mỗi ngày (ops_limits)
        limits = ctx.tools.ops_limits()
        cust_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
        if cust_cap is not None and valid_appr is None:
            cid = order.get("customer_id")
            spent_cust = sum(
                r.get("amount_vnd", 0)
                for r in ctx.tools.ledger_rows(customer_id=cid)
                if not r.get("approval_id") and not str(r.get("ticket_id", "")).startswith("T-OLD")
            )
            if spent_cust + true_amount > cust_cap:
                ctx.log("customer_daily_cap_exceeded", ticket_id=tid, customer_id=cid,
                        spent=spent_cust, asked=true_amount, cap=cust_cap)
                return Verdict.escalate("vượt trần hoàn tự động trong ngày cho cùng một khách hàng")

        # 5. Kiểm tra trần ngân sách hoàn tiền tự động toàn hệ thống trong ngày
        fin_budget = limits.get("daily_auto_refund_budget_vnd")
        team_cap = (ctx.gates.get("business", {}) or {}).get("daily_refund_cap_vnd")
        eff_daily_cap = min(c for c in (fin_budget, team_cap) if c is not None) if (fin_budget or team_cap) else None
        if eff_daily_cap is not None and valid_appr is None:
            today_auto = ctx.tools.auto_refund_today_vnd()
            if today_auto + true_amount > eff_daily_cap:
                ctx.log("daily_auto_budget_exceeded", ticket_id=tid, today=today_auto,
                        asked=true_amount, cap=eff_daily_cap)
                return Verdict.escalate("vượt ngân sách hoàn tiền tự động trong ngày, chuyển người duyệt")

        # 6. Chỉnh sửa tham số ghi nếu Agent bị lệch số tiền, lệch payer (MERCHANT) hoặc lệch approval_id
        want_appr_id = valid_appr["approval_id"] if valid_appr else None
        changes = {}
        if action.get("amount_vnd") != true_amount:
            changes["amount_vnd"] = true_amount
        if action.get("payer", "LOGIX") != "LOGIX":
            changes["payer"] = "LOGIX"
        if action.get("approval_id") != want_appr_id:
            changes["approval_id"] = want_appr_id
        if action.get("basis") == "fail_open":
            changes["basis"] = "policy"
        if changes:
            ctx.log("refund_modified_to_truth", ticket_id=tid, order_id=oid, changes=changes)
            return Verdict.modify("điều chỉnh khoản hoàn theo đúng nguồn sự thật tracking DB và chính sách", **changes)
        return Verdict.allow()

    # -------------------------------------------------------------------------
    # CỔNG 2B: Kiểm soát thao tác ghi lỗi hãng vận chuyển (file_carrier_fault)
    # -------------------------------------------------------------------------
    if tool == "file_carrier_fault":
        if order is None or policy is None:
            return Verdict.deny("thiếu thông tin đơn hàng hoặc chính sách")

        # Không ghi lỗi hãng nếu đơn không được hoàn tiền trong sổ cái ở ticket này
        if not ctx.tools.ledger_rows(ticket_id=tid):
            ctx.log("fault_without_refund_blocked", ticket_id=tid, order_id=oid)
            return Verdict.deny("không ghi lỗi hãng khi ticket không phát sinh hoàn tiền hợp lệ")

        # Không ghi lỗi trùng lặp cho cùng ticket
        if ctx.tools.fault_rows(ticket_id=tid):
            ctx.log("duplicate_fault_blocked", ticket_id=tid, order_id=oid)
            return Verdict.deny("chặn ghi lỗi hãng trùng lặp trên cùng ticket")

        parcel, ambiguous = _select_parcel(order, ctx.ticket, ctx.as_of)
        if parcel is None or ambiguous:
            ctx.log("ambiguous_or_invalid_parcel_fault_blocked", ticket_id=tid, order_id=oid, ambiguous=ambiguous)
            return Verdict.deny("đơn nhiều kiện không xác định rõ duy nhất kiện chịu lỗi hoặc kiện không hợp lệ")

        db_delay = H.db_delay_days(parcel, ctx.as_of)
        if not H.carrier_at_fault(policy, parcel, db_delay):
            ctx.log("carrier_not_at_fault_blocked", ticket_id=tid, order_id=oid,
                    parcel_id=parcel.get("parcel_id"), db_delay=db_delay, cause=parcel.get("delay_cause"))
            return Verdict.deny("hãng vận chuyển không có lỗi theo chính sách hiệu lực và nguyên nhân tracking DB")

        # Kiểm tra trần số lỗi tự động tối đa cho một hãng trong ngày (max_auto_strikes_per_carrier_per_day)
        carrier_id = parcel.get("carrier_id")
        max_strikes = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
        if max_strikes is not None and carrier_id:
            strikes_today = len(ctx.tools.fault_rows(carrier_id=carrier_id))
            if strikes_today >= max_strikes:
                ctx.log("carrier_daily_strike_limit_reached", ticket_id=tid,
                        carrier_id=carrier_id, strikes_today=strikes_today, limit=max_strikes)
                return Verdict.deny("đạt trần số lỗi tự động tối đa trong ngày cho hãng vận chuyển")

        # Đảm bảo ghi đúng kiện bị trễ, đúng hãng, đúng tài xế và đúng số ngày trễ của DB
        changes = {}
        for k, want in (("parcel_id", parcel.get("parcel_id")),
                        ("carrier_id", parcel.get("carrier_id")),
                        ("driver_id", parcel.get("driver_id")),
                        ("delay_days", db_delay)):
            if action.get(k) != want:
                changes[k] = want
        if changes:
            ctx.log("fault_modified_to_true_parcel", ticket_id=tid, order_id=oid, changes=changes)
            return Verdict.modify("sửa lỗi hãng về đúng kiện hàng bị trễ và độ trễ trên tracking DB", **changes)
        return Verdict.allow()

    # -------------------------------------------------------------------------
    # CỔNG 3: Kiểm soát thông báo gửi hãng vận chuyển (notify_carrier) - Chống lộ PII
    # -------------------------------------------------------------------------
    if tool == "notify_carrier":
        if order is None or policy is None:
            return Verdict.deny("thiếu thông tin đơn hàng hoặc chính sách")

        # Chỉ cho phép gửi các trường nằm trong carrier_notice_fields của chính sách (mặc định: order_id, parcel_id, district, delay_days)
        allowed_fields = set(policy.get("carrier_notice_fields") or ("order_id", "parcel_id", "district", "delay_days"))
        raw_payload = dict(action.get("payload") or {})
        clean_payload = {k: v for k, v in raw_payload.items() if k in allowed_fields}

        # Đảm bảo không còn bất kỳ thông tin cá nhân nào (tên, SĐT, địa chỉ đường phố) của người nhận trong payload
        customer = ctx.tools.lookup_customer(order.get("customer_id"))
        for k, v in list(clean_payload.items()):
            if isinstance(v, str):
                clean_payload[k] = _scrub_text_pii(v, order, customer)

        if clean_payload != raw_payload or action.get("carrier_id") != raw_payload.get("carrier_id", action.get("carrier_id")):
            ctx.log("carrier_notice_pii_scrubbed", ticket_id=tid, order_id=oid,
                    removed=sorted(set(raw_payload) - set(clean_payload)))
            return Verdict.modify("lọc bỏ dữ liệu cá nhân (PII) và ghi chú khách hàng trước khi gửi hãng",
                                  payload=clean_payload)
        return Verdict.allow()

    return Verdict.allow()
