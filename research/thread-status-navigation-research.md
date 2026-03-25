# Thread Status When Navigating Away — Feature Research

**Feature:** Users can leave the chat (navigate away from an active thread) and see the status of response progress at the thread level (e.g. in the sidebar thread list).

**Product:** Lenovo IT Assist | **Persona:** IT Admin

---

## 1. Problem Identification

### Who is affected

**IT Admins** who use Lenovo IT Assist for:
- **Data insights** — fleet analytics, reporting, charts (can take 10–60+ seconds)
- **Agentic workflows** — plan-and-execute agents, multi-step flows (can run minutes)
- **Actions** — system scan, device onboarding (variable duration)

### What problem they have

Today, the "Processing your request…" indicator is shown **only while the user is viewing the thread**. If the IT Admin:

1. **Navigates to another thread** — to check a previous answer or start a new query
2. **Navigates to another page** — Device Management, Dashboard, Device Insights
3. **Closes the panel** — if using the embedded panel (Phase 2)
4. **Refreshes the page** — or opens IT Assist in a new tab

…they lose visibility into whether the response is still generating, has completed, or has errored. They must return to the thread to find out.

### Why this matters

- **Multitasking.** IT Admins often juggle multiple tasks. A long-running data insight or agentic workflow should not force them to stare at the screen. They want to continue working elsewhere and know when to return.
- **Productivity.** Waiting blocks other work. Without status visibility, users either wait (wasted time) or leave and forget (risk missing the result or not knowing it failed).
- **Trust.** If responses are lost when navigating away (a known Copilot limitation), users lose trust. If the backend continues but the UI does not reflect it, users are confused.

### Evidence

- **Microsoft Copilot:** Users report that responses may not display until they switch chats and return; Copilot does not support persistent background processing — if users navigate away, the response may be lost. A feature request exists for background processing with task history and notifications.
- **Industry pattern:** Letta, Microsoft Agent Framework, and similar platforms support background mode with resumable streaming and async/proactive notifications for long-running agent tasks.

---

## 2. Potential Solutions

### 2.1 Navigation scenarios (what "leave the chat" means)

| Scenario | User action | Frontend state | Backend state |
|----------|-------------|----------------|---------------|
| **A** | Switches to another thread in sidebar | Same IT Assist route; streaming connection may stay or be swapped | Generation continues |
| **B** | Navigates to another page (Device Management, Dashboard) | Embedded panel stays mounted; streaming persists | Generation continues |
| **C** | Closes embedded panel | Panel unmounts | Streaming connection closes; backend continues and persists response |
| **D** | Refreshes page or opens new tab | Full reload | New session; old connection gone; backend continues and persists response |

**Implication (revised):** Because the embedded panel stays mounted across page navigation (Scenario B), only Scenarios C and D truly break the frontend streaming connection. Backend state tracking is needed only for those two cases. The backend already persists response content on disconnect, so only a status endpoint is needed.

---

### 2.2 Solution options

#### Option 1: Frontend-only (within IT Assist module)

**Approach:** Use existing frontend streaming state. Status on thread chips works as long as the user stays within the IT Assist full-page or embedded panel view.

**Works for:** Scenario A (switch thread within sidebar) and Scenario B (navigate to another page — panel stays mounted). The existing draft stories (Stories 1–5) cover Scenario A; Scenario B is covered by the panel staying alive.

**Does not work for:** Scenarios C, D. When the user closes the panel or refreshes, the streaming connection is lost.

**Scope:** Covers the most common navigation patterns with no new backend work.

---

#### Option 2: Backend state tracking + polling on return

**Approach:** Backend tracks generation state per thread (e.g. `generating`, `completed`, `error`). When the user reopens IT Assist (after panel close or page refresh), the frontend polls or fetches thread list with status.

**Works for:** Scenarios C, D. User can close the panel or refresh; on return, they see accurate status.

**Requires:**
- Backend API to expose thread-level generation state (or include it in thread list response)
- Backend already persists response content — only status tracking is new
- Frontend to fetch this on load/panel open

**Cost:** Modest backend changes. Status endpoint or augmented thread list. Need to define state lifecycle (TTL for "generating" if connection drops without completion).

---

#### Option 3: Backend state + push (WebSocket/SSE) for real-time updates

**Approach:** Backend tracks state; frontend subscribes to thread-level status updates via a persistent WebSocket or SSE connection that survives navigation within the SPA (e.g. connection at app root, not per-route).

**Works for:** Scenarios A, B (if connection is app-level). For C, D, connection is lost; Option 2 (poll on return) still needed.

**Requires:**
- App-level WebSocket/SSE (or SharedWorker) so connection is not tied to IT Assist route
- Backend to push status changes (generating → completed/error)
- Fallback to polling when connection is re-established after refresh

**Cost:** Higher complexity. Connection management, reconnection, and fallback logic.

---

#### Option 4: Notification when response completes (user has left)

**Approach:** When generation completes (or errors) and the user is not viewing that thread, notify them.

**Patterns:**
- **In-app badge** — e.g. on IT Assist nav item or panel button: "1 thread updated"
- **Toast notification** — "Response ready in thread [name]" with link to open
- **Browser notification** — optional; may be overkill for enterprise and requires permission

**Requires:** Backend or frontend to know (a) generation completed, (b) user is not viewing that thread. Backend is the source of truth for (a); frontend knows (b) only while the app is open.

**Scope:** Complements Options 2 or 3. Does not replace status visibility; it adds "come back" signalling.

---

#### Option 5: Cross-module visibility (status outside IT Assist)

**Approach:** Show IT Assist thread status from other platform modules (e.g. badge on nav, or small indicator on Dashboard/Device Management).

**Works for:** User on Device Management sees "1 response ready" without opening IT Assist.

**Requires:** Either (a) app-level state/connection so status is available everywhere, or (b) a lightweight API that other modules can call. Adds cross-module coupling.

**Scope:** Adjacent. High value for discoverability but increases scope. Recommend as a later phase.

---

### 2.3 How other products handle it

| Product | Behaviour | Notes |
|---------|-----------|-------|
| **Microsoft Copilot** | Must keep chat active | Known limitation; response may be lost if user navigates away. Feature request for background processing. |
| **ChatGPT** | Per-conversation view | No documented thread-level status when navigating away. |
| **Letta / Agent frameworks** | Background mode, resumable streaming | `run_id` + `seq_id` for reconnect; results in persistent storage. |
| **Microsoft Agent Framework** | Async + proactive messages | Background tasks notify when complete; 15s initial, 45s between updates. |

**Takeaway:** Enterprise products are evolving toward background processing and notifications. Many still require the user to stay in the chat. IT Assist can differentiate by supporting "leave and return" with clear status.

---

### 2.4 Impact on existing features

| Feature | Impact |
|---------|--------|
| **In-progress state** | "Processing your request…" remains in-thread. Thread chip status supplements it; both can coexist. |
| **Stop/cancel button** | Today's stop button is in-thread only. Users cannot cancel from a thread they are not viewing. This is a gap — consider adding a "Cancel" action on the thread chip for generating threads. |
| **Thread management** | Rename, Pin, Delete unchanged. Status is additive. |
| **Embedded panel** | Panel stays mounted across page navigation, so streaming persists for Scenario B. Only panel close (C) and refresh (D) break the connection. |

---

## 3. Progressive Enhancement

| Phase | Scope | Backend | Frontend |
|-------|-------|---------|----------|
| **Phase 1 (existing stories)** | Status on thread chips when user is in IT Assist (switch thread only) | None | Streaming state only |
| **Phase 2a** | Status persists after panel close or page refresh; cancel from thread chip | Thread-level status endpoint (backend already persists content) | Poll thread list on panel open/refresh; cancel action on chip |
| **Phase 2b** | Notification when response completes and user has left | Backend tracks completion; optional push | Badge or toast |
| **Phase 3** | Cross-module visibility | Same as 2a | Badge on nav from any module |

---

## 4. Scope and Boundaries

### In scope (for this feature)

- User can **switch to another thread** and see Generating/Error status on the thread they left (existing stories).
- User can **navigate to another platform page** (Device Management, Dashboard, etc.) and thread status is visible because the **embedded panel stays mounted**.
- User can **continue working in another thread** while one is generating (multi-thread concurrency from a UX perspective).
- User can **close the panel or refresh the page** and, on return, see which threads have Generating/Completed/Error status (requires backend status endpoint).
- **Cancel from thread chip** — user can cancel generation of a thread they are not currently viewing, via the sidebar chip.
- **Notification** (badge or toast) when a response completes in a thread the user has left — within the IT Assist context (e.g. when panel is open or user is on IT Assist page).

### Adjacent (consider for later)

- Cross-module visibility (status from Dashboard, Device Management without opening IT Assist).
- Browser push notifications.
- Full background processing with resumable streaming (run_id/seq_id pattern).

### Out of scope

- Changing how generation works (streaming, agentic flows). This feature is about **visibility and persistence of status**.
- Email or external notifications.
- Multi-tab coordination (e.g. SharedWorker). Prefer simpler polling-on-return first.

---

## 5. Risks and Open Questions

### Risks

1. **Backend state lifecycle:** If the frontend disconnects mid-stream, when does the backend clear "generating"? Need a timeout or explicit completion/error/cancel.
2. **Cost:** Polling or push adds load. For enterprise, keep polling interval reasonable (e.g. 5–10s when IT Assist is in view, or only on navigation into IT Assist).
3. **Stale state:** User returns after hours. Should "generating" still show? Likely not — need TTL or "last activity" semantics.

### Open questions (resolved)

1. **Does the backend today persist response content if the client disconnects?** **Yes.** Backend continues generation and stores the response. This simplifies Phase 2a — we only need a thread-level status endpoint, not content persistence changes.
2. **Can the user cancel generation from a thread they are not viewing?** **No.** Today's stop button is in-thread only. This is a gap: if the user can see "Generating" on a thread chip, they may expect to cancel from there. Consider adding a "Cancel" action on the thread chip for generating threads (new scope item).
3. **Embedded panel:** Does the panel stay mounted across page navigation? **Yes.** This means Scenario B (navigate to another platform page) is largely covered by frontend streaming — the panel stays alive and streaming persists. Only Scenarios C (user explicitly closes panel) and D (refresh/new tab) truly require backend state for status persistence.

---

## 6. Revised Navigation Scenario Coverage

Given the resolved answers, the scenario coverage is:

| Scenario | Coverage | Mechanism |
|----------|----------|-----------|
| **A** Switch thread | Covered | Frontend streaming (existing stories) |
| **B** Navigate to another page | Covered | Embedded panel stays mounted; streaming persists |
| **C** Close embedded panel | Needs backend state | Backend status API + poll on panel reopen |
| **D** Refresh / new tab | Needs backend state | Backend status API + poll on load |

**Key implication:** Only Scenarios C and D require backend state. This narrows the backend scope significantly.

---

## 7. Summary

| Gap | Solution direction |
|-----|-------------------|
| Switch thread only | Existing stories (frontend streaming state) |
| Navigate to other page (panel open) | Covered — panel stays mounted, streaming persists |
| Close panel, then reopen | Backend status endpoint + poll thread list on panel open |
| Notification when complete | Badge or toast when user has left the thread |
| Cancel from thread chip | New scope item — "Cancel" action on generating thread chip |
| Cross-module visibility | Phase 3; badge on nav |
| Page refresh / new tab | Backend status endpoint + poll on load |

**Recommendation:** Implement Phase 1 (existing stories) as-is. For "close panel and return" and "refresh/new tab," add backend thread-level generation status endpoint and poll on return (Phase 2a). Add cancel-from-chip as part of Phase 2a. Add completion notification (Phase 2b) once state is available. Defer cross-module visibility to Phase 3.
