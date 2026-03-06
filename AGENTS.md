# AI PM Research — Agent Workflow

## Atlassian MCP defaults

- **Defaults file**: Jira project key, Confluence space, and default parent pages live in `.cursor/defaults.md`. Rule `03-jira-confluence-defaults.mdc` points agents to that file.
- **Epic**: Use the Jira Epic key/number provided by the user for the initiative. If missing when creating or linking stories, **ask**.
- **Confluence page / parent**: The **publish_confluence** agent proposes a title and suggests a parent from `.cursor/defaults.md`; it always asks for user confirmation before publishing.
- Use `maxResults: 10` or `limit: 10` for Jira JQL and Confluence CQL searches unless the user asks for more.

---

## Workflow Overview

1. **Input**: User provides 1–2 lines (or 2–3) for the feature/research topic, plus optional project brief and screenshot. User should also provide (or agent must **ask for**) **Jira Epic** (key/number) and **Confluence page** (target page for requirements). If either is missing when creating Confluence content or Jira stories, **ask** before proceeding.
2. **Research**: Deep research within project boundaries (user-problem first, to-the-point). See rules: project context, research style.
3. **Devil's Advocate** (optional but recommended): Run a Devil's Advocate pass on the research/requirement. Challenge assumptions, find gaps, argue against. See rule `05-devils-advocate.mdc`.
4. **Confluence**: **publish_confluence** agent drafts from `templates/confluence-requirement-template.md` (format is defined there) and publishes via Confluence MCP. Requirement IDs (REQ-1, REQ-2, …) for traceability.
5. **Stories**: Create user stories (and technical tasks) in **Gherkin format**; include **NFRs** when applicable. **Every story must map to at least one requirement ID** (traceability). See rules: story format, story–requirement traceability.
6. **Traceability check**: Ensure every requirement has ≥1 story and every story has ≥1 requirement ID. Fix or report gaps.
7. **Jira**: Publish stories and tasks to Jira via Atlassian MCP. Include "Maps to: REQ-x" in each story.
8. **Bolt prompt**: Produce a single, copy-paste prompt for Bolt (or another AI coding tool) to build a working prototype from the requirement and stories.

---

## When to Use Which Agent / Rule

- **Research**: Always use project context + research style rules.
- **Devil's Advocate**: Invoke when user says "run Devil's Advocate" or as part of the full workflow after research (before or after Confluence).
- **Story ↔ requirement**: Always when creating or reviewing stories; use traceability rule to validate before Jira publish.
- **Story format**: Always Gherkin + NFRs when applicable (see story format rule).

---

## Project Setup (for new teams)

1. Set **Jira project key**, **Confluence space**, and default parent pages in `.cursor/defaults.md`.
2. For each run, user provides or is asked for **Epic** and **Confluence page** (or parent) as needed.
3. Confluence page format is defined in `templates/confluence-requirement-template.md`; **publish_confluence** uses it and MCP to create and publish.
4. Add project brief / "what we're doing" in chat or in a doc in `context/`.
5. Optional: Add screenshots to `context/` for theme and current UI.
