# Project defaults

Single place for Confluence, Jira, and other defaults. Agents and rules use this file when they need space keys, parent pages, project keys, etc.

---

## Confluence

| Key | Value | Notes |
|-----|--------|--------|
| Space key / ID | YOURSPACE | Confluence space for requirement pages. Replace with your space key or ID. |
| Default parent page(s) | Requirements | Suggested parent for new requirement pages. Agent always asks for confirmation. |

- **Default parent pages**: List one or more suggested parents (title or page ID). The **publish_confluence** agent suggests these and always seeks user confirmation before publishing.

---

## Jira

| Key | Value | Notes |
|-----|--------|--------|
| Project key | YOURPROJ | Jira project for stories/epics. Replace with your project key. |

- Add other Jira defaults here as needed (e.g. default board, epic custom field).

---

## Other

- Use this section for any other default pages or IDs (e.g. other tools, links).
