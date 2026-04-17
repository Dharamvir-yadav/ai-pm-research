# Research: LITA chat completion awareness — LDO-global vs LITA-specific mechanisms

**Topic:** Notify users when a Lenovo IT Assist (LITA) chat response is complete so they need not remain on the LITA screen. Two layers: **platform-wide (LDO)** and **in-product (LITA)** progress tracking.

**Sources:** `context/product-definition.md`, `context/industry-context.md`; public vendor documentation where cited; gaps marked **unverified**.

---

## 1. Problem & WHY

**Who is affected**

- **Primary:** IT Admins using LITA inside Lenovo Device Orchestration (LDO) for KB Q&A, fleet data insights, and increasingly **agentic / long-running actions** (scans, updates, onboarding per product definition).
- **Secondary:** IT operations leads who care about throughput and multitasking across Dashboard, Device Management, Insights, and LITA without losing track of assistant work.

**The problem**

- Today, **“Processing your request…”** signals work in flight, but it is a **UI facade only** — not bound to backend stages — and users who navigate away risk **missing completion** or losing mental context about which thread was running.
- LITA is reached via **nav (e.g. dropdown)** and is **not embedded across all pages**, so context switches are explicit and common.

**WHY it matters**

- **Cost of waiting:** Long or variable latency (LLM + tools + actions) keeps admins **blocked on one surface** or forces **polling by revisiting** the thread with no durable “job” metaphor.
- **Cost of switching:** If they leave to use another LDO module, they lack a **single place** to see “LITA finished” or **which thread** completed — increasing errors (acting on stale assumption that work is still running) and rework.
- **Trust and safety:** Agentic flows amplify the need to **re-engage at completion** so the user can review reasoning, feedback, and any proposed actions — aligned with enterprise norms (auditability, human-in-the-loop) in `industry-context.md`.

---

## 2. Current state vs desired (LDO vs LITA layering)

| Aspect | Current (per SSOT) | Desired direction (research) |
|--------|---------------------|------------------------------|
| **LDO shell** | Modules (Dashboard, Device Management, Insights, LITA, Tickets, Config) without a stated **cross-module notification center** for assistant jobs in product definition | **Platform-level** awareness: badge/toast/notification list when any in-flight LITA work for this user completes (or fails / is cancelled) |
| **LITA module** | Thread list, in-thread “Processing…”, stop/cancel, no stated persistence of “running jobs” outside the thread view | **Thread-scoped** progress surfacing: mini status, background continuation, deep link back to result; optional escalation to LDO-level notification |
| **Progress truth** | UI facade only | Product may evolve to **server-backed job/run IDs** and stage labels; research assumes **completion events** must become **durable** for any reliable notification (engineering detail in Open Questions) |

**Layering principle:** LDO owns **routing attention** across the product; LITA owns **conversation state and thread UX**. Avoid duplicating two incompatible sources of truth — prefer one **job/run model** consumed by both layers.

---

## 3. Solution directions

### 3.1 Global (LDO) mechanisms

| Direction | Description | Pros | Cons / notes |
|-----------|-------------|------|----------------|
| **In-app notification center (bell)** | Central list: “LITA: response ready — [thread name]” with deep link | Familiar enterprise pattern; works without OS permissions | Requires UI shell work, read-state, retention policy |
| **Toasts / banners** | Transient banner on navigation or top bar when completion fires | Low friction | Easy to miss; needs deduplication and accessibility |
| **Nav affordance** | Badge on LITA entry in dropdown when any thread has completing/completed-unread work | Lightweight | Limited detail until user opens LITA or center |
| **Browser/OS push** | Web Push or desktop notifications when tab unfocused | Strong for “walk away” | **Privacy/security** review (permission prompts, content in notification body), enterprise policy variance |
| **Email** | “Your LITA request completed” with link | Works when user leaves LDO entirely | Latency, PII in email, threading volume, opt-in |

**Recommendation (research-level):** Start with **in-app** (center +/or nav badge + optional toast) tied to authenticated session; treat **email and OS push** as optional channels with explicit consent and content minimization.

### 3.2 LITA-specific mechanisms

| Direction | Description | Pros | Cons / notes |
|-----------|-------------|------|----------------|
| **Background run with thread continuity** | Submit request returns a **run ID**; user can browse other LDO pages; LITA sidebar shows per-thread **Running** / **Ready** | Matches “don’t stay in thread” without inventing full OS push | Requires backend correlation thread ↔ run |
| **Compact “running jobs” strip or drawer** | Within LITA: list of active runs across threads | Clear for multi-thread power users | Still module-scoped unless mirrored at LDO |
| **Stage-aware progress** | Replace pure facade with coarse stages (e.g. planning, tool use, summarizing) when backend supports it | Reduces anxiety and support tickets | Only honest if instrumented server-side |
| **Stop/cancel propagation** | Ensure cancel stops work and updates global/LITA indicators consistently | Safety + trust | Already partially present (stop/cancel in UI); must align with async model |

**Non-AI note (scope boundary):** If “completion” is purely deterministic automation with known duration, **simple job queue + notification** may suffice without LLM-specific logic — call this out in design to control **cost** and **complexity** (`00-research-scope.mdc`).

---

## 4. Competitive / market scan

**Method:** Enterprise set from `industry-context.md` plus Microsoft Copilot patterns; SMB toggle is **yes** — **Lansweeper** / **Snipe-IT** only where labeled **non-enterprise / inspiration** (not verified for this specific feature).

| Vendor / product | What they do (relevant) | Source & verification |
|------------------|-------------------------|------------------------|
| **Microsoft 365 Copilot (Graph)** | **Change notifications** for Copilot **aiInteraction** resources: subscribe to be notified when a user queries Copilot or **when Copilot responds**; tenant- or user-scoped subscriptions; optional encrypted resource payload. | Verified: [Get change notifications for Copilot AI interactions using Microsoft Graph](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api/ai-services/change-notifications/aiinteraction-changenotifications) |
| **Microsoft 365 Copilot — custom engine agents** | Documents **asynchronous patterns**: user can keep chatting while a task runs (minutes–days); **after completion, the agent sends a notification to the user**; distinguishes follow-up vs long-running vs proactive messages. Notes **Copilot Studio–built custom engine agents don’t support async messages** (platform split). | Verified: [User Experience for Custom Engine Agents in Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/ux-custom-engine-agent) |
| **Microsoft Intune** | Strong **device-targeted** notifications (custom notifications, enrollment notifications); not a direct analog for “admin console AI chat completion,” but shows Microsoft’s **notification infrastructure** maturity for IT surfaces. | Verified (adjacent): [Send custom notifications](https://learn.microsoft.com/en-us/mem/intune/remote-actions/custom-notifications) |
| **ServiceNow — Virtual Agent** | Product line includes **async web** configuration and **VA notifications / proactive triggers** (enhanced chat). Exact UX for “leave page, get ping when bot finishes” **not confirmed** from fetched excerpts. | Partially cited; **unverified** for end-user completion UX: [Configure Async Web](https://www.servicenow.com/docs/bundle/zurich-conversational-interfaces/page/administer/virtual-agent/task/configure-async-web.html), [VA notifications / proactive triggers](https://www.servicenow.com/docs/r/conversational-interfaces/now-assist-in-virtual-agent/va-notifications-proactive-triggers-enhanced-chat.html) |
| **Tanium Ask** | AI-assisted natural language / agentic querying over endpoints; public materials emphasize Q&A and automation; **specific “notify when answer ready” UX** not verified from primary docs in this pass. | Positioning: [Tanium Ask Agent — Tanium](https://www.tanium.com/resources/tanium-ask-agent-data-sheet/) — **unverified** for completion notifications |
| **Ivanti Neurons / ManageEngine / Freshservice (Freddy)** | Likely in-product assistant or automation flows; **no primary-source verification** in this research for async completion notifications. | **Unverified** — treat as follow-up competitive deep-dive if sales names them |

**Non-enterprise / inspiration (SMB toggle yes):** Mid-market ITAM tools sometimes use **simple email digests** or **in-app toasts** for long reports — useful as UX inspiration only, not enterprise comparables.

---

## 5. Enterprise considerations & compliance

### 5.1 Enterprise considerations

**Security**

- Notifications must **not leak** another user’s threads or tenant data (strict **authorization on run/thread**).
- **Deep links** should enforce session and role checks; avoid putting sensitive fleet details in **OS notification bodies** (prefer “Response ready in LITA” + generic thread label).
- **Webhook-style** patterns (à la Graph subscriptions) imply **signature validation, secret rotation, replay protection** if LDO ever exposes subscription APIs to customers.

**Privacy**

- **PII minimization** in notification payload; configurable **verbosity**; regional / tenant policies for **email** and **push**.
- **Retention:** how long “completed / unread” stays in a notification center affects storage and **subject access** workflows.

**Cost**

- **Push volume** if every token stream event triggers noise — gate on **meaningful state transitions** (e.g. completed, failed, cancelled, needs_approval).
- LLM vs automation: **job orchestration** without extra model calls is cheaper than “AI summarizing progress” for each stage.

**Latency**

- User-perceived value depends on **timely** delivery once the server knows completion; avoid blocking navigation on client-only timers.

### 5.2 Compliance (NIST AI RMF, EU AI Act, US federal AI policy)

Independent, cross-cutting — not legal advice; deeper article-level analysis only if the feature touches **high-risk** automated decisions or regulated data flows (open for PM/legal).

- **Human oversight & usability (NIST AI RMF — Map / Govern / Manage themes):** Surfacing **completion and outcome** when the user is not staring at the chat supports **meaningful human review** before relying on outputs or actions, especially for **agentic** flows. Tie notifications to **clear next steps** (open thread, review reasoning, confirm action).
- **Transparency & disclosure (EU AI Act — general transparency obligations for certain AI systems):** Users should understand **what completed** (e.g. “answer” vs “action proposal”) and that content is **AI-generated** — consistent with existing **AI labeling** patterns in comparable platforms (see Microsoft “AI labels” in custom engine agent UX doc).
- **Logging & audit (sector-agnostic enterprise expectation):** Correlating **notification delivery** (channel, timestamp, user) with **run ID / thread ID** may be required for incident response; balance with **privacy minimization**.
- **Third-party / browser channels:** **OS notifications and email** introduce extra **processors and policies** (enterprise MDM, DLP); default **in-app** reduces compliance surface until explicitly enabled.

---

## 6. Open questions for PM / engineering / legal

1. **Source of truth:** Will the backend expose a **durable run/job ID** and terminal states (`completed`, `failed`, `cancelled`, `awaiting_user`) for every user-visible “processing,” including **multi-step agents**?
2. **Multi-tab / multi-device:** Should completion be **per browser session** only, or **cross-device** for the same user (implies server-side notification inbox)?
3. **Notification content:** Minimum viable text vs thread title vs **first-line preview** — what is acceptable under **DLP / privacy** review?
4. **Failure modes:** How to notify when **partial** completion, **timeout**, or **guardrail block** occurs (not only happy path)?
5. **Rate limits:** Expected concurrent runs per user/tenant to size **notification fan-out** and anti-abuse controls?
6. **Copilot Studio–style constraint analog:** If parts of LITA are built on a stack that **cannot** do async/proactive messaging (see Microsoft split above), which experiences are in/out?
7. **Legal / policy:** Are **browser push** or **email** allowed by default for all customers, or **opt-in** per tenant?

---

## 7. Explicit scope boundaries

**In scope (research)**

- **LDO-level** patterns for awareness (notification center, nav badge, toasts, optional browser/OS/email).
- **LITA-level** patterns for **tracking progress** without staying in the active thread (running list, thread states, deep links).
- **Honest progress** as a future enabler (stages), without requiring implementation detail in this document.

**Out of scope / separate initiatives**

- **Embedding LITA in every page** (noted as planned separately in SSOT).
- **Changing model latency** or **agent planning algorithms** (only **awareness** of outcomes).
- **End-user device notifications** (Intune-style **device** push) — different problem from **IT admin web console** completion.
- **Customer-facing webhook APIs** for Copilot-style Graph subscriptions — possible future enterprise ask, not assumed here.

**Depends on product decision**

- Whether “completion” includes **only generative text** or also **action execution** milestones (e.g. scan finished on endpoints) — may split into **chat complete** vs **operation complete** with different notification templates.

---

## Revision note

Update this file when the product exposes real **backend-driven** processing states (replacing UI-only facade) so requirements can be tied to observable events.
