# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `ConBoBietBayPlus`
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-Day10-ConBoBietBayPlus-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S2`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Bùi Đặng Nhật Nguyên | 2A202603937 | Kỹ sư cổng | |
|   2 | Trần Xuân Lộc | 2A202603951 | Sản phẩm và kinh doanh | |
|   3 | Đỗ Hoàng Vũ | 2A202603920 | Vận hành và pháp lý | x |
|   4 | | | | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## DoHoangVu-2A202603920

### Phần việc phụ trách

- Vai: **Vận hành và pháp lý** (Trưởng nhóm).
- Câu 1.2, 1.4 (Phiếu A · mục A1, A2); Câu 2.4, 2.5 (Phiếu B · mục B4 HAZOP vòng 1, B5 Checklist 9 nhóm, B6 Pre-mortem); Câu 2.10 (cổng `operations`, `legal` trong `config/operating_gates.json`, Runbook 1–3 & Giờ cao điểm mục B7.5–B7.6); Câu 3.1 phần riêng `C3.1`, `C4` HAZOP thẻ S2, Câu 3.3 giả định môi trường (`C5`), Câu 3.4 & 3.7 (`C6`, `C9` Fault tree trước/sau sửa, `C10` Risk register, `C11` Checklist & Runbook 4–5); điền `submission/submission.json` và chạy `lab10.check_submission --collect`.

### Đóng góp cụ thể

- Tạo/đồng bộ tài liệu phân công `docs/assignment.md` và hoàn thiện bảng thông tin thành viên trong `TEAM.md` (PR #1, PR #2).
- Phiếu A (`templates/form-a-criteria.md`): viết mục tiêu từ góc nhìn kế toán đối soát (`NV-OANH`) và trưởng ca CSKH (`NV-HANH`) ở Câu 1.2; thiết kế telemetry production đo tác hại bên ngoài không có nhãn (tỉ lệ khiếu nại/hoàn tác từ hãng và shop, ngưỡng Vàng/Đỏ theo 24h/7 ngày) ở Câu 1.4; rà soát chốt `signed_by` trong `config/acceptance_criteria.json` trước khi ký.
- Phiếu B (`templates/form-b-evaluation-gates.md`) & `config/operating_gates.json`: hoàn thiện HAZOP vòng 1 (`B4`), Checklist 9 nhóm có PIC (`B5`), Pre-mortem lăng kính Con người/Vận hành & Pháp lý (`B6`); cấu hình mục `operations` (`pic: NV-TUNG`, `approver_id: NV-HANH`, `reviewers_on_shift: 1`, `max_queue_wait_minutes: 60`, `decision_note: true`, `review_sampling_pct: 10`) và `legal` (`pii_fields_blocked_to_third_party`, `carrier_fault_requires_recorded_cause: true`); viết Runbook 1–3 (`B7.5`) và Giờ cao điểm (`B7.6`) (PR #4, PR #7).
- Phiếu C (`templates/form-c-incident.md`) cho thẻ `S2` & Gom bài nộp: hoàn thiện `C3.1` mức kiểm soát con người, `C4` HAZOP thẻ S2, `C5` Câu 3.3 giả định môi trường, `C6` & `C9` Fault tree trước/sau sửa, `C10` Risk register, `C11` cập nhật Checklist & Runbook 4–5 (PR #8); hoàn thiện `submission/submission.json` và chạy kiểm tra đủ thành phần bài nộp (`check_submission --collect`).
- *(Có sử dụng trợ lý AI để tra cứu cấu trúc codebase, kiểm chứng số liệu mô phỏng, rà soát câu chữ và đối chiếu tính nhất quán giữa các phiếu với config.)*

### Bằng chứng

- Các commit/PR trên `main`: `93b8203` (PR #1 `docs/assignment.md`), `af2ed3a` (PR #2 `TEAM.md`), `7c8b813` (Câu 1.2), `9f41660` (Câu 1.4), `70fd907` (`signed_by`), `f1270d4` (PR #4 `B4`–`B6`), `ea83378` (PR #7 `operating_gates.json` & `B7.5`–`B7.6`), `8978144` & `c971c52` (PR #8 Phiếu C thẻ `S2`).
- Mã lần chạy đối chiếu: `R-S2-grade-20261119-160943-c1d1c4` (`prepared` đỡ 100% gói visible S2), `R-S2-grade-20261119-163344-46fbf4` (`3 visible ✅`, `5 regression ✅`, `6 monitor ✅`, `0` ca ùn, `0` lộ PII, `0` lỗi hãng oan).

### Exit ticket

- **Điều học được:** Cổng bảo vệ cho hệ thống AI không chỉ nằm ở code `guards.py` mà còn nằm ở các con số vận hành và niềm tin con người (`reviewers_on_shift`, `decision_note`, `review_sampling_pct`, `approver_id`) cùng việc tách rạch ròi kênh dữ liệu đầu vào (`ticket.text`, `checkout_note`) khỏi quyền ra lệnh thanh toán/phê duyệt.
- **Điều còn chưa chắc:** Khi chạy pilot thật với lượng đơn lớn và nhiều giao dịch xảy ra đồng thời (concurrent writes), độ trễ đồng bộ giữa các lượt ghi sổ cái có thể làm việc kiểm tra trần `300.000đ/khách/ngày` bị hụt nếu không có khóa/giao dịch nguyên tử (atomic) ở tầng cơ sở dữ liệu — cần đo lại trước Gate 2.

## BuiDangNhatNguyen-2A202603937

### Phần việc phụ trách

- Vai: **Kỹ sư cổng**.
- Câu 1.3 (Phiếu A · mục A2 Offline metric); ký tiêu chí (`lab10.criteria sign`), Câu 2.1–2.2 (`eval` mốc `base`, `trace T-002@55`), Câu 2.5–2.8 (`lab10/guards.py`, tránh rò rỉ dữ liệu, behavioral test `--adhoc`), chốt vòng 1 (`lab10.checkpoint`); nhận thẻ & đo `prepared` (`lab10.grade`), Câu 3.1 trace sự cố (C2), Câu 3.5–3.6 (sửa `lab10/guards.py`, thêm chỉ số mới trong `lab10/monitors.py`, C7–C8).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.

## TranXuanLoc-2A202603951

### Phần việc phụ trách

- Vai: **Sản phẩm và kinh doanh**.
- Câu 1.1, 1.6 (Phiếu A · mục A1, A4, A5) và `config/acceptance_criteria.json`; Câu 2.3 (Bản đồ dữ liệu & drift B3), Câu 2.5 (Pre-mortem lăng kính kinh doanh B6), Câu 2.9 (cổng `business` trong `config/operating_gates.json`, B7.4), Quyết định v1 (B8); Câu 3.2 (Specification C5), Câu 3.5 chỉnh `business` trong `config/operating_gates.json` (C7), Quyết định v2 & 3 dòng bắt buộc (C12).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
