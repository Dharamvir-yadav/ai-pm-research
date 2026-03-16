# Embedded Panel Chatbot — Phase 2: Context-Aware AI & "Ask IQ"

**Feature:** Context-aware interactions and "Ask IQ" contextual triggers for the Lenovo IT Assist side panel.

**Dependency:** Phase 1 (right-side panel chatbot on every screen) must be implemented first. Phase 2 builds on top of it.

---

## 1. Problem Statement

### Why context awareness matters

Phase 1 makes the chatbot accessible from every page, but the chatbot has no awareness of what the user is looking at or doing. An IT Admin viewing a list of 746 devices with 427 offline still has to manually describe their situation when asking for help. This creates friction:

1. **Prompt formulation burden.** The user knows what they're looking at but has to translate it into a prompt. "Show me the warranty status for devices AHELSINGER, GYSCLUMY, JQARTSSR" is tedious to type when those devices are already selected on screen.
2. **Missed high-intent moments.** When a user selects multiple devices or examines a dashboard widget, they have implicit questions. Without contextual triggers, the chatbot misses these moments.
3. **Generic responses.** Without page or selection context, the chatbot answers generically even when specific, grounded answers would be more useful.

### What Phase 2 adds

Two capabilities layered on top of Phase 1:

1. **"Ask IQ" contextual triggers** — popup with smart suggestions that appear at high-intent moments (row selection on tables, widget interaction on dashboards).
2. **Context injection** — passing page context and entity IDs to the chatbot so responses are grounded in what the user is working with.

---

## 2. "Ask IQ" on Data Tables

### 2.1 Trigger

When the user selects **more than 1 row** on a data table (e.g. Device Management > Devices), an "Ask IQ" popup appears.

- **Popup style:** Small floating popup, similar to Amazon Rufus but less intrusive.
- **Placement:** Positioned near the right edge of the viewport (close to where the side panel would open), not center-screen. This keeps it visible but non-obstructive to the table content.
- **Trigger threshold:** >1 row selected. Single row selection does not trigger the popup.
- **Dismissible:** The popup can be dismissed by clicking outside it or deselecting rows.

### 2.2 Popup content

The popup shows:

1. **Up to 3 smart suggestions** from the prompt store, matched based on:
   - The page definition (e.g. "Device Management > Devices")
   - The type of selection (e.g. "devices selected")
   - Semantic matching against the prompt store
2. **"Something else"** — always present as the last option. Opens the panel with context loaded, letting the user type freely.

Example suggestions for Device Management > Devices with 3 devices selected:
- "Run a system scan on selected devices"
- "Show warranty status for selected devices"
- "Compare selected devices"
- _Something else_

### 2.3 Clicking a suggestion

1. If the side panel is **closed**, it opens.
2. The suggestion is fired into the **existing active thread** in the panel (not a new thread).
3. The selected entity IDs (e.g. device IDs) are attached as context to the message.
4. The message displays in the panel with the suggestion text and the context chip (see §4).
5. The popup closes.

### 2.4 Clicking "Something else"

1. If the side panel is **closed**, it opens.
2. The panel's input bar gains focus, ready for the user to type.
3. A **context chip** (see §4) appears in or near the input area showing what context is attached (e.g. "3 devices selected"). The chip is dismissible.
4. The user types their own question. The selected entity IDs are included as context when the message is sent.
5. The popup closes.

### 2.5 Disabled state during active response

If the panel is currently processing a response (in-progress state), the "Ask IQ" popup suggestions are **disabled** (greyed out). On hover, a tooltip reads: "You can trigger once current response is fully generated."

Once the response completes, the suggestions become active again.

### 2.6 Pages with table-based "Ask IQ"

| Page | Selectable entities | Context payload |
|------|-------------------|-----------------|
| **Device Management > Devices** | Devices (rows) | Device IDs, device count |
| **Device Management > System Update** | Update packages (rows) | Package IDs, package count |
| **App Management > Apps** | Applications (rows) | App IDs, app count |
| **App Management > Patch** | Patches (rows) | Patch IDs, patch count |

Other table pages can be added incrementally. The pattern is the same: >1 row selected → popup with suggestions + "Something else".

---

## 3. "Ask IQ" on Dashboard Widgets

### 3.1 Trigger

Each dashboard widget on the Dashboard page gets a small **LITA icon** (AI sparkle or IT Assist brand icon) in the widget header or corner.

Dashboard widgets:
- Total Devices
- Device Connectivity
- Current Issue Summary
- System Update
- Overall Health Score

### 3.2 Clicking the widget LITA icon

1. An "Ask IQ" popup appears near the widget (or near the right panel area).
2. The popup shows **3 smart suggestions** matched from the prompt store based on the widget type and its data, plus **"Something else"**.
3. Clicking a suggestion or "Something else" behaves identically to the table-based "Ask IQ" (§2.3, §2.4).

### 3.3 Widget context payload

The context includes:
- **Widget type** (e.g. "Device Connectivity")
- **Widget data** (e.g. "Online: 319 (42.76%), Offline: 427 (57.24%)")

Example suggestions for the Device Connectivity widget:
- "Why are so many devices offline?"
- "Show me the list of offline devices"
- "Compare online vs offline device health"
- _Something else_

Example suggestions for the System Update widget:
- "Which devices have critical updates pending?"
- "How do I schedule these critical updates?"
- "Show update compliance trend"
- _Something else_

### 3.4 Disabled state

Same as table-based "Ask IQ" (§2.5). Suggestions disabled while panel is processing; tooltip on hover.

---

## 4. Context Chip

### 4.1 What it is

A visible indicator in or near the panel's input area showing that context is attached to the next message. It tells the user what data the chatbot will use.

### 4.2 Appearance

- A small chip/badge near the input bar (e.g. above the text input or inline).
- Format: "[icon] 3 devices selected" or "[icon] Device Connectivity widget"
- Dismissible: clicking the X on the chip removes the context. The user can then ask a general question without context.

### 4.3 Lifecycle

| Event | Context chip behaviour |
|-------|----------------------|
| User triggers "Ask IQ" with a suggestion | Chip appears with context, suggestion fires, chip clears after message is sent |
| User clicks "Something else" | Chip appears with context, stays visible until user sends a message or dismisses it |
| User sends a message with chip visible | Context is included in the message, chip clears |
| User dismisses the chip | Context is removed, user types without context |
| User navigates to another page with chip visible | Chip clears (context was specific to the previous page's selection/widget) |
| User deselects rows while chip is visible | Chip clears |

### 4.4 Per-message context display

When a message is sent with context, the message in the chat displays:
- The context label (same per-message label from Phase 1: "From: Device Management > Devices")
- Additionally, a context attachment indicator: e.g. "With: 3 devices (AHELSINGER, GYSCLUMY, JQARTSSR)" — shown as a subtle, collapsible detail below the message.

---

## 5. Context Injection (Backend)

### 5.1 What gets sent to the model

| Source | Context payload | Token budget |
|--------|----------------|-------------|
| **Table selection** | Entity type + entity IDs + count (e.g. `{type: "device", ids: ["DEV-001", "DEV-002", "DEV-003"], count: 3}`) | ~100–200 tokens |
| **Dashboard widget** | Widget type + key data points (e.g. `{widget: "Device Connectivity", data: {online: 319, offline: 427, online_pct: 42.76}}`) | ~100–150 tokens |
| **Page definition** | Page hierarchy (e.g. "Device Management > Devices") — already part of Phase 1 context labels | ~10–20 tokens |

For large selections (>20 entities), the context chip displays "20+" but the full selection identifiers are passed. The model already has schema access and generates GQL to resolve entity data as needed — this capability exists today and is not part of Phase 2 scope.

### 5.2 What does NOT get sent

- Unselected row data
- Data from other pages
- User PII

The model uses the entity IDs and its existing schema + GQL generation capability to look up full entity details.

### 5.3 Security considerations

- Context injection must respect the user's access control. Only data the user can already see is included.
- Entity IDs are scoped to the current tenant/organisation.
- Context payloads are not persisted beyond the thread lifecycle.
- Sanitise context before injection to prevent prompt injection attacks.

---

## 6. Smart Suggestion Matching

### 6.1 How suggestions are selected

The existing prompt store is used. Matching logic:

1. **Input signals:** Page definition + entity type (for selection) or widget type (for dashboard).
2. **Matching:** Semantic similarity search against the prompt store, filtered by entity type or widget type tags.
3. **Output:** Top 3 matching suggestions, ranked by relevance.

### 6.2 Prompt store requirements

- Prompts in the store must be **tagged** by relevant entity types (device, package, app, patch) and widget types (Device Connectivity, System Update, etc.).
- If no matching prompts are found for a given context, the "Ask IQ" popup shows only "Something else" (no suggestions).
- The prompt store tagging is configurable without code changes.

---

## 7. Requirements

| ID | Requirement |
|----|-------------|
| **REQ-18** | When the user selects more than 1 row on a supported data table, the system SHALL display an "Ask IQ" floating popup near the right edge of the viewport. |
| **REQ-19** | The "Ask IQ" popup SHALL show up to 3 smart suggestions from the prompt store (matched by page definition and entity type) plus an always-present "Something else" option. |
| **REQ-20** | Clicking a suggestion in the "Ask IQ" popup SHALL open the side panel (if closed) and fire the suggestion into the existing active thread with the selected entity IDs attached as context. |
| **REQ-21** | Clicking "Something else" SHALL open the side panel (if closed), focus the input bar, and display a context chip showing the attached context (e.g. "3 devices selected"). The chip SHALL be dismissible. |
| **REQ-22** | If the panel is processing a response, "Ask IQ" popup suggestions SHALL be disabled with a hover tooltip: "You can trigger once current response is fully generated." |
| **REQ-23** | Each dashboard widget SHALL display a LITA icon. Clicking the icon SHALL open an "Ask IQ" popup with up to 3 smart suggestions (matched by widget type and widget data) plus "Something else". |
| **REQ-24** | The context chip SHALL appear in or near the input area when context is attached. It SHALL display the context summary (e.g. "3 devices selected" or "Device Connectivity widget") and be dismissible. |
| **REQ-25** | The context chip SHALL clear when: the user sends a message, dismisses the chip, navigates to another page, or deselects the rows/widget. When the selection changes (rows added or removed), the chip SHALL update to reflect the new selection. |
| **REQ-26** | Messages sent with context SHALL include the entity IDs (or widget data) in the payload sent to the model. For selections exceeding 20 entities, all entity IDs are still passed; the context chip displays "20+" for readability. The model resolves full entity data via its existing schema and GQL generation capability. |
| **REQ-27** | Messages sent with context SHALL display a context attachment indicator in the chat (e.g. "With: 3 devices (AHELSINGER, GYSCLUMY, JQARTSSR)") as a collapsible detail below the message. |
| **REQ-28** | The prompt store SHALL support tagging prompts by entity type (device, package, app, patch) and widget type (Device Connectivity, System Update, etc.) for "Ask IQ" suggestion matching. |
| **REQ-29** | If no matching prompts are found in the store for a given context, the "Ask IQ" popup SHALL show only "Something else" (no suggestion slots). |
| **REQ-30** | Context injection SHALL respect user access controls — only data visible to the user is included. Context payloads SHALL be scoped to the current tenant and not persisted beyond the thread lifecycle. |
| **REQ-31** | The "Ask IQ" popup SHALL be dismissible by clicking outside it or deselecting rows/widget. |

### Requirements moved from Phase 1

| ID | Requirement | Origin |
|----|-------------|--------|
| **REQ-7** | The panel SHALL include a collapsed thread list that can be expanded to view and switch between recent threads. | Moved from Phase 1 — accessing historic threads from the right-side panel. |
| **REQ-8** | Full thread management (pin, rename, delete) SHALL remain available only in the full-page LITA view. The panel thread list is read-only for switching. | Moved from Phase 1. |
| **REQ-9** | The panel home screen SHALL display curated pre-canned prompts specific to the page type the user is currently on. | Moved from Phase 1 — complements "Ask IQ" by providing page-aware prompts when no selection/action has been made. |
| **REQ-10** | The page-specific prompt mapping SHALL be configurable without code changes (e.g. via a prompt catalogue or configuration file). | Moved from Phase 1. |
| **REQ-11** | If no page-specific prompts are configured for a page, the system SHALL fall back to the default global prompt set. | Moved from Phase 1. |

---

## 8. Out of Scope (Phase 2)

| Excluded | Rationale |
|----------|-----------|
| **GQL generation / data resolution** | The model already has schema access and generates GQL to resolve entity data. This is existing infrastructure, not Phase 2 scope. |
| **Context for pages without tables or widgets** | Phase 2 focuses on tables with row selection and dashboard widgets. Other pages use page-specific pre-canned prompts (REQ-9/10/11, moved from Phase 1 to Phase 2). |
| **Personalised suggestion matching** | Separate feature. Prompt store matching is semantic, not personalised to user history. |
| **Dynamic "Summarise this page"** | Phase 1 covers page-specific prompts including summarise-style prompts. Phase 2 does not change home screen behaviour. |
| **Context persistence across threads** | Context is per-message. It does not carry over to subsequent messages unless the user triggers "Ask IQ" again. |
| **"Ask IQ" on single row selection** | Trigger threshold is >1 row. Single row selection does not trigger the popup. |

---

## 9. NFRs

| ID | Requirement | Rationale |
|----|-------------|-----------|
| **NFR-7** | The "Ask IQ" popup SHALL appear within 500ms of the selection exceeding 1 row. | Immediate feedback to high-intent user action. |

---

## 10. Key Design Decisions & Rationale

| Decision | Choice | Why |
|----------|--------|-----|
| Popup vs action bar button | **Popup** (Rufus-style, near right panel) | Higher discoverability at high-intent moments. Positioned less intrusively than center-screen. |
| Trigger threshold | **>1 row selected** | Avoids popup fatigue on single-click. Multi-select signals higher intent. |
| Fire into existing thread vs new thread | **Existing thread** | Avoids noisy thread creation. Historic threads are visible in full-page LITA — too many auto-created threads would clutter. |
| Context chip (visible, dismissible) | **Yes** | Transparency — user knows what context is attached and can remove it. |
| Entity IDs in payload, model resolves via GQL | **Yes** | Keeps token budget low. Model already has schema + GQL capability to fetch full data when needed. |
| Dashboard widget LITA icons | **Yes** | Surfaces AI at widget-level intent moments without requiring row selection. |

---

## 11. Success Metrics

| Metric | What it tells you |
|--------|-------------------|
| **"Ask IQ" trigger rate** | How often do users see the popup (selection > 1 row)? |
| **"Ask IQ" click-through rate** | Of those who see it, how many click a suggestion or "Something else"? |
| **Suggestion vs "Something else" ratio** | Are the smart suggestions relevant enough, or do users mostly click "Something else"? |
| **Dashboard widget "Ask IQ" usage** | Which widgets drive the most "Ask IQ" interactions? |
| **Context chip dismissal rate** | How often do users dismiss context? (High dismissal = context not useful or unwanted.) |
| **Response quality with context vs without** | Compare thumbs up/down rates for context-attached messages vs general messages. |

---

*Phase 2 research complete. DA feedback applied. Ready for Confluence, stories, and Jira.*
