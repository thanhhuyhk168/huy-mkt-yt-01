# Research Protocol — US Gardening Channel

## Mục tiêu
Tìm kiếm dữ liệu thực từ nguồn chính thống để làm tư liệu viết script. KHÔNG bịa số liệu. KHÔNG dùng trí nhớ làm nguồn sự thật.

---

## Source Priority (Tier)

| Tier | Nguồn | Ví dụ |
|------|-------|-------|
| **Tier 1** | Peer-reviewed journals | Journal of Experimental Botany, HortScience |
| **Tier 2** | .edu / Extension services | extension.umd.edu, extension.psu.edu |
| **Tier 3** | .gov / NGO | USDA.gov, EPA.gov, RHS.org.uk |
| **Tier 4** | Botanical societies | AmericanHorticulturalSociety, PlantSociety |

Ưu tiên Tier 1 → 2 → 3 → 4. Tìm thêm nếu chỉ có Tier 4.

---

## Output Format — research-brief.md

```markdown
# Research Brief: [TOPIC]
Date: [DATE]
Video page: [NOTION URL]

## Key Claims

- [Claim ngắn, 1 câu] — [URL] ([Năm])
- [Claim ngắn, 1 câu] — [URL] ([Năm])
...

## Supporting Stats

- [Số liệu cụ thể] — [URL] ([Năm])
...

## YMYL Flags (cần hedge)

- [Claim liên quan sức khỏe/an toàn] → hedge: "according to [source]"
...

## Gaps (không tìm được nguồn)

- [Claim] → [NEED DATA]
```

---

## Quy tắc cứng

1. Mỗi claim **bắt buộc có URL thật** — nếu không tìm được → ghi `[NEED DATA]`, không bịa
2. URL phải còn live — chạy `citation_check.py research-brief.md` để verify
3. Claim về pets/trẻ em/độc tính → Tier 1-2 bắt buộc, không dùng Tier 4
4. Số liệu phải có năm — tránh số liệu > 5 năm nếu có bản mới hơn
5. Sau khi viết research-brief.md → ghi vào Notion page > "Nghiên Cứu" > "Dữ liệu / nguồn research"
