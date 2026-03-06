# AI PM Research — Cursor Project

Use this project to go from **1–2 lines of feature idea** to **research → Confluence requirements → Jira stories (Gherkin + NFRs) → Bolt prototype prompt**, with Devil's Advocate and story–requirement traceability.

## Prerequisites

- **Cursor** (IDE) with access to MCP.
- **Atlassian Cloud** (Jira + Confluence). First time: authorize the Atlassian MCP (OAuth or API token) when Cursor prompts you.
- Set your **Jira project key**, **Confluence space**, and default parent pages in `.cursor/defaults.md`. For each research run, provide or be asked for **Epic** and **Confluence page** as needed.

## Quick start

1. **Open this folder in Cursor.**  
   The project uses `.cursor/mcp.json` for the Atlassian MCP. If prompted, complete Atlassian OAuth (or API token).

2. **Set your defaults**  
   Edit `.cursor/defaults.md`: set Jira project key, Confluence space, and default parent page(s). For each run, you will provide or be asked for **Epic** (Jira) and **Confluence page** (target/parent) as needed.

3. **Optional: add project context**  
   - Put a short “what this product is” / “what we’re doing” in `context/` or paste it in chat.  
   - Add a screenshot in `context/` for current UI/themes.  
   - Customize `templates/confluence-requirement-template.md` with your Confluence page format.

4. **Run the workflow in Composer**  
   Example prompt:

   > Do deep research on [your 1–2 line feature]. Stay within our project boundaries. Then:  
   > 1) Run a Devil's Advocate pass on the research.  
   > 2) Create and publish the requirement page in Confluence using our format (with requirement IDs).  
   > 3) Create user stories and technical tasks in Gherkin format; add NFRs where applicable. Ensure every story maps to a requirement ID.  
   > 4) Validate traceability (every REQ has a story, every story has a REQ).  
   > 5) Publish the stories to Jira.  
   > 6) Give me a single prompt I can paste into Bolt to build a working prototype.

## What’s in this project

| Path | Purpose |
|------|--------|
| `.cursor/mcp.json` | Atlassian MCP (Confluence + Jira). Shareable; each user authorizes with their own Atlassian account. |
| `.cursor/rules/` | Project and research rules, Jira/Confluence defaults pointer, **story format (Gherkin + NFRs)**, **Devil's Advocate**, **story–requirement traceability**. |
| `AGENTS.md` | Workflow steps, when to run Devil's Advocate and traceability, Atlassian defaults. |
| `templates/confluence-requirement-template.md` | Confluence page structure. Replace with your team’s format. |
| `context/` | Optional: project one-pager, screenshots (for theme/current UI only). |

## Story format (Gherkin + NFRs)

- All user stories and acceptance criteria are in **Gherkin** (Feature, Scenario, Given/When/Then).  
- NFRs are included **when applicable** (e.g. performance, security, accessibility).  
- Rule: `.cursor/rules/04-story-format.mdc`.

## Devil's Advocate

- Use when you want assumptions challenged, gaps found, and counter-arguments before locking requirements or stories.  
- Rule: `.cursor/rules/05-devils-advocate.mdc`.  
- You can ask: “Run Devil's Advocate on this requirement” or “Run Devil's Advocate on these stories.”

## Story ↔ requirement mapping

- Every story must **map to at least one requirement ID** (e.g. REQ-1) from the Confluence page.  
- Before publishing to Jira, the agent checks: every requirement has ≥1 story, every story has ≥1 requirement.  
- Rule: `.cursor/rules/06-story-requirement-traceability.mdc`.

## Sharing with others

- Clone or share the repo. Everyone gets the same `.cursor/` and rules.  
- Each teammate must complete Atlassian MCP auth (OAuth or API token) once in Cursor.  
- Keep `.cursor/defaults.md` updated with the right Jira project key, Confluence space, and default parent pages for the team.
