# Embedded Panel Chatbot — Combined Bolt Prompt (Phase 1 + Phase 2)

Paste this into bolt.new to add the embedded right-side panel chatbot with context-aware "Ask IQ" features on top of the existing Lenovo IT Assist base application.

---

## Existing Application (do not rebuild)

The application is **Lenovo IT Assist**, an enterprise Gen AI chatbot for IT Admins within the **Lenovo Device Orchestration** platform. It already has: a dark sidebar with thread list (Pinned/Recent threads, Deployment assistant), a main chat area, top nav with product switcher/breadcrumb/search/notifications/user avatar, chatbot home page with 5+ prompt tiles, response anatomy (timestamp, reasoning toggle, body, thumbs up/down, recommendations), in-progress state ("Processing your request…" + stop button), and an input bar with Explore/Favourite prompts. Tech stack: **React + Tailwind CSS + Vite**. All of this exists and must not be rebuilt or modified.

---

## ADD THE FOLLOWING FEATURES

### Feature 1: Right-Side Panel Chatbot (Phase 1)

Add an embedded chatbot panel that slides in from the right side of every page.

#### 1.1 Entry Point — Top-Nav Button

- Add a persistent **IT Assist button** in the top navigation bar, positioned near the notification bell icon on the right.
- The button uses the IT Assist / IQ branding icon (purple AI sparkle icon).
- Tooltip on hover: "Open Lenovo IT Assist".
- The button appears on **every page** in the platform (Dashboard, Device Management, Device Insights, Support Tickets, Configurations & Settings, Reports, App Management).
- **Exception:** When the user is on the full-page LITA (the existing chatbot page), hide or disable this button — the chatbot is already in full view.

#### 1.2 First-Use Onboarding Cue

- On the first time a user sees the button (simulated with a state flag), show a **one-time onboarding cue**: a pulsing animation on the button + a tooltip callout: "AI assistance is now available from any page. Click to try it."
- The cue dismisses when clicked or when the user opens the panel. It never appears again after dismissal.

#### 1.3 Panel Open / Close Behaviour

- **Open:** Clicking the top-nav button slides the panel in from the right. The page content **pushes left** (not overlay). The panel is ~380–420px wide, full viewport height below the top nav.
- **Close:** Clicking the top-nav button again, or clicking the **X close icon** in the panel header, slides the panel out. Page content shifts back to full width.
- **Animation:** Smooth slide-in/out, ≤300ms. Page content animates simultaneously.
- **On page navigation:** The panel **stays open**. The conversation persists. The user closes it explicitly.
- **Lazy loading:** The panel shell (button) renders with the page. The chat engine, threads, and prompts load only on first open. Simulate this with a brief loading spinner on first open.

#### 1.4 Panel Anatomy

**Header (top of panel):**
- IT Assist branding icon + "Lenovo IT Assist" label.
- **"Open full view"** icon/link — when clicked, navigates to the full-page LITA showing the same active thread.
- **"+" button** — creates a new thread (closes the current thread, starts a fresh one). Behaviour matches the existing "+" in the full-page sidebar.
- **Close button (X icon)** — closes the panel.

**Chat area (main body):**
- If a persisted thread exists: show the thread conversation. Each **user message** displays a **context label** — a small tag below the message text showing which page it was sent from. Format: "From: Dashboard" or "From: Device Management > Devices". This is **per-message**, not per-thread.
- If no thread exists (first use or after "+"): show the **home screen** — the same default prompt tiles as the full-page chatbot (e.g. "How many expired warranties are in my fleet?", "Show me a list of devices that are online and pending critical updates").
- All chatbot capabilities work in the panel: KB Q&A (text + images + tables), Data insights (text + charts), Actions, Reasoning toggle, Smart suggestions/recommendations, Thumbs up/down, In-progress state with stop/cancel.

**Input bar (footer):**
- Same as the full-page chatbot: text input, Explore button, Favourite prompts button, Send button (paper plane) / Stop button (red circle) when processing.
- Disclaimer text below: "Lenovo IT Assist uses AI. Please double-check results."

#### 1.5 Rich Content in Panel

- Charts and visualisations must adapt to the panel's narrower width (~380–420px) — use adjusted aspect ratios.
- Wide data tables get **horizontal scroll** within the panel.
- Images scale to fit panel width.

#### 1.6 Responsive Behaviour

- On viewports **<1024px wide**, the panel opens as an **overlay** (full-width) instead of push. Page content does not shift.
- On viewports ≥1024px, the push layout is used.

#### 1.7 Thread Behaviour

- When opened, the panel shows the **most recent active thread**.
- Thread persists across close/reopen and across page navigations.
- The "+" button creates a new thread; the old thread appears in the full-page LITA's thread history.

---

### Feature 2: "Ask IQ" Context-Aware Triggers (Phase 2)

Add context-aware AI triggers that surface an "Ask IQ" popup when users select table rows or interact with dashboard widgets.

#### 2.1 "Ask IQ" on Data Tables

**Trigger:** When the user selects **more than 1 row** on any page that has a data table, show an **"Ask IQ" floating popup**.

- **Popup style:** Small floating card near the right edge of the viewport (near where the panel opens). Not center-screen. Similar to Amazon Rufus style.
- **Popup content:** Up to **3 smart suggestions** (text labels) + a **"Something else"** option always at the bottom.
- **Dismissible:** Clicking outside the popup or deselecting rows closes it.
- **Appears within 500ms** of the second row being selected.

**Prototype data — example suggestions for Device Management > Devices:**
- "Run a system scan on selected devices"
- "Show warranty status for selected devices"
- "Compare selected devices"
- _Something else_

**Prototype data — example suggestions for App Management > Patch:**
- "Show patch compliance for selected patches"
- "Which devices are missing these patches?"
- "Schedule deployment for selected patches"
- _Something else_

**Clicking a suggestion:**
1. Opens the side panel (if closed).
2. Fires the suggestion text as a message in the **existing active thread** (or creates a new thread if on the home screen).
3. The message shows a **context attachment indicator** below it: "With: 3 devices (LENOVO-LAPTOP-001, DELL-WORKSTATION-042, HP-PROBOOK-089)" — collapsible.
4. The popup closes.

**Clicking "Something else":**
1. Opens the side panel (if closed).
2. Input bar gains focus.
3. A **context chip** appears near the input bar: "[AI icon] 3 devices selected [X]". The X dismisses the chip (removes context).
4. User types their own question. When sent, entity IDs are included as context. The context chip clears after sending.

**Disabled state:** If the panel is processing a response, all popup suggestions are **greyed out**. Tooltip on hover: "You can trigger once current response is fully generated." Suggestions re-enable when the response completes.

#### 2.2 "Ask IQ" on Dashboard Widgets

Each dashboard widget gets a small **LITA icon** (AI sparkle) in its header or corner.

**Dashboard widgets to add the icon to:**
- Total Devices
- Device Connectivity
- Current Issue Summary
- System Update
- Overall Health Score

**Clicking the LITA icon:** Opens an "Ask IQ" popup (same style as the table popup) with 3 suggestions matched to the widget + "Something else".

**Prototype data — example suggestions for Device Connectivity widget:**
- "Why are so many devices offline?"
- "Show me the list of offline devices"
- "Compare online vs offline device health"
- _Something else_

**Prototype data — example suggestions for System Update widget:**
- "Which devices have critical updates pending?"
- "How do I schedule these critical updates?"
- "Show update compliance trend"
- _Something else_

Clicking a suggestion or "Something else" behaves identically to the table-based "Ask IQ" — opens panel, fires into active thread or shows context chip.

**Widget context chip:** Shows e.g. "Device Connectivity widget" instead of row count.

#### 2.3 Context Chip

A visible chip/badge near the input bar when context is attached.

**Appearance:** Small pill with icon + text + dismiss X. Examples:
- "[AI icon] 3 devices selected [X]"
- "[AI icon] Device Connectivity widget [X]"
- "[AI icon] 20+ devices selected [X]" (for selections >20)

**Lifecycle:**
| Event | Chip Behaviour |
|-------|---------------|
| Suggestion clicked | Chip appears → message fires → chip clears after send |
| "Something else" clicked | Chip appears → stays until user sends or dismisses |
| Message sent with chip | Context included → chip clears |
| Chip X clicked | Context removed, user types without context |
| Navigate to another page | Chip clears |
| Deselect rows | Chip clears |
| Selection changes (add/remove rows) | Chip updates (e.g. "3 devices" → "5 devices") |

#### 2.4 Per-Message Context Display

Messages sent with context show **two indicators:**
1. **Phase 1 page label:** "From: Device Management > Devices" (always present on every user message).
2. **Context attachment indicator** (Phase 2): "With: 3 devices (LENOVO-LAPTOP-001, DELL-WORKSTATION-042, HP-PROBOOK-089)" — shown as a collapsible detail below the message. Click to expand/collapse.

Messages sent **without** "Ask IQ" context show only the Phase 1 page label, no attachment indicator.

#### 2.5 Thread List in Panel

Add a **thread list toggle** in the panel header (e.g. hamburger or thread icon).

- **Default:** Collapsed (thread list hidden).
- **Click to expand:** Shows recent threads within the panel — each row has thread title + timestamp.
- **Click a thread:** Switches to that thread. Thread list collapses.
- **No management actions:** No pin, rename, or delete in the panel. Those stay in the full-page LITA only.

#### 2.6 Page-Specific Pre-Canned Prompts on Home Screen

When the panel shows the **home screen** (no active thread or after "+"), display **page-specific prompts** instead of always showing the same global set.

**Prototype data — prompts by page:**

| Page | Prompts |
|------|---------|
| Dashboard | "How many devices are offline right now?", "Explain the overall health score", "Summarise my fleet status" |
| Device Management > Devices | "What devices have expiring warranties?", "How do I export my device list?", "Summarise device health" |
| Device Management > System Update | "Which updates are critical?", "How do I schedule updates?", "Summarise update compliance" |
| App Management > Apps | "How do I deploy an app to a group?", "Which apps have the most installs?", "Summarise app deployment status" |
| App Management > Patch | "Which patches are pending?", "Show patch compliance", "Summarise patch status" |
| *(fallback for any other page)* | Use the default global prompt tiles (same as the existing home screen) |

Prompts update when the user navigates to a different page while the home screen is visible.

---

## PROTOTYPE INTERACTIONS TO WIRE UP

Build these end-to-end flows so a PM can demo the feature:

1. **Open panel → see persisted thread → send a message → see response with context label + reasoning + recommendations → close panel.** The thread persists if reopened.

2. **Navigate to Device Management > Devices → select 3 devices → "Ask IQ" popup appears → click a suggestion → panel opens → suggestion fires as a message with context attachment indicator → mock AI response appears.**

3. **Select devices → "Ask IQ" popup → click "Something else" → panel opens with context chip → type a question → send → context chip clears → mock response with context indicator.**

4. **Dashboard → click LITA icon on Device Connectivity widget → "Ask IQ" popup → click suggestion → panel opens → fires into thread with widget context.**

5. **Panel home screen → navigate between pages → home screen prompts change to match the page.**

6. **Panel header → click thread list toggle → expand thread list → click a different thread → panel switches.**

7. **Panel header → click "+" → new thread starts → old thread appears in thread list.**

8. **Panel header → click "open full view" → navigate to full-page LITA showing the active thread.**

9. **First-use onboarding cue → pulse on button → click to open → cue dismissed forever.**

10. **Viewport <1024px → open panel → panel opens as overlay, not push.**

---

## MOCK DATA

Use realistic IT fleet data throughout. **No lorem ipsum.**

**Devices:** LENOVO-LAPTOP-001, DELL-WORKSTATION-042, HP-PROBOOK-089, LENOVO-THINKPAD-X1C-007, HP-ELITEBOOK-055  
**Fleet stats:** 746 total, 319 online (42.76%), 427 offline (57.24%)  
**Warranties:** 3 expiring in 30 days  
**Updates:** Critical (68), Recommended (152), Optional (58)  
**Health score:** 92  
**Device groups:** North Room, South Room, DV_Group 1, DV_Group 2  
**Apps:** Lenovo System Update, Lenovo Vantage, Microsoft Teams, Zoom Client  
**Patches:** KB5034441, KB5035845, KB5036892  
**Thread names:** "Application Deployment Steps", "BSOD events timeline chart (90 days)", "Warranties Expiring Soon", "Critical Updates Count"

**Mock AI responses:**
- For "Show warranty status for selected devices": Return a data table with Device Name, Warranty Start, Warranty End, Status columns.
- For "Why are so many devices offline?": Return a paragraph + a bar chart breaking offline by device group.
- For "Run a system scan on selected devices": Return an action confirmation message with a progress indicator.
- For any other prompt: Return a realistic text response with recommendations.

---

## DO NOT MODIFY

**Explicitly:** Do not remove, break, or simplify any of the following existing features:

- KB Q&A capability (text + images + tables)
- Data insights capability (text + charts + visualisations)
- Actions capability (device actions from chat)
- Agentic workflows (plan-and-execute flows)
- Thread sidebar (Deployment assistant, Pinned threads, Recent threads)
- Thread actions in sidebar (Rename, Pin, Delete via 3-dot menu)
- Reasoning toggle (Show/Hide reasoning)
- Thumbs up / thumbs down feedback
- Recommendations card (follow-up suggestions)
- In-progress state ("Processing your request…" + stop button)
- Input bar (Explore, Favourite prompts, Send, disclaimer)
- Top nav (logo, product switcher, breadcrumb, search, help, notifications, user avatar)
- Chatbot home page with prompt tiles

Only **add** the features described above. Keep all existing screens, components, and interactions intact.

---

## QUALITY INSTRUCTIONS

- Use clean, reusable React components. Suggested component structure:
  - `TopNavButton` — the IT Assist button in the top nav
  - `SidePanel` — the sliding panel container
  - `PanelHeader` — branding, full-view link, "+" button, thread list toggle, close button
  - `ThreadListDropdown` — collapsible thread list within the panel
  - `ChatArea` — messages, context labels, context indicators
  - `ContextChip` — the dismissible context badge near input bar
  - `AskIQPopup` — the floating "Ask IQ" card (reusable for tables and widgets)
  - `WidgetLitaIcon` — the LITA icon overlay on dashboard widgets
  - `OnboardingCue` — first-use pulse/tooltip on the top nav button
  - `PagePrompts` — page-specific pre-canned prompts config and display

- Use **Tailwind CSS** for all styling. Enterprise feel: professional, minimal, clean.
- Colours: Match the existing application palette (purple/indigo primary, dark navy sidebar, white backgrounds, blue-green for online/success, red for offline/critical).
- Animations: `transition-all duration-300` for panel slide. `transition-opacity duration-200` for popup fade.
- Make the prototype **interactive enough to demonstrate every flow** end-to-end. All buttons, suggestions, popup triggers, chip interactions, and thread switching should work.
- Use simulated delays (500–1500ms) for AI response generation to show the in-progress state.
