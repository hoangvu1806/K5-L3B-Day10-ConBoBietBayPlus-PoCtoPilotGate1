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

- Vai: **Kỹ sư cổng** (`Gate Engineer`).
- Phụ trách chính: Câu 1.3 (Phiếu A · mục `A2` cột Offline metric); ký niêm phong tiêu chí (`python -m lab10.criteria sign`); Câu 2.1–2.2 (`lab10.eval` mốc `base`, `lab10.gate`, dò `lab10.trace` và điền bảng soát lỗi `T-002@55` ở Phiếu B mục `B0`–`B2`); Câu 2.5–2.8 (Pre-mortem lăng kính Kỹ thuật ở `B6`, thiết kế & cài đặt 3 cổng hệ thống trong `lab10/guards.py` ở `B7.1`, hai bước tránh rò rỉ dữ liệu ở `B7.2`, behavioral test với 2 ticket hiểm `--adhoc` ở `B7.3`); chốt cổng vòng 1 (`python -m lab10.checkpoint`, mốc `prepared`); nhận thẻ sự cố `S2` từ repo thẻ, chạy `lab10.grade --incident S2` mốc `prepared` (Câu 3.0 · `C0`, `C1`); dò trace sự cố `S2` và lập bảng soát lỗi 3 nhánh ở `C2` (Câu 3.1); hoàn thiện bảng sửa `C7` (Câu 3.5); thiết kế và cài đặt 3 chỉ số theo dõi mới trong `lab10/monitors.py` và điền mục `C8` (Câu 3.6); chạy kiểm tra toàn vẹn `lab10.grade` và gom gói bài nộp `lab10.check_submission --collect`.

### Đóng góp cụ thể

- **Phiếu A (`templates/form-a-criteria.md`) & Ký tiêu chí:** Thiết kế Offline metric cho bước ghi lỗi hãng vận chuyển (`file_carrier_fault`) ở Câu 1.3 (công thức tỉ lệ lệnh ghi lỗi hợp lệ khớp `label.faults` và `H.carrier_at_fault`, cách xử lý mẫu số 0/lệnh trùng và 3 điểm mù); hoàn thiện giải thích khoảng tin cậy 95% ở Câu 1.5 (`A3`); thực hiện ký số `config/acceptance_criteria.json` (hash `6c0b92aa`) và điền mục `A5` trước lần chạy đánh giá đầu tiên.
- **Phiếu B (`templates/form-b-evaluation-gates.md`) & Cổng vòng 1 (`lab10/guards.py`):**
  - Chạy và phân tích mốc `base` (`R-base-before-20261119-151903-bde05c`), chỉ ra phân khúc xấu nhất (kho `HCM` pass `0.96`, hãng `VNX` pass `0.9714`, nhóm `?` chi phí `10.359đ > làm tay`); dò trace `T-002@55` bóc tách 2 lỗi chìm do `model_override` (`B1`, `B2`).
  - Cài đặt 3 cổng phòng ngừa tổng quát trong `lab10/guards.py`: (1) `pre_guard` ghim chính sách hiệu lực theo `ctx.as_of` bằng `H.effective_policy`; (2) `write_gate("issue_refund")` chặn hoàn trùng/retry 429, đối chiếu `H.entitlement_vnd` từ `db_delay_days`, ép `payer = "LOGIX"`, kiểm tra phê duyệt hợp lệ (`_find_valid_approval`) và trần hoàn tự động `300.000đ/khách/ngày` + ngân sách ngày; (3) `write_gate("file_carrier_fault", "notify_carrier")` sửa đúng kiện bị trễ trên đơn nhiều kiện (`_select_parcel`), kiểm tra `H.carrier_at_fault`, trần strike/ngày và lọc sạch PII khỏi bản tin gửi hãng (`B7.1`).
  - Viết 2 bước chống rò rỉ dữ liệu (`B7.2`), thiết kế behavioral test bất biến nguồn sự thật & quyền riêng tư với 2 ticket hiểm `--adhoc` trên đơn `O-1002` và đơn quà tặng `O-1026` (`B7.3`), và chốt `lab10.checkpoint` (hash `6e487aab`).
- **Phiếu C (`templates/form-c-incident.md`) & Chỉ số theo dõi (`lab10/monitors.py`) cho thẻ `S2`:**
  - Kéo gói sự cố `incidents/S2`, chạy `grade` mốc `prepared` chứng minh cổng vòng 1 đã đỡ được 100% sự cố `S2` ngay từ đầu (`pass_rate` từ `0.4667` lên `1.0`, cứu `32.750.000đ` tiền shop bị trừ oan).
  - Dò trace `S2-01@11`, `S2-04@11`, `S2-20@11`, `S2-43@11` để hoàn thiện bảng soát lỗi 3 nhánh (`C2`) và bảng sửa (`C7`).
  - Cài đặt 3 hàm monitor mới không dùng nhãn trong `lab10/monitors.py` (`directive_or_merchant_payer_rate`, `note_injection_rate`, `customer_daily_auto_cap_rate`) đều sáng đèn trên `S2` (`0.4667`, `0.1333`, `0.1333` so với `0.0` trên bộ nền) và hoàn thiện mục `C8`.
- *(Có sử dụng trợ lý AI để hỗ trợ đọc hiểu luồng codebase `lab10/`, kiểm tra chuẩn hóa line-ending LF cho `MANIFEST.json` trên Windows, gợi ý cấu trúc hàm trong `guards.py`/`monitors.py` và rà soát định dạng bảng Markdown trong các phiếu.)*

### Bằng chứng

- **Mã commit trên `main` / branch `feat/gate-eng-nguyen`:** `77a7ddf` (Câu 1.3 Offline metric), `187cd5a` (`Sign acceptance criteria`, hash `6c0b92aa`), `c9ab34d` (Phiếu A mục `A3`, `A5`), `63a0d19` (Phiếu B mục `B0`–`B2`), `31b1d8c` & `7226f97` (PR #3 `lab10/guards.py` và `B6`, `B7.1`–`B7.3`), `f567a9d` (chốt cổng vòng 1 `6e487aab` & quyết định v1), `b61f29f` (Nhận thẻ `S2`), `16815a1` & `8b99e2c` (`lab10/monitors.py` và Phiếu C mục `C0`, `C1`, `C2`, `C7`, `C8`).
- **Mã lần chạy (`runs/<run_id>`):**
  - Vòng 1: `R-base-before-20261119-151903-bde05c` (baseline), `R-base-after-20261119-152321-f4f789` (thử cổng vòng 1), `R-base-prepared-20261119-155505-c1d1c4` (mốc `prepared` đã chốt).
  - Vòng 2 (Thẻ `S2`): `R-S2-grade-20261119-161028-c1d1c4` (kiểm tra mốc `prepared` trước khi sửa), `R-S2-after-20261119-161500-8e0d5f`, `R-base-after-20261119-161501-8e0d5f`, `R-S2-grade-20261119-161501-8e0d5f` (`PASS-VISIBLE`, 5/5 mục kiểm đạt `✅`).
- **Dòng trong phiếu:** Phiếu A mục `A2` (cột Offline), `A3`, `A5`; Phiếu B mục `B0`, `B1`, `B2`, `B6` (dòng 1 & 5), `B7.1`–`B7.3`, `B8`; Phiếu C mục `C0`, `C1`, `C2`, `C7`, `C8`.

### Exit ticket

- **Một điều học được:** Khi đưa một Agent có quyền ghi sổ cái từ PoC lên Pilot, mọi văn bản đi vào LLM (kể cả trường có vẻ nội bộ như `order.checkout_note` trong thẻ `S2`) đều phải bị coi là dữ liệu không đáng tin (untrusted data); chỉ những cổng kiểm tra tất định nằm ngoài model (`write_gate` đối chiếu trực tiếp Source of Truth và kiểm tra trạng thái tích lũy như trần `300.000đ/khách/ngày`) mới thực sự ngăn (prevent) được thiệt hại cho bên thứ ba, đồng thời phải đi kèm các chỉ số telemetry không nhãn (`monitors.py`) để phát hiện sớm hành vi tấn công dù cổng chặn đã đỡ được.
- **Một điều còn chưa chắc:** Trên bộ dữ liệu mock, các hàm trong `guards.py` đối chiếu trực tiếp với `world.json` trong bộ nhớ nên độ trễ bằng 0 và dữ liệu tracking luôn có sẵn; khi ra Pilot thật, nếu API của hệ thống Tracking DB hoặc hệ thống Sổ cái bị trễ/timeout hoặc cập nhật bất đồng bộ giữa các microservice, cổng `write_gate` sẽ cần chính sách fallback/circuit-breaker như thế nào để vừa không hoàn tiền trùng vừa không làm nghẽn hàng chờ CSKH.

## TranXuanLoc-2A202603951

### Phần việc phụ trách

- **Sản phẩm và kinh doanh.** Chủ trì mục tiêu hệ thống và tiêu chí nghiệm thu (A1 câu 1.1, A4), bản đồ dữ liệu và phân tích drift (B3), phần kinh doanh của pre-mortem (B6) và cổng kinh doanh (B7.4). Đối chiếu số liệu cho v1 (B8) và viết quyết định v2 (C12), cùng quy tắc đối soát (C5 câu 3.2) và đánh giá cổng kinh doanh sau sự cố S2 (C7).

### Đóng góp cụ thể

- Nối mục tiêu rút ngắn thời gian xử lý hoàn phí với PRD v1.1 và eval card Lab 9. Soạn ngưỡng trước khi nhóm chạy đánh giá, gồm 92% lượt đúng, 85% ticket đúng cả năm lượt, ba ngưỡng an toàn bằng 0, chi phí tối đa 9.000đ/ticket, ROI tối thiểu 0,10 và 0 ca ùn. Viết điều kiện dừng và quy tắc cho bốn quyết định trong `config/acceptance_criteria.json`.
- Lập bản đồ nguồn dữ liệu và phân tích thay đổi chính sách `REFUND-v4` trong B3. Đặt trần hoàn tự động 2.000.000đ/ngày, ngân sách tiền máy 1.500đ/ticket và sàn ROI 0,10 trong `config/operating_gates.json`. Giữ đủ phạm vi bộ thử để so chi phí theo kho và dùng mốc `prepared` để đối chiếu các ngưỡng cho v1.
- Viết yêu cầu mọi khoản hoàn phí giao trễ phải do LogiX chịu, rồi kiểm chứng bằng sổ cái và `merchant_debit_vnd`. Ở C7 và C12, dùng kết quả S2 để giải thích việc giữ các cổng kinh doanh và quyết định **Tiếp tục**. Mốc `after` đạt 75/75 lượt, 0đ trừ shop, 5.273đ/ticket, ROI 0,90 và 0 ca ùn.
- Dùng trợ lý AI để đọc repo, đối chiếu phiếu với cấu hình và báo cáo, hỗ trợ soạn và rà câu chữ ở các mục phụ trách.

### Bằng chứng

- `15a782a`, `fd4a348` (Phiếu A và bộ tiêu chí), `3b11a47` (B3), `552b3c5` (B6, B7.4 và cấu hình kinh doanh), `90bd53f` (C5 câu 3.2 và C7), `4be5ca4` (C12).
- `R-base-after-20261119-154319-e820f4` (kiểm cổng kinh doanh B7.4) và `R-S2-grade-20261119-165439-8e0d5f` (bằng chứng cho quyết định v2 trong C12).

### Exit ticket

- **Điều học được.** Chi phí pilot phải tính cả tiền máy, công duyệt và phí trực. Kết quả đúng vẫn cần đối chiếu với trải nghiệm của khách và chi phí từng kho trước khi mở rộng.
- **Điều còn chưa chắc.** Nếu nhiều khoản hoàn của cùng một khách đến đồng thời, sổ cái có cập nhật kịp để giữ trần 300.000đ/khách/ngày và hàng chờ vẫn trong SLA 60 phút hay không.
