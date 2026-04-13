# Embedded Panel Chatbot — Feature Research

**Feature:** Right-side panel chatbot accessible from every screen in Lenovo Device Orchestration.

**Phasing:** This document covers **Phase 1** (embedded panel, no context awareness). Phase 2 (context-aware AI, "Ask IQ" triggers) will be defined separately.

---

## 1. Problem Statement

### Why usage is low

Lenovo IT Assist is a Gen AI chatbot for IT Admins, housed within the Lenovo Device Orchestration platform. Today the chatbot lives on a **dedicated page** — users must navigate to it via a dropdown in the platform nav. This creates two barriers:

1. **Workflow interrupt.** IT Admins spend most of their time on Device Management, Dashboard, System Update, and other operational pages. Switching to the chatbot means leaving their working context, asking a question, and then navigating back. This friction discourages casual or quick use.
2. **Low discoverability.** The chatbot is one option in a dropdown alongside Dashboard, Device Management, Device Insights, Support Tickets, and Configurations & Settings. There is no persistent visual cue that AI assistance is available while the user works on other pages.

### Industry evidence

Embedded AI assistants consistently outperform standalone pages for adoption:

- **Microsoft 365 Copilot** — sidebar panel on every app (Word, Excel, Teams). Available where the user works.
- **Salesforce Einstein Copilot** — persistent side panel within CRM screens.
- **Zendesk, Figma, Notion, Adobe** — all use right-side or floating panel patterns for AI assistance.
- **GitHub Copilot Chat** — side panel within the IDE, not a separate application.

Tools that force users to leave their workflow see lower adoption. A chatbot behind a dropdown is a workflow interrupt.

### Scope of this solution

Phase 1 addresses the **discoverability and access friction** problem only. It does not address other potential usage barriers (answer quality, trust, personalisation). The hypothesis: if users can access the chatbot without leaving their current page, usage will increase. This should be validated with before/after measurement.

---

## 2. Solution: Right-Side Panel Chatbot

### 2.1 Entry point

A dedicated **button in the platform's top navigation bar**, positioned near the bell/notification icon on the right side. This placement ensures:

- Visibility on every screen without consuming content area space.
- Consistency — the button is always in the same location regardless of which page the user is on.
- Familiarity — follows the same pattern as notification/help icons in enterprise platforms.

The button should use the IT Assist / IQ branding icon. A tooltip on hover: "Open Lenovo IT Assist".

### 2.2 Panel behaviour

| Aspect | Behaviour |
|--------|-----------|
| **Default state** | Closed. The button is always visible; the panel is not. |
| **Open trigger** | Click the top-nav button. |
| **Close trigger** | Click the button again, or click a close icon on the panel header. |
| **Layout** | Push — the page content shifts left to accommodate the panel. The panel does not overlay content. |
| **Panel position** | Right side of the viewport, full height below the top nav bar. |
| **Panel width** | Fixed width (~380–420px). Not user-resizable in Phase 1. |
| **Animation** | Smooth slide-in from the right; page content animates left simultaneously. |
| **On page navigation** | Panel stays open. The user's conversation persists and the panel remains visible across page changes. User closes explicitly when done. |
| **Lazy loading** | Panel shell (button, header) loads with the page. Chat engine, thread data, and prompts load only when the panel is first opened. |

### 2.3 Panel anatomy

The panel consists of three areas:

**Header:**
- IT Assist branding/icon and label ("Lenovo IT Assist" or "IQ").
- "Open full view" icon/link — navigates to the full-page LITA experience, opening the user's currently active thread.
- "+" button — creates a new thread (closes current thread, starts a new one, maintaining existing behaviour from full-screen LITA).
- Close button (X icon).

**Chat area (main body):**
- If a persisted thread exists: shows the thread conversation. Each message displays a **context label** indicating which page it was sent from (e.g. "From: Dashboard" or "From: Device Management > Devices"). This is per-message, not per-thread, so the user can see how the conversation spanned pages.
- If no thread exists (first use or after starting a new thread): shows the **home screen** with default prompts (page-specific prompts deferred to Phase 2).
- Message bubbles, reasoning toggle, smart suggestions, and response feedback (thumbs up/down) — all capabilities from the full-page chatbot are available.

**Input bar (footer):**
- Text input with send button.
- Explore and Favourite prompts buttons (same as current full-page chatbot).
- Stop/cancel button during processing.

### 2.4 Thread management

| Behaviour | Detail |
|-----------|--------|
| **Thread persistence** | When the user opens the panel, it shows the **most recent active thread**. The thread persists across panel close/reopen, including across different pages. |
| **Context label** | Each user message displays a per-message label showing which page the prompt was sent from (e.g. "From: Device Management > Devices"). This keeps context accurate even when a single thread spans multiple pages. |
| **New thread ("+" button)** | A "+" button in the panel header closes the current thread and starts a new one (maintaining existing new-thread behaviour from full-screen LITA). |
| **Thread list in panel** | Deferred to Phase 2. Accessing historic threads from the right-side panel will be addressed in Phase 2. |
| **Full-page LITA** | Remains accessible via: (1) the dropdown nav, and (2) the "open full view" link in the panel header. When opened from the panel, it navigates to the currently active thread. |

### 2.5 ~~Page-specific pre-canned prompts~~ — Deferred to Phase 2

Page-specific pre-canned prompts have been moved to Phase 2 scope, where they are covered by the "Ask IQ" context-aware smart suggestions feature. In Phase 1, the home screen shows the **default global prompt set** (same as today's chatbot home page).

### 2.6 Capability parity

The panel chatbot supports **all capabilities** available in the full-page chatbot:

- KB Q&A (text, images, data tables)
- Data insights (text, charts, visualisations)
- Actions (system scan, system update, device onboarding, etc.)
- Reasoning toggle (show/hide)
- Smart suggestions / recommendations
- Response feedback (thumbs up/down)
- Explore and Favourite prompts
- In-progress state with stop/cancel

**Note on rich content:** Charts, data tables, and images must render correctly within the panel's narrower width (~380–420px). This may require responsive adaptations (e.g. horizontal scroll for wide tables, chart aspect ratio adjustments).

### 2.7 Responsive considerations

- **Dense data pages (e.g. Device Management > Devices):** The push behaviour reduces available width for the data table. The table should either horizontally scroll or hide lower-priority columns. This is acceptable — the user has explicitly chosen to open the panel and can close it to reclaim space.
- **Narrow viewports / smaller screens:** If the viewport is below a minimum threshold (e.g. <1024px), consider opening the panel as a full-width overlay instead of push, to avoid unusable content area. Define the threshold based on testing.
- **Full-page LITA:** When the user is already on the full-page Lenovo IT Assist, the top-nav button should be hidden or disabled (the chatbot is already in full view).

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| **REQ-PANEL-01** | The platform SHALL display a persistent IT Assist button in the top navigation bar on every screen in Lenovo Device Orchestration. |
| **REQ-PANEL-02** | Clicking the top-nav button SHALL open a right-side panel chatbot that pushes the page content to the left. |
| **REQ-PANEL-03** | The panel SHALL close when the user clicks the close button or clicks the top-nav button again. The panel SHALL remain open when the user navigates to a different page. |
| **REQ-PANEL-04** | The panel SHALL show the user's most recent active thread when opened. Each user message SHALL display a per-message context label indicating which page it was sent from (e.g. "From: Device Management > Devices"). |
| **REQ-PANEL-05** | The panel header SHALL include a "+" button that closes the current thread and starts a new one (maintaining existing new-thread behaviour from full-screen LITA). |
| **REQ-PANEL-06** | The panel header SHALL include a link/icon to open the full-page LITA view, navigating to the currently active thread. |
| ~~**REQ-PANEL-07**~~ | ~~Thread list in panel~~ — Moved to Phase 2. |
| ~~**REQ-PANEL-08**~~ | ~~Thread management in full-page only~~ — Moved to Phase 2. |
| ~~**REQ-PANEL-09**~~ | ~~Page-specific prompts~~ — Removed (covered in Phase 2). |
| ~~**REQ-PANEL-10**~~ | ~~Configurable prompt mapping~~ — Removed (covered in Phase 2). |
| ~~**REQ-PANEL-11**~~ | ~~Fallback to global prompts~~ — Removed (covered in Phase 2). |
| **REQ-PANEL-12** | The panel chatbot SHALL support all capabilities available in the full-page chatbot: KB Q&A, Data insights, Actions, Reasoning toggle, Smart suggestions, Response feedback, Explore/Favourite prompts, In-progress state with stop/cancel. |
| **REQ-PANEL-13** | Rich content (charts, data tables, images) SHALL render correctly within the panel's width, with responsive adaptations as needed (e.g. horizontal scroll, aspect ratio adjustment). |
| **REQ-PANEL-14** | The panel and chat engine SHALL be lazy-loaded — only initialised when the user first opens the panel. |
| **REQ-PANEL-15** | The full-page Lenovo IT Assist page SHALL remain accessible via the platform dropdown navigation and via the panel's "open full view" link. |
| **REQ-PANEL-16** | When the user is already on the full-page LITA, the top-nav panel button SHALL be hidden or disabled to avoid redundancy. |
| **REQ-PANEL-17** | On first use (first time the panel button appears for a user), the system SHALL display a one-time onboarding cue (e.g. tooltip, callout, or pulse animation on the button) to inform the user that AI assistance is available from any page. The cue SHALL be dismissible and not shown again after dismissal or first panel open. |

---

## 4. Out of Scope (Phase 1)

| Excluded | Rationale |
|----------|-----------|
| **Page context injection** | Phase 2. Panel does not pass page data (selected devices, filters, current records) to the chatbot. |
| **"Ask IQ" contextual popup** | Phase 2. No popup on row selection or other in-page interactions. |
| **Personalised suggestions** | Separate feature. Recommendations remain non-personalised (semantic match against prompt store). |
| **Proactive notifications** | Separate feature. No system-triggered AI prompts. |
| **Resizable panel** | Not in Phase 1. Fixed width. |
| **Panel on mobile / tablet** | Phase 1 targets desktop viewports. Mobile/tablet may be addressed later. |
| **Thread management in panel** | Panel shows a read-only thread list for switching. Pin, rename, delete remain in full-page view only. |
| **Keyboard shortcut to open panel** | Can be added later. Phase 1 uses button click only. |

---

## 5. NFRs

| ID | Requirement | Rationale |
|----|-------------|-----------|
| **NFR-1** | Panel open/close animation SHALL complete in ≤300ms. | Snappy feel; avoid sluggish transitions. |
| **NFR-2** | Lazy loading of the chat engine SHALL complete in ≤2s on first open (P95, standard enterprise network). | Users should not wait long after clicking the button. |
| **NFR-3** | Opening the panel SHALL NOT increase the initial page load time of any platform page. | Lazy loading ensures zero cost until interaction. |
| ~~**NFR-4**~~ | ~~WCAG 2.1 AA accessibility~~ — Removed from Phase 1 scope. |
| **NFR-5** | The panel SHALL work correctly on viewports ≥1024px wide. Below this threshold, the panel MAY use overlay mode instead of push. | Ensures usability on standard enterprise monitors without breaking dense pages. |
| ~~**NFR-6**~~ | ~~Prompt catalogue updatable without redeployment~~ — Removed (page-specific prompts deferred to Phase 2). |

---

## 6. Key Design Decisions & Rationale

| Decision | Choice | Why |
|----------|--------|-----|
| Push vs overlay | **Push** | User can see both page content and chatbot simultaneously; overlay hides content and feels temporary. |
| Panel stays open on navigation | **Yes** | Avoids reopen friction when users work across multiple pages. Per-message context labels keep the conversation clear. User closes explicitly when done. |
| Thread persists across pages | **Yes** | Users don't lose their conversation when they navigate; context labels help them track origin. |
| Full-page LITA remains | **Yes** | Power users and thread management need more space; panel is for quick access, full page for deep work. |
| Page-specific prompts (generic) | **Phase 1** | Low effort, high value — guides users toward relevant prompts without needing context injection. |
| Context-aware prompts & injection | **Phase 2** | Requires backend work to pass page state to the model; deferred to validate panel usage first. |

---

## 7. Success Metrics

Measure before and after Phase 1 rollout:

| Metric | What it tells you |
|--------|-------------------|
| **Chatbot sessions per user per week** | Are more users engaging now that the panel is on every page? |
| **Pages from which panel is opened** | Which pages drive the most chatbot usage? (Informs Phase 2 prioritisation.) |
| **Session depth** (messages per session) | Are users having meaningful conversations or just opening and closing? |
| **Return rate** | Do users who try the panel come back? (If not, the problem may be value/quality, not access.) |
| **Full-page LITA usage** | Does full-page usage decline, stay flat, or increase? (Panel may be a gateway to deeper use.) |
| **Time to first prompt** | How quickly after opening the panel does the user send a message? (Pre-canned prompts should reduce this.) |

---

*Phase 1 research complete. Awaiting user review before proceeding to Phase 2 definition or Devil's Advocate.*
