---
name: youtube-garden-us
description: Full pipeline to write a 15-20 min YouTube script for the US gardening channel. Just say "script big idea #2" or "viết kịch bản big idea #3" — Claude auto-reads the big idea, creates the Notion video page, and runs the full pipeline. Uses Brendan Kane framework (Jenga or 30-Day) with compliance QA and optional ES translation. USE WHEN user says "script big idea", "viết kịch bản big idea", "viết script big idea", "chạy pipeline", "script kênh garden", or any variant with a big idea number.
---

# YouTube Garden US — Script Pipeline Orchestrator

Bạn là NGƯỜI ĐIỀU PHỐI, không phải người viết tự do.
Luôn áp dụng `references/guard-rails.md` ở MỌI phase.

---

## Notion Pointers (cố định — không hỏi user)

| Resource | URL |
|----------|-----|
| **Big Ideas page** | https://app.notion.com/p/377d73f564198028a6c8dbd7445d461f |
| **Content Manager DB** | collection://55cd73f5-6419-826b-a3dd-8716e793b758 |
| **Video page template** | https://app.notion.com/p/c54d73f56419822b90bb01e2ef5bb169 |
| **DNA Brand Voice** | https://app.notion.com/p/4fed73f5641983298ab9814692167e81 |
| **SEO Description Prompt** | https://app.notion.com/p/8b8d73f564198243a4df810cf26b0741 |
| **Team system** | https://app.notion.com/p/366d73f5641980bd8789dc418aa01b11 |

---

## Lệnh khởi động

| Lệnh | Hành động |
|------|-----------|
| `"Script big idea #[N]"` | Auto-setup + chạy toàn bộ Phase 0→5 |
| `"Viết kịch bản big idea #[N]"` | Như trên |
| `"Chạy Phase [0-5]"` | Chạy từ phase chỉ định trên page hiện tại |
| `"Chạy từ bước [X]"` | Resume từ điểm cụ thể |
| `"Auto đến Phase [X]"` | Auto chạy đến phase đó, hard gate vẫn dừng |
| `"Tiếp / Confirm"` | Qua gate tiếp theo |
| `"Sửa [phần X]"` | Re-run phần cụ thể |

---

## Routing Table

| Phase | Nội dung | Reference nạp | Script chạy | Notion section |
|-------|----------|---------------|-------------|----------------|
| **0** | Deep Research | research-protocol.md | citation_check.py | Nghiên Cứu > Dữ liệu | 🟢 Auto |
| **1** | Format + Outline | guard-rails.md | — | Dàn Ý + Thông Tin Video | 🟢 Auto |
| **2** | Script viết (Kane) | guard-rails.md | compliance_scan.py + word_budget.py | Kịch Bản Chi Tiết | 🟢 Auto |
| **3** | QA + Audit Loop | guard-rails.md | compliance_scan.py | Ghi chú QA |
| **4** | TTS Clean | — | tts_clean.py | Sub-page Script_Final_voiceAI |
| **5** | ES Translation (optional) | — | — | Sub-page {TITLE}_ES_USHispanic_v1.0 |
| **6** | SEO Description + Pinned Comment | SEO Prompt page | — | Sub-page YouTube SEO Description |

---

## PHASE SETUP — TỰ ĐỘNG (chạy trước Phase 0, không cần user làm gì)

### Bước S0 — Đọc DNA Brand Voice
Dùng Notion MCP đọc trang:
`https://app.notion.com/p/4fed73f5641983298ab9814692167e81`

Lưu vào context: Voice Formula, Speaker Archetype, Signature Phrases, Human Texture rules, Anti-patterns, Narrator Integrity rules.
Áp dụng xuyên suốt Phase 2 khi viết script.

### Bước S1 — Đọc Big Idea
Dùng Notion MCP đọc trang Big Ideas:
`https://app.notion.com/p/377d73f564198028a6c8dbd7445d461f`

Tìm Big Idea #[N] → đọc toàn bộ nội dung (tiêu đề EN, góc tiếp cận, angle).

### Bước S2 — Tìm số video tiếp theo
Query Content Manager DB: `collection://55cd73f5-6419-826b-a3dd-8716e793b758`
Sắp xếp theo `Ngày tạo` DESC → lấy tên trang mới nhất → parse số → N+1.

Nếu không parse được số → hỏi user 1 lần duy nhất: "Video hiện tại mới nhất là số mấy?"

### Bước S3 — Tạo trang video mới
Tạo page mới trong Content Manager với:
- **Title:** `Video[N+1] — [Tên EN của Big Idea]`
- **Template:** `https://app.notion.com/p/c54d73f56419822b90bb01e2ef5bb169`
- **Properties:**
  - Nền tảng = YouTube
  - Trạng thái = Viết kịch bản
  - Big Idea = [nội dung tóm tắt từ sub-page]

Thông báo cho user: "Đã tạo trang: **Video[N+1] — [Title]** → [link trang mới]"

### Bước S4 — Đánh dấu Big Idea đã được dùng
Quay lại trang Big Ideas (`377d73f564198028a6c8dbd7445d461f`).
Tìm heading của Big Idea #[N] vừa dùng → thêm dòng ngay bên dưới heading:

```
> ✅ **Scripted** → [Video[N+1] — Title](link trang video)  |  Ngày: [DATE]
```

Ví dụ:
```
## Big Idea #2: The Science Behind Grandma's "Useless Weeds"
> ✅ **Scripted** → [Video 48 — Grandma's Useless Weeds](https://notion.so/...) | Ngày: 2026-06-06
```

Nhờ đó bất kỳ ai mở trang Big Ideas đều thấy ngay ý nào đã được viết script, ý nào còn trống.

Sau đó tiếp tục Phase 0 tự động.

---

## PHASE 0 — DEEP RESEARCH 🔴 Hard Stop sau phase

**Nạp:** `references/research-protocol.md`

### Bước 0.1 — Đọc Notion page
Dùng Notion MCP đọc trang video. Lấy:
- Channel context từ synced block (audience, DNA brand voice, competitors)
- Các field đã điền (Big Idea, Format nếu có)
- Section nào còn trống → đó là việc cần làm

### Bước 0.2 — AI Auto-Search
Tìm kiếm thực (web tool BẬT). KHÔNG dùng trí nhớ.
- Tìm theo Tier: peer-reviewed → .edu → .gov → botanical
- Mục tiêu: 5-8 claims có URL thật + năm
- Gắn cờ YMYL claims cần hedge

### Bước 0.3 — Tạo research-brief.md
Lưu local: `research/[topic-slug]/research-brief.md`
Chạy: `python scripts/citation_check.py research/[slug]/research-brief.md`
Fix claims không có URL trước khi tiếp tục.

### Bước 0.4 — Ghi vào Notion
Điền vào trang video:
- **Nghiên Cứu > Dữ liệu / nguồn research**: danh sách claims + URL
- **Đào Sâu Insight**: điền 5 câu hỏi dựa trên research

**🟢 AUTO:** Ghi research brief vào Notion xong → tự động sang Phase 1.

---

## PHASE 1 — FORMAT + OUTLINE 🔴 Hard Stop sau phase

### Bước 1.1 — Phân tích topic → đề xuất Kane format

Phân tích topic theo 3 tiêu chí:

| Tiêu chí | Jenga Longform | 30-Day Challenge |
|----------|---------------|-----------------|
| Có bí ẩn/câu hỏi phản trực giác? | ✅ Phù hợp | ❌ |
| Có quá trình thay đổi quan sát được? | ❌ | ✅ Phù hợp |
| Audience muốn giải thích hay transformation? | Giải thích | Transformation |

Đề xuất 1 format + lý do ngắn. Đề xuất format còn lại làm backup nếu user muốn thử.

### Bước 1.2 — Viết Outline

**Nếu Jenga:** Teaser reveal → câu hỏi trung tâm → thử lần 1 (thất bại) → thử lần 2 (thất bại) → breakthrough → payoff
**Nếu 30-Day:** Why → expert backing → Day blocks (1/10/15-pivot/25/30) → before-after metrics → universal lessons

Viết outline theo cấu trúc Dàn Ý của Notion:
- HOOK: cảnh mở, sự thật khó nghe, lời hứa, câu hỏi tò mò lớn
- PREVIEW: 3 phần theo thứ tự
- PHẦN 1/2/3: Setup + Beat 1/2/3 + bằng chứng + bài học + câu kéo tiếp
- KẾT LUẬN + CTA

### Bước 1.3 — Title + Thumbnail
**Nạp:** `references/title-thumb-generator.md`
Chạy đúng theo format và 🟡 Soft Stop trong file đó.

### Bước 1.4 — Ghi vào Notion
- **Nghiên Cứu > Loại Format Kịch Bản**: format chọn + framework
- **Dàn Ý**: điền đầy đủ HOOK, PREVIEW, PHẦN 1/2/3, KẾT LUẬN
- **Thông Tin Video > Tiêu đề + Thumbnail**: 3 options
- **Properties > Big Idea**: 1 câu tóm tắt
- **Properties > Hook / Tiêu đề**: title được chọn tạm

**🟢 AUTO:** Ghi outline + titles vào Notion xong → tự động sang Phase 2.

---

## PHASE 2 — VIẾT SCRIPT 🟡 Soft Stop mỗi session

**Nạp:** `references/guard-rails.md`

### Quy tắc viết

- Dựa 100% vào research-brief.md — không bịa số liệu
- Narrator voice: "practitioners report", "research shows", "gardeners have found"
- Câu thoại max 20 từ — viết để nghe, không để đọc
- Grade 6-8 reading level
- Imperial units: feet, °F, gallons, lbs
- Tham chiếu US: USDA zones, Home Depot, Lowe's

### Viết theo sessions (theo outline đã approve)

Viết từng phần: HOOK → PREVIEW → PHẦN 1 → PHẦN 2 → PHẦN 3 → KẾT LUẬN + CTA

Sau mỗi session hoàn thành 1 phần lớn:
1. Chạy: `python scripts/compliance_scan.py script_draft.txt`
2. Fix issues nếu có — tự động, không hỏi user
3. Tiếp tục session tiếp theo ngay

### Điền vào Notion — Bảng Kịch Bản Chi Tiết

Mỗi đoạn script → 1 row trong bảng:
- **#**: số thứ tự
- **Loại**: A-Roll / B-Roll / VO / Screen record / On-screen text
- **TL**: timestamp ước tính (00:00)
- **Cảm xúc / Giọng đọc**: vd "Calm, conversational", "Excited, energetic"
- **Lời thoại**: câu thoại thực (không có markdown)
- **Visual**: mô tả hình ảnh/góc máy
- **Kỹ thuật**: text on screen, SFX, effects

---

## PHASE 3 — QA + AUDIT LOOP 🔴 Hard Stop

### Bước 3.1 — Compliance Full Scan
```bash
python scripts/compliance_scan.py script_draft.txt
python scripts/word_budget.py script_draft.txt --format [E1/E2/E3/E4]
```

Báo cáo kết quả: VERDICT + danh sách issues.

### Bước 3.2 — Kane Gold Comparison
Trigger skill `mkt-kane-gold-comparison-reviewer`:
- So sánh script với video Gold của ngách (Huw Richards / Epic Gardening)
- Chấm điểm 8 drivers: First 3s, Generalist Approach, Viewer Connection, Tension Building, Cleverness, Absurdity, EOV, CTA
- Output: scorecard + top 3 priority fixes

### Bước 3.3 — Anti-Pattern Audit
Trigger skill `mkt-kane-anti-pattern-auditor`:
- Kiểm tra 4 downward drivers
- Output: danh sách evidence + priority fixes

### Bước 3.4 — Phản Biện Toàn Diện
Claude tự phản biện script theo 5 góc:
1. **Retention**: có đủ tension? Gate ở đâu? Người xem có lý do ở lại không?
2. **Clarity**: có câu nào mơ hồ hoặc cần ngữ cảnh không?
3. **Evidence**: có claim nào chưa có nguồn?
4. **Hook**: 30 giây đầu có đủ mạnh theo Kallaway SSSQ?
5. **CTA**: có 1 hành động cụ thể, dễ làm?

**🔴 GATE 3:** Trình bày toàn bộ audit report. Hỏi:
- "Muốn sửa điểm nào trước?"
Chờ user chỉ định → sửa → re-scan compliance → confirm.

---

## PHASE 4 — TTS CLEAN + EXPORT 🟢 Auto

### Bước 4.1 — TTS Clean
```bash
python scripts/tts_clean.py script_final.txt > script_voiceAI.txt
```

### Bước 4.2 — Ghi vào Notion
Tạo sub-page dưới video: **Script_Final_voiceAI**
Dán 100% nội dung đã clean vào sub-page đó.

Cập nhật Properties:
- **Trạng thái** → "QA Done"
- **Hook / Tiêu đề** → title đã chọn cuối cùng

---

## PHASE 5 — ES TRANSLATION (Optional) 🟡 Soft Stop

Hỏi user: "Muốn tạo bản ES (US Hispanic) không?"

Nếu yes:
- Nguồn: sub-page Script_Final_voiceAI
- Áp dụng prompt dịch EN→ES (US Hispanic neutral) đã có trong Notion
- Output: sub-page mới `{VIDEO_TITLE}_ES_USHispanic_v1.0`
- Tuân thủ: Español neutro, usted, Imperial units, code-switching ≤3%, no vosotros

---

## PHASE 6 — SEO DESCRIPTION + PINNED COMMENT 🟡 Soft Stop

Hỏi user: "Muốn tạo SEO description cho YouTube không?"

Nếu yes:

### Bước 6.1 — Lấy dữ liệu từ trang video Notion
Đọc 4 nhóm dữ liệu trên trang video hiện tại:
1. **Thông Tin Kênh**: Audience, DNA Brand Voice, positioning
2. **Thông Tin Video**: thông điệp, keyword chính + phụ, Tiêu đề + Thumbnail, video tiếp theo, sponsor (nếu có)
3. **Dàn Ý**: HOOK/PREVIEW + các phần chính
4. **Nghiên Cứu**: link tham khảo, nguồn research

Thiếu dữ liệu → ghi `[NEED DATA: …]`, KHÔNG bịa.

### Bước 6.2 — Viết SEO Description (EN)

Theo rules bắt buộc:
- **1–2 dòng đầu**: Keyword chính + Hook rõ ràng
- **Độ dài**: 1200–2500 ký tự
- **Tông giọng**: DNA Brand Voice (thẳng thắn, không phóng đại)
- **Keyword**: chính 1–2 lần trong 3–4 dòng đầu, phụ rải tự nhiên trong bullets
- **KHÔNG nhồi hashtag** trong phần mô tả chính

**Disclaimers bắt buộc (thứ tự cố định):**
1. 🤖 AI Disclosure — LUÔN LUÔN có, không điều kiện
2. Affiliate — chỉ khi video page ghi có affiliate links
3. YMYL — chỉ khi có cỏ dại/thảo dược/dinh dưỡng/sức khỏe
4. Sponsor — chỉ khi video page ghi có sponsor

**References**: chỉ thêm section `📚 REFERENCES:` nếu script có claim số liệu cụ thể.

### Bước 6.3 — Viết Pinned Comment

Xoay vòng 3 kiểu (A→B→C theo từng video):
- **A**: Câu hỏi mở kích thích chia sẻ kinh nghiệm
- **B**: Bonus tip không có trong video
- **C**: CTA nhẹ nhàng + câu hỏi

≤ 300 ký tự. KHÔNG nhồi keyword, KHÔNG spam link.

### Bước 6.4 — Kiểm tra ES

Kiểm tra trong trang video xem có sub-page `{TITLE}_ES_USHispanic_v1.0` không:
- **Có** → tạo thêm 1 sub-page SEO ES theo ES overrides (usted, Imperial, keyword whitelist ES US-Hispanic, AI Disclosure ES, pinned comment ES)
- **Không có** → chỉ xuất 1 bản EN

### Bước 6.5 — Ghi vào Notion

Tạo sub-page dưới khung **TTS CLEAN SCRIPT** của trang video:
- EN: `YouTube SEO Description — {TIÊU ĐỀ VIDEO NGẮN}`
- ES (nếu có): `YouTube SEO Description — {TIÊU ĐỀ VIDEO NGẮN} (ES)`

Mỗi sub-page chứa: SEO Description đầy đủ + Pinned Comment ở cuối.

---

## Nguyên Tắc Cứng

1. Phần kiểm tra máy móc → CHẠY SCRIPT, không quét bằng mắt
2. Thiếu data → `[NEED DATA: ...]`, KHÔNG bịa
3. Narrator = educator, KHÔNG đóng vai nhân chứng cá nhân
4. Hard gate → BẮT BUỘC dừng chờ user, không tự tiếp
5. Brand voice đọc từ synced block trên Notion page — không tự suy diễn
