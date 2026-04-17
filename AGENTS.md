# AI PM Research — Agent Workflow

## Atlassian MCP defaults

- **Defaults file**: Jira project key, Confluence space, and default parent pages live in `.cursor/defaults.md`. Rule `03-jira-confluence-defaults.mdc` points agents to that file.
- **Epic**: Before **any** Jira MCP call that creates or links issues to an Epic, **obtain the Epic key** from the user. If it was mentioned earlier in the thread, **quote it back and ask for explicit confirmation** (e.g. “Confirm Epic `PROJ-123` before I publish?”). **Never** publish without that confirmation. If the user has not provided an Epic, **ask**; do not assume or infer.
- **Confluence page / parent**: The **publish_confluence** agent proposes a title and suggests a parent from `.cursor/defaults.md`; it always asks for user confirmation before publishing.
- Use `maxResults: 10` or `limit: 10` for Jira JQL and Confluence CQL searches unless the user asks for more.
- **Research file link**: Whenever research is saved under `research/*.md`, the assistant’s message **must** include the **repo-relative path** to that file (e.g. `research/my-feature-research.md`) so the user can open the artifact in the workspace.
- In a single chat turn, agents should not narrate the entire AGENTS pipeline; only the current step + one next-step line.

---

## Workflow Overview

1. **Input**: User provides 1–2 lines (or 2–3) for the feature/research topic, plus optional project brief and screenshot. User should also provide (or agent must **ask for**) **Jira Epic** (key/number) and **Confluence page** (target page for requirements). If either is missing when creating Confluence content or Jira stories, **ask** before proceeding.
2. **Research**: Deep research within project boundaries (user-problem first, to-the-point). See rules: research scope (`00-research-scope.mdc`), research style. **Context:** read `context/product-definition.md` (capabilities) and `context/industry-context.md` (market, personas, competitors) before research. If research is written to the repo, save it under `research/` and include that file path in the chat response (see **Research file link** above and `01-research-style.mdc` → Output).
3. **Devil's Advocate** (optional but recommended): Run on the **research deliverable** (e.g. markdown under `research/`), on **requirements**, and/or on **stories** as appropriate. Challenge assumptions, find gaps, argue against. See rule `05-devils-advocate.mdc`.
4. **Confluence**: **publish_confluence** agent drafts from `templates/confluence-requirement-template.md` (format is defined there) and publishes via Confluence MCP. Hierarchical requirement IDs (`REQ-{AREA}-{NN}`, e.g. REQ-AUTH-01) for traceability.
5. **Stories**: **create_stories** agent creates user stories (and optional technical tasks) in **Gherkin format**; includes **NFRs** when applicable; ensures **every story maps to at least one requirement ID** (traceability). Does not publish to Jira. See rules: story format, story–requirement traceability.
6. **Devil's Advocate**: Run Devil's Advocate on the drafted stories (rule `05-devils-advocate.mdc`). User reviews and gives go-ahead.
7. **Jira**: **publish_jira** agent publishes the reviewed stories to Jira via Atlassian MCP after DA sign-off; links to Epic; includes "Maps to:" each requirement ID (e.g. REQ-AUTH-01) in each story. **Epic:** `publish_jira` must receive **explicit user confirmation** of the Epic key immediately before MCP publish (see Atlassian MCP defaults → Epic).
8. **Bolt prompt**: Produce a single, copy-paste prompt for Bolt (or another AI coding tool) to build a working prototype from the requirement and stories.

---

## When to Use Which Agent / Rule

- **Research**: Always use research scope + research style rules; use `context/product-definition.md` + `context/industry-context.md` as SSOT.
- **Devil's Advocate**: Invoke when the user asks, or per workflow — on **research** (file under `research/` or draft in chat), on **requirements**, or on **stories**; before Confluence and/or before Jira as described in `05-devils-advocate.mdc`.
- **Story ↔ requirement**: Always when creating or reviewing stories; use traceability rule to validate before handover to Devil's Advocate.
- **Story format**: Always Gherkin + NFRs when applicable (see story format rule).
- **publish_jira**: Use after Devil's Advocate has reviewed the stories and user has given go-ahead.

---

## Project Setup (for new teams)

1. Set **Jira project key**, **Confluence space**, and default parent pages in `.cursor/defaults.md`.
2. Customize **`context/product-definition.md`** (product name, platform, **current features** after each release) and **`context/industry-context.md`** (industry, personas, competitors, SMB toggle) for your product. Keep both aligned when forking.
3. For each run, user provides or is asked for **Epic** and **Confluence page** (or parent) as needed.
4. Confluence page format is defined in `templates/confluence-requirement-template.md`; **publish_confluence** uses it and MCP to create and publish.
5. Add project brief / "what we're doing" in chat or in a doc in `context/`.
6. Optional: Add screenshots to `context/` or `base-features-screenshots/` for theme and current UI.
