# Lenovo IT Assist — Base Application (bolt.new)

Build a full prototype of **Lenovo IT Assist**, a Gen AI chatbot for IT Administrators, housed within the **Lenovo Device Orchestration** platform. This is an enterprise-grade fleet management application. Use **React + Tailwind CSS + Vite**. Clean, component-based structure. No backend required for the prototype.

---

## 1. App Overview

**Lenovo IT Assist** is a generative AI chatbot designed for IT Admins managing device fleets. It lives within the broader **Lenovo Device Orchestration** platform, which includes Dashboard, Device Management, Device Insights, Lenovo IT Assist, Support Tickets, and Configurations & Settings. The chatbot provides how-to answers, fleet analytics, device actions, and agentic workflows. The UI must feel professional, minimal, and enterprise-grade.

---

## 2. Color Palette

Extract and use these colors consistently:

| Use | Color |
|-----|-------|
| **Primary / Brand** | Purple/indigo (#4F46E5 or similar) — Lenovo logo, active states, notification badges |
| **Backgrounds** | White (#FFFFFF) for main content; very light grey for cards if needed |
| **Sidebar** | Dark grey / navy (#1E293B or similar) — fixed left panel |
| **Sidebar text** | White or light grey for headers and items |
| **Active / Online** | Blue-green (#10B981 or similar) — success, online status |
| **Offline / Critical** | Red or orange (#EF4444, #F97316) — offline, critical updates |
| **Secondary text** | Grey (#6B7280, #9CA3AF) — timestamps, placeholders, disclaimers |
| **User chat bubble** | Light blue (#E0E7FF or similar) |
| **AI response bubble** | White with subtle border |

---

## 3. Layout

**Two-panel layout:**

- **Left sidebar:** Fixed width ~260px, dark navy background. Contains thread management.
- **Main chat area:** Flex, takes remaining width. White background. Scrollable.

**Top navigation bar** (spans full width, sticky):

- **Left:** Lenovo Device Orchestration logo (purple text + icon)
- **Product switcher dropdown:** Shows "Lenovo IT Assist" with gear icon; options: Dashboard, Device Management, Device Insights, Lenovo IT Assist, Support Tickets, Configurations & Settings
- **Breadcrumb:** "Home / Lenovo IT Assist"
- **Right:** Search bar (magnifying glass, "Search" placeholder), help icon (question mark in circle), history/clock icon, notification bell (with optional badge), user avatar ("DV Organization Admin" with dropdown)

---

## 4. Sidebar Contents

**Header:**
- "Lenovo IT Assist" title (white)
- "+" button (top right) — creates new thread

**Collapsible sections** (each with expand/collapse arrow):

1. **Deployment assistant** — collapsible, with "+" to create
2. **Pinned threads** — collapsible
3. **Recent threads** — collapsible

**Thread list** (under Recent threads, and Pinned when pinned):
- Each row: chat icon (speech bubble) | thread name | 3-dot menu
- 3-dot menu options: **Rename thread**, **Pin thread**, **Delete thread**
- Selected thread: light blue-grey background
- "Show more" link at bottom if many threads

**Example thread names:**
- Application Deployment Steps
- BSOD events timeline chart (90 days)
- Warranties Expiring Soon
- Demo thread
- New thread on 01/07/26 12:11 PM
- Critical Updates Count
- Oldest Windows Version on Network

---

## 5. Chatbot Home Page (Empty State)

When no thread is selected or thread is empty:

- **Centered AI icon/logo** (purple intertwined shapes, same as product switcher)
- **Heading:** "How may I assist you today?"
- **5 suggested prompt tiles** in a grid:
  1. "How many expired warranties are in my fleet?"
  2. "Show me a list of devices that are online and pending critical updates"
  3. "How can I deploy an application to a device?"
  4. "Generate a table showing device_ids with poor battery status and over 50% capacity and warranty about to expire"
  5. "Show me the list of devices with storage drives that are running low on space"
- **Sixth tile:** "Explore more ways to interact with Lenovo IT Assist →" (with arrow)
- **Input bar** at bottom (see section 9)

---

## 6. Base Chatbot Capabilities — Always Protect

These four capabilities must exist and work in the prototype. **Never remove or break them.**

1. **KB Q&A** — How-to question-and-answer. Responses include text, images, and data tables.
2. **Data insights** — Fleet analytics and reporting. Responses include text, charts, and visualisations.
3. **Actions** — Device actions from chat (e.g. system scan, system update, device onboarding).
4. **Agentic workflows** — Plan-and-execute flows (single or multi-step).

For the prototype, use **mock responses** that demonstrate each type:
- **KB:** Step-by-step text + image (e.g. QR code for onboarding)
- **Data insights:** Text + pie chart or bar chart (e.g. "Device Groups Distribution in Fleet")
- **Actions:** Text + action buttons (e.g. "Download", "Complete")
- **Agentic:** Multi-step flow UI (e.g. deployment assistant)

---

## 7. Response Anatomy (Any AI Response)

Each AI response must include:

1. **Timestamp** — e.g. "7:45 PM" (grey text)
2. **"Show reasoning ▼" toggle** — Collapsed by default. Click expands to show chain-of-thought reasoning text inline above the main response. When expanded, label changes to "Hide reasoning ▲"
3. **Response body** — Text, image, chart, or table depending on query type
4. **Feedback row** — Thumbs up, thumbs down, bookmark/favourite star (below response)
5. **Recommendations card** — Title "Recommendations", 2–3 follow-up prompt suggestions as clickable rows, each with AI spark icon on the left. Examples:
   - "Show me a pie chart of my fleet divided by device category"
   - "How can I create and manage device groups in my organization?"

User messages: right-aligned, light blue bubble, timestamp, optional star (favourite).

---

## 8. In-Progress State

When the AI is "generating" a response:

- **Text:** "Processing your request…" with animated dots or spinner (and optional gear icon)
- **Input bar:** Send button is **replaced** by a **stop button** — red circle with white square icon. Click to cancel.

---

## 9. Input Bar (Bottom, Sticky)

- **Placeholder:** "Ask Lenovo IT Assist a question…"
- **Left:** "Explore" button (grid icon), "Favorite prompts" button (star icon)
- **Right:** Send button (paper plane icon) — or stop button when processing (see section 8)
- **Below bar:** Small grey text — "Lenovo IT Assist uses AI. Please double-check results."

---

## 10. Do Not Modify Guard

**Explicit instruction:** Do not remove, break, or simplify:

- KB Q&A capability
- Data insights capability
- Actions capability
- Agentic workflows capability
- Thread sidebar (Deployment assistant, Pinned threads, Recent threads)
- Thread actions (Rename, Pin, Delete)
- Reasoning toggle (Show/Hide reasoning)
- Thumbs up / thumbs down feedback
- Recommendations card

---

## 11. Realistic IT Admin Data

Use realistic fleet management data throughout. **No lorem ipsum.**

**Examples:**
- Device names: LENOVO-LAPTOP-001, DELL-WORKSTATION-042, HP-PROBOOK-089
- Fleet stats: 746 total devices, 42.76% online (319), 57.24% offline (427)
- Warranty: "3 devices with warranties expiring in 30 days"
- Updates: Critical (68), Recommended (152), Optional (58)
- Device groups: North Room, South Room, DV_Group 1, DV_Group 2, DV_Group 3
- Health score: 92
- Issue summary: BSOD, High CPU Apps, Storage, Batteries

---

## 12. Tech Stack & Structure

- **React** + **Tailwind CSS** + **Vite**
- Clean, reusable components (e.g. `Sidebar`, `ChatPanel`, `MessageBubble`, `InputBar`, `Recommendations`)
- No backend — use mock data and simulated delays for "Processing your request…"
- Make the prototype interactive: clicking prompt tiles sends the prompt, clicking recommendations sends follow-up, thread menu works, reasoning toggle expands/collapses

---

## Summary Checklist

- [ ] Two-panel layout (sidebar + main)
- [ ] Top nav: logo, product switcher, breadcrumb, search, help, notifications, user
- [ ] Sidebar: Lenovo IT Assist header, Deployment assistant, Pinned threads, Recent threads, thread list with 3-dot menu
- [ ] Empty state: AI icon, "How may I assist you today?", 5+ prompt tiles
- [ ] Response anatomy: timestamp, reasoning toggle, body, thumbs, recommendations
- [ ] In-progress: "Processing your request…", stop button in input bar
- [ ] Input bar: placeholder, Explore, Favorite prompts, send, disclaimer
- [ ] Mock KB, Data insights, Actions, Agentic responses
- [ ] Realistic IT Admin data throughout
