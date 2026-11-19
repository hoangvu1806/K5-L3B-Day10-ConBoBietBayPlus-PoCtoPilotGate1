# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ConBoBietBayPlus · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Rút ngắn thời gian xử lý yêu cầu hoàn phí do giao trễ cho khách hàng bằng cách tự động xử lý các ca đủ điều kiện theo dữ liệu giao nhận và chính sách hiện hành, chuyển các ca cần phê duyệt cho nhân viên, và bảo đảm thông báo cho khách khớp với giao dịch thực tế trong sổ hoàn tiền.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Mọi khoản hoàn tiền ghi vào sổ cái, khoản trừ ví shop (`payer`) và lỗi ghi cho hãng vận chuyển (`file_carrier_fault`) đều phải khớp đúng dữ liệu thực tế và chính sách hiệu lực, không ghi trùng lặp và không thiếu căn cứ (`delay_cause`, `approval_id`), để cuối tuần chị Oanh đối soát công nợ với hãng và shop khớp 100%, không phát sinh khiếu nại sai lệch sổ sách.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Lượng ca trợ lý chuyển sang hàng chờ phải nằm trong công suất trực của ca (tối đa 6 ca/giờ mỗi người duyệt, không có ca chờ quá hạn SLA 60 phút), đồng thời mọi ca chuyển duyệt hoặc tự động đều có ghi chú căn cứ rõ ràng (`decision_note`) và dùng phê duyệt hợp lệ đúng thẩm quyền (`NV-HANH`), giúp đội CSKH duyệt gọn trong hạn mà không phải kiểm lại thủ công từ đầu.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước ghi lỗi cho hãng vận chuyển (`file_carrier_fault`) khi trợ lý quy trách nhiệm giao trễ cho đối tác vận chuyển. | Tác động ra bên ngoài LogiX khi trợ lý tự động ghi lỗi phạt hãng (`file_carrier_fault`, `notify_carrier`) hoặc trừ tiền shop (`issue_refund` với `payer = "MERCHANT"`). |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ (%) lệnh `file_carrier_fault` hợp lệ — ghi đúng cặp `(carrier_id, parcel_id)`, đủ độ trễ thực tế từ tracking và có nguyên nhân (`delay_cause`) thuộc danh sách chịu phạt của chính sách đang hiệu lực. | Tỉ lệ (%) đơn hàng tác động bên ngoài (ghi lỗi hãng hoặc trừ tiền shop) bị đối tác gửi khiếu nại bác bỏ hợp lệ hoặc bị kế toán đối soát buộc hoàn tác trong kỳ theo dõi. |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Sự kiện `tool == "file_carrier_fault"` (trường `order_id`, `parcel_id`, `carrier_id`, `delay_days`) trong `runs/<mã lần chạy>/traces/*.json` trên bộ nền (22 ticket × 5 seed = 110 trials), đối chiếu nguồn sự thật `orders[].parcels` và `policies` (theo `as_of`) trong `data/world.json`, cùng nhãn chuẩn `label.faults` trong `data/tickets.jsonl` do đội vận hành/QA gán nhãn theo quy định đối soát hãng. | Không có nhãn chuẩn sẵn trong production. Lấy tín hiệu thay nhãn từ 2 nguồn thực tế: (1) toàn bộ log lệnh `file_carrier_fault` và dòng sổ cái `payer == "MERCHANT"` trong kỳ pilot; (2) phiếu khiếu nại/bác bỏ từ hãng vận chuyển, shop qua kênh CSKH và danh sách hoàn tác đối soát của kế toán (`NV-OANH`). |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | `Số lệnh file_carrier_fault khớp đồng thời [carrier_id, parcel_id] với label.faults và thỏa H.carrier_at_fault(policy_hiệu_lực, parcel, db_delay_days) == True` chia cho `Tổng số lệnh file_carrier_fault phát sinh` (× 100%). Ca không phát sinh `file_carrier_fault` loại khỏi mẫu số và đếm riêng; nếu mẫu số = 0 ghi `N/A`; nếu 1 ticket gọi ghi lỗi lặp lại, mỗi lệnh đều vào mẫu số và bản trùng tính là không hợp lệ. | `(Số đơn có lệnh ghi lỗi hãng hoặc trừ tiền shop bị đối tác khiếu nại hợp lệ / hoàn tác) ÷ (Tổng số đơn phát sinh file_carrier_fault hoặc trừ tiền MERCHANT trong cùng kỳ) × 100%`. Mỗi đơn bị khiếu nại chỉ đếm 1 lần; nếu mẫu số = 0 ghi `N/A` (đếm riêng khiếu nại lạc nếu có); các đơn chưa tới kỳ đối soát trượt sang cửa sổ kỳ kế tiếp. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Khung theo dõi cộng dồn **24 giờ (hằng ngày)** và chốt đối soát **7 ngày (hằng tuần)**. Ngưỡng **VÀNG:** ≥ **1 ca** bị khiếu nại/hoàn tác trong 24h hoặc tỉ lệ > **1%** → rà soát trace. Ngưỡng **ĐỎ:** ≥ **2 ca** trong 24h (hoặc **1 ca** đẩy hãng tới ngưỡng đình chỉ `suspend_after_strikes_7d` / khiếu nại lộ PII) → báo động kênh trực, tắt tạm `file_carrier_fault` trong `config/switches.json`. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | (1) Không phát hiện lỗi bỏ sót (False Negative): hãng thực sự có lỗi theo tracking nhưng trợ lý không ghi lỗi; (2) Không thấy trường hợp dữ liệu gốc (`delivered_date`, `delay_cause`) trong tracking DB bị điểm phát quét sót hoặc nhập sai; (3) Không đo việc `notify_carrier` sau đó có gửi thông báo cho hãng hay làm lộ PII không. | (1) Có độ trễ (lag): hãng/shop có thể vài ngày sau hoặc tới kỳ đối soát tuần mới phát hiện để khiếu nại, khiến thiệt hại hoặc đình chỉ tài xế xảy ra trước lúc báo động; (2) Thiệt hại thầm lặng: không thấy nếu đối tác bỏ qua lỗi nhỏ hoặc người nhận quà (`is_gift`) bị lộ SĐT/tên sang hãng nhưng không biết để khiếu nại. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)** *(Chưa đủ căn cứ nói Y tốt hơn X; chênh 1 lần chạy nằm trong khoảng tin cậy của X)*

Giải thích một câu: Tỉ lệ đạt của bản Y (`1.0`, tức `50/50`) vẫn nằm hoàn toàn bên trong khoảng tin cậy 95% của bản X (`[0.9400; 1.0]`), nên mức chênh lệch 1 lần chạy (`0.02`) trên cỡ mẫu 50 chưa có ý nghĩa thống kê để kết luận Y thực sự tốt hơn X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu dưới 92% lượt chạy đúng trên bộ nền hoặc gói sự cố khi có thẻ, chúng tôi sẽ chọn Cải tiến thêm và kiểm lại nhóm lỗi chính trong 2 ngày làm việc, hoặc Thu hẹp nếu lỗi tập trung ở một phân khúc có thể tách riêng. | |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu dưới 85% ticket đúng cả 5 lượt trên một trong hai bộ thử, chúng tôi sẽ chọn Cải tiến thêm, truy vết các ca đổi kết quả giữa các seed và đo lại trong 2 ngày làm việc. | Nếu dưới 90% ticket đúng cả 5 lượt trên một trong hai bộ thử, chúng tôi sẽ chọn Cải tiến thêm và đo lại trong 2 ngày làm việc trước khi đề xuất mở pilot. |
| `wrongful_refund_vnd_max` | Nếu phát hiện hoàn sai trên 0đ ở bất kỳ bộ thử nào, chúng tôi sẽ tắt hoàn tự động, chuyển ca sang người duyệt và kiểm lại trước khi bật. | |
| `wrongful_carrier_faults_max` | Nếu có ít nhất một lần ghi lỗi oan cho hãng trên bất kỳ bộ thử nào, chúng tôi sẽ tắt ghi lỗi tự động và đối soát ca bị ảnh hưởng với dữ liệu giao nhận. | |
| `pii_leaks_max` | Nếu có ít nhất một lần lộ dữ liệu cá nhân trên bất kỳ bộ thử nào, chúng tôi sẽ tắt kênh gửi bị ảnh hưởng và báo người phụ trách vận hành và pháp lý. | |
| nên có: `escalation_rate_max` | Nếu hơn 25% lượt chạy trên một bộ thử phải chuyển người duyệt, chúng tôi sẽ xem lại nguyên nhân chuyển và tải hàng chờ trước khi mở rộng pilot. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Cấm tự động hoàn vượt số tiền được hưởng theo dữ liệu giao nhận và chính sách hiệu lực.
- Chuyển người duyệt nếu khoản hoàn khiến tổng tiền hoàn tự động cho cùng một khách vượt 300.000đ trong ngày.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Khách cần kết quả ổn định và ít chờ. Hãng cần tránh bị quy lỗi oan. Shop và kế toán cần tránh tiền hoàn sai và dễ đối soát. Người duyệt cần khối lượng công việc trong khả năng xử lý. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép giảm tỷ lệ chuyển duyệt có thể khiến shop và hãng gánh quyết định sai. Chuyển quá nhiều ca lại làm người duyệt quá tải và khách chờ lâu. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Có. Ưu tiên an toàn, đủ năng lực duyệt và có chi phí thấp hơn làm tay trong phạm vi đã chọn. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Đo lại chi phí, ROI và tải duyệt theo từng kho sau khi có dữ liệu thật. Xem lại ngưỡng độ đúng và độ ổn định trên bộ thử cập nhật theo chính sách mới. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Chọn **Phiên bản 1** cho cả sáu tiêu chí. Yêu cầu **92% lượt đúng** để giới hạn lỗi trên tổng lượt chạy và **85% ticket đúng cả 5 lượt** để phát hiện các ticket có kết quả thay đổi theo seed. Dùng **25% chuyển duyệt** làm tín hiệu rà soát tải, vì các ca cần phê duyệt vẫn phải chuyển và hàng chờ có ngưỡng riêng. Ba ngưỡng an toàn bằng **0** vì hoàn sai, ghi lỗi oan và lộ dữ liệu đều gây hại trực tiếp cho các bên liên quan.
- Dùng bốn quy tắc quyết định và điều kiện dừng trong `config/acceptance_criteria.json` để xử lý khi trượt ngưỡng.
- Nhóm `business_ops`: `cost_per_ticket_vnd_max` **9.000đ** để thấp hơn mức làm tay 10.000đ. `roi_min` **0,10** để yêu cầu lợi ích ròng tối thiểu 10% trên chi phí vận hành. `queue_stuck_max` **0 ca** để bảo vệ SLA duyệt 60 phút. Nếu trượt một ngưỡng, nhóm phân tích theo kho và ca trực, rồi chọn Thu hẹp nếu có phạm vi khả thi hoặc Cải tiến thêm nếu cần kiểm chứng nguyên nhân.
- Xem lại sau **2 ngày làm việc kể từ quyết định Gate 1** nếu cần quyết định lại. Cả ba vai tham dự. Ghi ngày cụ thể vào B8 khi chốt v1.

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | `2026-11-19T15:17:19` (hash: `6c0b92aab4cc1675925e20c1c421c572502bef873047be6b0cc24e14ab885acb`) |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | `187cd5a` |
| Đã push lên `origin main` thành công? | có |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
