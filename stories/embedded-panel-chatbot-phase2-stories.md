# User Stories: Embedded Panel Chatbot — Phase 2: Context-Aware AI & "Ask IQ"

**Source:** Confluence page "Embedded Panel Chatbot — Phase 2: Context-Aware AI & Ask IQ Requirements" (pageId=1372621889)
**Requirements:** REQ-18 through REQ-31, NFR-7
**Feature:** Context-Aware AI & "Ask IQ"
**Dependency:** Phase 1 stories (Stories 1–10) must be implemented first.

---

## Definitions

- **"Ask IQ" popup:** A small floating card (Rufus-style) that appears near the right edge of the viewport when the user multi-selects table rows or clicks a dashboard widget LITA icon. Contains up to 3 smart suggestions plus "Something else".
- **Smart suggestions:** Prompts from the prompt store, matched by page definition + entity type or widget type via semantic search.
- **Context chip:** A visible, dismissible badge near the panel input bar showing what context is attached to the next message (e.g. "3 devices selected").
- **Context attachment indicator:** A per-message collapsible detail shown on sent messages that included context (e.g. "With: 3 devices (AHELSINGER, GYSCLUMY, JQARTSSR)").
- **Entity IDs:** Key identifiers for selected entities (device IDs, package IDs, app IDs, patch IDs).
- **LITA icon:** An AI sparkle / IT Assist brand icon placed on dashboard widgets to trigger "Ask IQ".

---

## Story 11: "Ask IQ" popup trigger on data tables

**Maps to:** REQ-18, REQ-31, NFR-7

As an IT Admin viewing a data table
I want an "Ask IQ" popup to appear when I select multiple rows
So that I can quickly ask AI questions about my selection without typing a prompt from scratch

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Popup appears when more than 1 row is selected on any page with a data table | I am on any platform page that contains a data table and have selected 0 or 1 row | I select a second row (total selection > 1) | An "Ask IQ" floating popup appears near the right edge of the viewport. The popup displays the "Ask IQ" header with an AI icon |
| Popup does not appear on single row selection | I am on any page with a data table | I select exactly 1 row | The "Ask IQ" popup does not appear |
| Popup is dismissible by clicking outside | The "Ask IQ" popup is visible | I click anywhere outside the popup | The popup closes. My row selection is preserved |
| Popup is dismissible by deselecting rows | The "Ask IQ" popup is visible | I deselect rows so that 1 or fewer rows are selected | The popup closes |
| Popup appears within 500ms | I am on any page with a data table | I select more than 1 row | The "Ask IQ" popup appears within 500ms of the selection threshold being met |

---

## Story 12: "Ask IQ" smart suggestions and popup content

**Maps to:** REQ-19, REQ-28, REQ-29

As an IT Admin
I want the "Ask IQ" popup to show relevant suggestions based on what I've selected
So that I can act on my selection with one click instead of formulating a prompt

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Popup shows up to 3 smart suggestions plus "Something else" | I have selected 3 devices on Device Management > Devices and the "Ask IQ" popup appears | I view the popup | I see up to 3 smart suggestions matched from the prompt store. I see a "Something else" option as the last item. The suggestions are relevant to the entity type (devices) |
| Suggestions are matched by page definition and entity type | I am on App Management > Patch and select 2 patches | The "Ask IQ" popup appears | The suggestions are matched against the prompt store using "App Management > Patch" and entity type "patch". The suggestions differ from those shown for device selections |
| No matching prompts shows only "Something else" | I have selected rows on a supported table and the prompt store has no tagged prompts for this entity type | The "Ask IQ" popup appears | The popup shows only "Something else". No empty suggestion slots are displayed |

---

## Story 13: Clicking a suggestion fires into the panel

**Maps to:** REQ-20, REQ-22

As an IT Admin
I want to click a suggestion and have it immediately sent to the chatbot with my selection as context
So that I get a contextual answer in one click

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Suggestion opens a closed panel and fires into the active thread | The side panel is closed and the "Ask IQ" popup is visible with suggestions | I click a suggestion (e.g. "Show warranty status for selected devices") | The side panel opens. The suggestion is sent as a message in the existing active thread. The selected entity IDs are attached as context to the message. The popup closes |
| Suggestion fires into an already-open panel | The side panel is open with an active thread and the "Ask IQ" popup is visible | I click a suggestion | The suggestion is sent as a message in the existing active thread. No new thread is created. The popup closes |
| Suggestions are disabled while panel is processing a response | The side panel is processing a response (in-progress state) and the "Ask IQ" popup is visible | I view the popup suggestions | All suggestions and "Something else" are greyed out / disabled. Hovering over a disabled suggestion shows a tooltip: "You can trigger once current response is fully generated" |
| Suggestions re-enable after response completes | The "Ask IQ" popup suggestions are disabled (panel processing) | The panel finishes generating the response | The popup suggestions become active and clickable again |
| Suggestion when panel is open on home screen (no active thread) | The side panel is open showing the home screen (no active thread) and the "Ask IQ" popup is visible | I click a suggestion | A new thread is created. The suggestion is sent as the first message in the new thread. The selected entity IDs are attached as context. The popup closes |

---

## Story 14: "Something else" opens the panel with context

**Maps to:** REQ-21

As an IT Admin
I want to click "Something else" and type my own question with my selection automatically attached
So that I can ask any question about my selection without re-entering what I've selected

| Scenario | Given | When | Then |
|----------|-------|------|------|
| "Something else" opens a closed panel with context chip | The side panel is closed and the "Ask IQ" popup is visible | I click "Something else" | The side panel opens. The input bar gains focus. A context chip appears near the input bar (e.g. "3 devices selected"). The popup closes |
| "Something else" focuses input in an already-open panel | The side panel is already open and the "Ask IQ" popup is visible | I click "Something else" | The input bar gains focus. A context chip appears near the input bar. The popup closes |
| User sends a message with context from "Something else" | I clicked "Something else" and the context chip is visible | I type a question (e.g. "What is the battery health of these devices?") and send the message | The message is sent with the selected entity IDs as context. The context chip clears after sending |
| User dismisses the context chip and asks without context | I clicked "Something else" and the context chip is visible | I click the X on the context chip | The context is removed. I can type and send a message without any selection context attached |

---

## Story 15: "Ask IQ" on dashboard widgets

**Maps to:** REQ-23

As an IT Admin viewing the Dashboard
I want each widget to have an AI icon I can click for contextual suggestions
So that I can ask questions about specific dashboard data without formulating a prompt

| Scenario | Given | When | Then |
|----------|-------|------|------|
| LITA icon is visible on each dashboard widget | I am on the Dashboard page | I view the dashboard widgets | Each widget (Total Devices, Device Connectivity, Current Issue Summary, System Update, Overall Health Score) displays a LITA icon in its header or corner |
| Clicking the LITA icon opens an "Ask IQ" popup | I am on the Dashboard page | I click the LITA icon on the Device Connectivity widget | An "Ask IQ" popup appears. The popup shows up to 3 smart suggestions matched by widget type "Device Connectivity" and its data. The popup shows "Something else" as the last option |
| Widget suggestion opens panel and fires into active thread | The "Ask IQ" popup is visible for a dashboard widget | I click a suggestion (e.g. "Why are so many devices offline?") | The side panel opens (if closed). The suggestion is sent as a message with the widget context (widget type + key data points). The popup closes |
| Widget "Something else" opens panel with widget context chip | The "Ask IQ" popup is visible for a dashboard widget | I click "Something else" | The side panel opens (if closed). The input bar gains focus. A context chip appears (e.g. "Device Connectivity widget"). The popup closes |

---

## Story 16: Context chip lifecycle

**Maps to:** REQ-24, REQ-25, REQ-26

As an IT Admin
I want to see what context is attached to my next message and control whether to include it
So that I have transparency over what the AI will use and can opt out if I want a general answer

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Context chip shows summary of attached context | I triggered "Ask IQ" and the context chip is visible | I view the input area | The chip displays a summary (e.g. "[icon] 3 devices selected" or "[icon] Device Connectivity widget"). The chip has a dismiss (X) button |
| Context chip displays "20+" for large selections | I am on Device Management > Devices and have selected 25 devices | I trigger "Ask IQ" and the context chip appears | The chip displays "20+ devices selected". The full set of entity IDs is still included in the payload when a message is sent |
| Context chip clears after sending a message | The context chip is visible | I send a message | The context chip clears. The message includes the attached context |
| Context chip clears when dismissed | The context chip is visible | I click the X on the chip | The chip is removed. No context is attached to the next message |
| Context chip clears on page navigation | The context chip is visible | I navigate to a different page | The context chip clears |
| Context chip clears when rows are deselected | The context chip is visible from a table selection | I deselect all rows on the table | The context chip clears |
| Context chip updates when selection changes | I selected 3 devices and the context chip shows "3 devices selected" | I select 2 additional devices (total 5) | The context chip updates to "5 devices selected". Deselecting 1 device updates chip to "4 devices selected" |

---

## Story 17: Per-message context attachment display

**Maps to:** REQ-27

As an IT Admin
I want to see what context was attached to each message in the chat history
So that I understand which data the AI used when answering

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Context attachment indicator on sent message | I sent a message with context (e.g. 3 devices selected) | I view the message in the chat | The message displays a context attachment indicator below it. The indicator reads e.g. "With: 3 devices (AHELSINGER, GYSCLUMY, JQARTSSR)" |
| Context indicator is collapsible | A message has a context attachment indicator | I click to collapse the indicator | The detail is hidden but a collapsed marker remains. Clicking to expand shows the full context detail again |
| Context indicator coexists with Phase 1 page context label | I sent a message with context from Device Management > Devices | I view the message | I see the Phase 1 page context label: "From: Device Management > Devices". I see the context attachment indicator: "With: 3 devices (…)". Both are visible on the same message |
| Messages without context show no indicator | I sent a message without any "Ask IQ" context attached | I view the message | No context attachment indicator is displayed. The Phase 1 page context label is still shown |

---

## Story 18: Thread list in panel (moved from Phase 1) — GAI-7381

**Maps to:** REQ-7, REQ-8

As an IT Admin
I want to view and switch between my recent threads from within the panel
So that I can resume past conversations without navigating to the full-page chatbot

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Thread list is collapsed by default | The panel is open | I look at the panel header | The thread list is collapsed (not visible). I see a thread list toggle icon (e.g. hamburger or thread icon) |
| Expand thread list to view recent threads | The thread list is collapsed | I click the thread list toggle | The thread list expands within the panel. I see recent threads with title and timestamp |
| Switch to a different thread | The thread list is expanded | I click on a different thread | The panel switches to display the selected thread. The thread list collapses |
| Full thread management is not available in the panel | The thread list is expanded in the panel | I view the thread list | I do not see options to pin, rename, or delete threads. These actions are available only in the full-page LITA view |

---

## Story 20: Page-specific pre-canned prompts on home screen (moved from Phase 1) — GAI-7445

**Maps to:** REQ-9, REQ-10, REQ-11

As an IT Admin
I want to see relevant suggested prompts based on which page I'm on
So that I can quickly ask relevant questions without having to formulate them myself

| Scenario | Given | When | Then |
|----------|-------|------|------|
| Home screen shows prompts relevant to the current page | I am on the Dashboard page and the panel is showing the home screen (no active thread) | I view the panel | I see pre-canned prompts relevant to the Dashboard (e.g. "How many devices are offline right now?", "Explain the overall health score") |
| Prompts update when navigating with the home screen open | The panel is open and showing the home screen and I am on the Dashboard | I navigate to Device Management > Devices | The home screen prompts update to show Device Management-relevant prompts (e.g. "What devices have expiring warranties?", "How do I export my device list?") |
| Fallback to global prompts when no page-specific set is configured | I am on a page with no page-specific prompts configured and the panel is showing the home screen | I view the panel | I see the default global prompt set (same as the current chatbot home page) |
| Pre-canned prompts are configurable without code changes | The page-specific prompt mapping is stored in a configuration file or catalogue | The PM or content team updates the prompt mapping | The changes are reflected in the panel without a code redeployment |
| Clicking a pre-canned prompt sends it as a message | The panel is showing the home screen with page-specific prompts | I click a pre-canned prompt | The prompt is sent as a message in a new thread. The panel displays the AI response |

---

## NFRs (applied across Phase 2 stories)

| NFR | Description | Relevant stories |
|-----|-------------|-----------------|
| NFR-7 | "Ask IQ" popup ≤500ms after trigger | Story 11 |

---

## Traceability summary

| Requirement | Story(ies) | Notes |
|-------------|------------|-------|
| REQ-7 | Story 18 | Moved from Phase 1 |
| REQ-8 | Story 18 | Moved from Phase 1 |
| REQ-9 | Story 20 | Moved from Phase 1 |
| REQ-10 | Story 20 | Moved from Phase 1 |
| REQ-11 | Story 20 | Moved from Phase 1 |
| REQ-18 | Story 11 | |
| REQ-19 | Story 12 | |
| REQ-20 | Story 13 | |
| REQ-21 | Story 14 | |
| REQ-22 | Story 13 | |
| REQ-23 | Story 15 | |
| REQ-24 | Story 16 | |
| REQ-25 | Story 16 | |
| REQ-26 | Story 16 | |
| REQ-27 | Story 17 | |
| REQ-28 | Story 12 | |
| REQ-29 | Story 12 | |
| REQ-30 | N/A — existing infrastructure | |
| REQ-31 | Story 11 | |

- **Every functional requirement has at least one story:** Yes (REQ-30 covered by existing infrastructure).
- **Every story has at least one requirement:** Yes.

---

## Jira field mapping (for publish_jira)

| Story element | Jira field |
|---------------|------------|
| Summary | **Summary** — prefix with `[Phase 2: short name]` |
| Story narrative (As a … I want … So that …) | **ATDD - As Persona** |
| Acceptance criteria (table) | **ATDD - Acceptance Criteria** |
| Domain terms | **ATDD - Domain Terms** — use **"To do"** |
| Maps to REQ-x | **Description** |

---

**Status:** Draft ready for review. Run **Devil's Advocate** for review. After sign-off, use **publish_jira** to publish to Jira.
