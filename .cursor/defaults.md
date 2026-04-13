# Project defaults

Add your Confluence and Jira links below. Agents use this file for space key, parent pages, and project key; they always ask for your confirmation before using them.

See **How to add default Confluence and Jira links** in `.cursor/rules/03-jira-confluence-defaults.mdc` for where to find these values.

---

## Confluence

| Key | Value | Notes |
|-----|--------|--------|
| Feature parent page | https://confluence.tc.lenovo.com/spaces/CGA/pages/919799978/IT+Assist+Features| Root to parent page |

---

## Jira

| Key | Value | Notes |
|-----|--------|--------|
| UGAIN| https://jira.tc.lenovo.com/projects/GAI/issues| Project key |

---

## Jira Story Defaults

When creating or publishing stories in Jira, house the content as follows:

### Field mapping

| Story element | Jira field / section |
|---------------|----------------------|
| Story title / summary | **Summary** — prefix with feature short name in brackets (e.g. `[Caching] Short description`) |
| Story narrative (As a … I want … So that …) | **ATDD - As Persona** |
| Acceptance criteria (Gherkin) | **ATDD - Acceptance Criteria** |
| Domain terms placeholder | **ATDD - Domain Terms** — use **"To do"** |
| Additional info (if any) | **Description** |

### Default field values

| Field | Default value |
|-------|---------------|
| **Priority** | Major |
| **Components** | UGAIN-PL |
| **BST - Business Segment Target** | Commercial |
| **Labels** | IQ-Platform, NotGroomed, CREATED_BY_CURSOR |

---

## Other

| Key | Value | Notes |
|-----|--------|--------|
| | | Add any other default links (e.g. board ID) |
