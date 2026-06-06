# Project: du-an-youtube-01

## Channel Kits

| Channel | Skill | Trigger |
|---------|-------|---------|
| US Gardening | `du-an-youtube-01/youtube-garden-us/SKILL.md` | "Script big idea #N" |

## Cách dùng

Khi user nói **"Script big idea #[N]"** hoặc **"Viết kịch bản big idea #[N]"**:
→ Đọc `du-an-youtube-01/youtube-garden-us/SKILL.md` và chạy toàn bộ pipeline từ đầu.
→ Tất cả data lấy từ Notion qua MCP — KHÔNG tìm file local.

## Notion Pointers (đã hardcode trong SKILL.md)

- Big Ideas: https://app.notion.com/p/377d73f564198028a6c8dbd7445d461f
- DNA Brand Voice: https://app.notion.com/p/4fed73f5641983298ab9814692167e81
- Content Manager DB: collection://55cd73f5-6419-826b-a3dd-8716e793b758
- Video Template: https://app.notion.com/p/c54d73f56419822b90bb01e2ef5bb169

## Scripts (cần Python 3 + num2words)

```
pip install num2words
```
