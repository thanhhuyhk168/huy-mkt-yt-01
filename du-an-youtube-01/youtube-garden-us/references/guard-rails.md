# Guard Rails — US Gardening Channel

Áp dụng ở MỌI phase. Không bao giờ bỏ qua.

---

## 1. Narrator Integrity

- Narrator = **knowledgeable gardening educator** đọc tài liệu công khai
- KHÔNG đóng vai nhân chứng/insider/chuyên gia cá nhân
- KHÔNG dùng "I planted", "my garden", "I tested" — dùng "gardeners report", "trials show", "practitioners have found"
- KHÔNG bịa trải nghiệm cá nhân để tạo authority

## 2. Anti-Hallucination

- Thiếu data → ghi `[NEED DATA: mô tả cần gì]`, KHÔNG tự điền
- Tên cá nhân không có URL nguồn → ẩn danh hóa
- Số liệu phải trỏ về research-brief.md — không tự nghĩ ra con số

## 3. YMYL Safety (Your Money Your Life)

- Claims về sức khỏe/an toàn pets/trẻ em → LUÔN hedge: "according to [source]", "many gardeners report"
- Không dùng: "cures", "eliminates 100%", "guaranteed", "proven to"
- Dùng thay: "can help manage", "research suggests", "effective approach for many"

## 4. AD-FRIENDLY Compliance

Chạy `compliance_scan.py` sau mỗi session viết. Không nộp script khi HARD-FAIL.

- Cat A (safety claims) → hedge hoặc xóa
- Cat B (absolute claims) → soften
- Cat C (conspiracy framing) → xóa hoàn toàn
- Cat D (clickbait shock) → rewrite
- Cat E (AI language patterns) → rewrite tự nhiên hơn
- Cat F (false personal authority) → chuyển sang narrator voice

## 5. Kane Anti-Pattern

Chạy `mkt-kane-anti-pattern-auditor` trước khi finalize. Tránh 4 downward drivers:
- Over-branding (logo/intro dài > 3 giây)
- Over-production (quá nhiều effects không cần thiết)
- Stock imagery (ảnh generic không liên quan)
- Standardized language (template-sounding, không có voice riêng)

## 6. Audience Context — US Gardening

- Đơn vị: Imperial (feet, inches, °F, gallons, lbs)
- Tham chiếu: Home Depot, Lowe's, USDA zones, EPA
- Tone: Conversational, warm, practical — KHÔNG academic
- Sentence length: Max 20 words/câu cho script
- Reading level: Grade 6-8 (dễ nghe khi đọc to)
