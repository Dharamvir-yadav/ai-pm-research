# Research: LITA chat completion awareness — LDO-global vs LITA-specific mechanisms

**Topic:** Notify users when a Lenovo IT Assist (LITA) chat response is complete so they need not remain on the LITA screen. Two layers: **platform-wide (LDO)** and **in-product (LITA)** — including **progress tracking without being in the thread**.

**Sources:** `context/product-definition.md`, `context/industry-context.md`; public vendor documentation where cited; gaps marked **unverified**.

**Assumptions (explicit):** A reliable “completion” signal for users implies a **server-backed** terminal state (or equivalent durable event), not only client-side UI. The SSOT states the in-progress indicator is a **UI facade** today; any notification or cross-page progress UX **depends** on backend evolution — flagged in Open Questions.

**Current delivery scope (stakeholder):** Implement **only** the **per-thread state identifier** on the **thread list** (each row’s thread banner): **Active**, **Completed**, **Failed** (and optionally **Cancelled** / **Awaiting user** / **Idle**). **LDO-level mechanisms** (nav badge, notification center, toasts, push, email) and **pairing** rules with the shell are **explicitly out of this increment**—documented below for continuity when you pick them up later.

**Stakeholder direction (deferred):** When you add LDO attention patterns, reuse the **same thread/run state** that powers list identifiers so shell and LITA never disagree.

---

## 1. Problem & WHY

### 1.1 Who is affected

- **Primary:** IT Admins using LITA inside Lenovo Device Orchestration (LDO) for KB Q&A, fleet data insights, and **agentic / long-running actions** (e.g. system scan, update, onboarding per product definition).
- **Secondary:** IT operations leads who care about throughput and multitasking across Dashboard, Device Management, Insights, and LITA without losing track of assistant work.

### 1.2 Affected users & JTBD

| Persona | Relevant JTBD (from `industry-context.md`, adapted) |
|--------|------------------------------------------------------|
| **IT Admin** | Get fleet answers and run guided actions **without blocking** on one screen while other LDO work is urgent. |
| **IT Admin** | **Return at the right moment** to review AI output, reasoning, and any proposed actions (human-in-the-loop). |
| **IT Operations lead** | Reduce **context loss** and rework when admins switch modules during long-running assistant or automation steps. |

### 1.3 The problem

- **“Processing your request…”** signals work in flight, but per SSOT it is a **UI facade only** — not bound to backend stages — and users who navigate away risk **missing completion** or losing track of **which thread** was running.
- LITA is reached via **nav (e.g. dropdown)** and is **not integrated with all pages** today, so context switches are explicit and common.

### 1.4 WHY it matters

- **Cost of waiting:** Long or variable latency (LLM + tools + actions) keeps admins **blocked on one surface** or forces **polling by revisiting** the thread with no durable “job” metaphor.
- **Cost of switching:** Without a **single place** to see “LITA finished” or **which thread** completed, users may act on stale assumptions (still running vs done) and incur rework.
- **Trust and safety:** Agentic flows amplify the need to **re-engage at completion** so the user can review reasoning, feedback, and actions — aligned with enterprise norms (auditability, human oversight) in `industry-context.md`.

---

## 2. Current-state gap (SSOT-aligned)

| Aspect | Current (per SSOT) | Gap vs desired experience |
|--------|---------------------|---------------------------|
| **LDO shell** | Modules (Dashboard, Device Management, Insights, LITA, Tickets, Config); no stated **cross-module notification center** for assistant jobs | No **platform-level** routing of attention when LITA work completes while the user is elsewhere in LDO |
| **LITA module** | Thread list (pinned/recent), in-thread “Processing…”, stop/cancel; threads named | No stated **persistent “running / ready”** state visible **outside** the active thread or **outside** LITA |
| **Progress truth** | UI facade only | **Completion / stage events** are not guaranteed observable for trustworthy notifications or global UI |

**Layering principle:** LDO owns **routing attention** across the product; LITA owns **conversation and thread UX**. Prefer one **job/run model** (or equivalent) consumed by both layers so indicators do not contradict each other. **For the current increment**, only the **LITA thread-list** surface is in scope; the same model should still be designed so **future** LDO widgets can subscribe without a redesign.

---

## 3. Solution options: LDO-global vs LITA-scoped vs combined

### 3.1 Global (LDO) mechanisms

| Direction | Description | Pros | Cons / notes |
|-----------|-------------|------|----------------|
| **In-app notification center (bell)** | Central list: e.g. “LITA: response ready — [thread name]” with deep link | Familiar enterprise pattern; no OS permissions | Shell UX work, read-state, retention policy |
| **Toasts / banners** | Transient banner on navigation or top bar when completion fires | Low friction | Easy to miss; deduplication and accessibility |
| **Nav affordance** (see **§3.1.1** — **later phase**) | Badge (or dot + optional count cap) on **LITA** in the LDO nav when any thread has **in-flight** or **completed-unread** work | Visible from **any** LDO module while nav persists; no bell page required for a minimal slice | **Not in current delivery**; requires shell integration; aggregation rules; non-sensitive chrome |
| **Browser / OS push** | Web Push or desktop notifications when tab unfocused | Strong for “walk away” | **Privacy/security** review (permission prompts, body content), enterprise policy variance |
| **Email** | “Your LITA request completed” with link | Works when user leaves LDO entirely | Latency, PII in email, volume, opt-in |

**Research-level stance (full vision):** Prefer **in-app** first (center and/or nav badge ± toast), tied to authenticated session; treat **email and OS push** as optional channels with explicit consent and **content minimization**. **Current build:** thread-list identifiers only (§3.4).

### 3.1.1 Nav affordance — deep dive (**later phase**, not current delivery)

Keep this section when you prioritize **cross-module** awareness (user on Dashboard, etc.). It does **not** ship with the thread-only increment.

**Why it mattered in earlier research**

- **Matches actual behavior:** Users already leave LITA via the **same nav** they use to return (`product-definition.md`: chatbot reached from platform nav). A badge is the smallest **“something changed in LITA”** signal that does not require them to **open the module on a guess**.
- **Cross-page without new destinations:** Unlike a notification center, a nav dot does not introduce a new **inbox mental model**, retention policy, or “mark all read” workflow—yet it still solves **“I’m on Dashboard and my long answer finished.”**
- **Enterprise-friendly default:** Nav chrome can stay **generic** (“activity in LITA”) so **DLP-sensitive** thread titles and answer previews never appear in the shell—detail stays inside LITA (banner / thread list).
- **Composes upward:** The same **aggregated state** that drives the badge can later **feed** a bell inbox or toasts without changing the underlying **run state** model.

**Concrete behaviors to specify (product / UX)**

| Topic | Recommendation |
|--------|----------------|
| **When the badge appears** | At least: **any thread** with a **server-acknowledged in-flight run** for this user/tenant; optionally extend to **“completed since last visit”** (unread completion) so users who missed the moment still see a nudge. |
| **Dot vs count** | **Dot** (or capped **9+**) reduces wrong conclusions (“3 things” might be 3 threads vs 3 runs); if **count** is used, define whether it is **threads with activity** or **in-flight runs**. |
| **Clearing** | Opening **LITA** clears **“new completion”** badge only after user **views** the terminal state (or dismisses), not merely on module mount—avoid silent false clears. **In-flight** clears when **no** runs remain in-flight (cancelled/failed/done). |
| **Deep link** | Clicking **LITA** while badge is for a **specific thread** should land on that thread when unambiguous; if **multiple**, land on **LITA home / last thread** with **each thread’s banner** already showing **Active / Completed / Failed** so the user can choose without opening each thread. |
| **Multi-tab** | Same user, two tabs: prefer **server-backed** counts or **event sync** so badges do not diverge indefinitely; minimum bar is **refresh on focus**. |
| **Accessibility** | Do not rely on color alone; support **tooltips** (“LITA: response in progress” / “LITA: ready to review”) and **keyboard** nav to LITA. Use **live regions** sparingly at shell level (optional) to avoid chatter. |
| **Authorization** | Badge computation must **only** include threads the user may access; no cross-tenant leakage. |

**Dependencies:** Shell team owns **placement and visual system**; LITA/backend owns **state API**. Treat as a **contract**: e.g. `GET /lita/activity-summary` (names illustrative) returning counts or booleans, not message bodies.

### 3.2 LITA-scoped mechanisms

| Direction | Description | Pros | Cons / notes |
|-----------|-------------|------|----------------|
| **Background run with thread continuity** | Associate each in-flight turn with a **run**; user can browse other LDO pages; **each thread list row’s banner** shows a **state identifier** (**Active** / **Completed** / **Failed**, etc.) for that thread’s latest run | Matches “don’t stay in thread” without requiring OS push; scan **all threads** at a glance | Requires backend correlation **thread ↔ run** and list API that returns **per-thread terminal or in-flight state** |
| **Running jobs strip or drawer** | Within LITA: list of active runs across threads | Clear for multi-thread power users | Module-scoped unless mirrored at LDO |
| **Stage-aware progress** | Coarse stages (e.g. planning, tool use, summarizing) when backend supports them | Reduces anxiety and support burden | Only honest if **instrumented server-side** |
| **Stop/cancel propagation** | Cancel stops work and updates **thread-list identifiers** (and later any LDO indicators) consistently | Safety + trust | SSOT: stop/cancel in UI exists; must align with async model |

**Non-AI boundary:** If completion is purely deterministic automation with known stages, **job queue + notification** may suffice without LLM-specific logic — controls **cost** and **complexity** per research scope rules.

### 3.3 Combined (LDO + LITA) — **full vision; LDO not in current delivery**

- **LITA** provides **truthful thread/run state** and **deep links**; **LDO** (later) surfaces **attention** (badge, center, optional toast) when terminal state is reached.
- **Single event stream** (or poll) keyed by **user + tenant** with **authorized** thread/run references avoids duplicate or conflicting “done” signals.
- **Unread / “needs review”** can be a product concept that powers both the thread list and a future global notification center.

### 3.4 Current delivery: per-thread banner state identifiers **only**

This section defines what ships **now**: **each thread’s** list row shows **that thread’s** response state—**no** LDO nav badge, **no** notification center, **no** push/email in this increment.

**Per-thread thread banner (definition — stakeholder-aligned)**

- In the **thread list** (pinned / recent per SSOT), **each thread** is represented by a row that includes a dedicated **thread banner** strip (or clearly bounded **banner region** on the row—not only a tiny dot lost in the title).
- That banner carries a **state identifier** tied to the **latest user-initiated assistant run** on that thread (the turn the user is waiting on):
  - **Active** — a response is **in progress** for this thread (spinner / pulse / “Active” label; indeterminate unless server exposes real stages).
  - **Completed** — last run ended **successfully**; optional second axis **unread vs viewed** (e.g. Completed vs Completed • needs review) if product wants “nudge” without reopening.
  - **Failed** — last run ended in **error** or guardrail failure; must be **as visually prominent** as Completed so admins never assume success from silence.
- **Optional extensions:** **Cancelled** (user stopped the run), **Awaiting user** (human-in-the-loop approval), **Idle** / no banner when there is no outstanding run—pick one vocabulary; when LDO nav ships later, **reuse the same labels** in tooltips for consistency.

**Identifier UX (research-level guidance)**

| Concern | Guidance |
|--------|----------|
| **Encoding** | Prefer **icon + short text** or **labeled pill** (not color alone) for **WCAG**; tooltip expands (“Response in progress”, “Last response failed”). |
| **Which run** | Default: **most recent** user message that triggered processing; if the user sends a new message while Active, state rolls forward to the **new** run. |
| **List performance** | Thread list endpoint (or field on thread summary) should return **state enum + optional run id** per thread—avoid N+1 fetches per row. |
| **Open thread** | Optional **echo** of the same identifier in **conversation header** chrome for consistency; not a substitute for **list** banners when the goal is “see all threads without entering each.” |

**Relationship to existing in-thread UI**

- SSOT already has **“Processing your request…”** in the transcript. The **thread-banner identifier** is the **at-a-glance** signal in the **sidebar**; in-thread copy can remain the **detailed** progress line. If both exist, they must show the **same** underlying state to avoid contradiction.

**Why this is the right *current* slice**

- **Multi-thread clarity:** While the user is **in LITA**, they can see **which** conversation is **Active**, **Completed**, or **Failed** **without** opening each thread—directly addresses “not in the **conversation**.”
- **Known limitation:** If the user **navigates away from LITA** to another LDO module, **nothing in this increment** alerts them—they must **return to LITA** to see list identifiers. **Nav / bell / push** (§3.1, §3.1.1) close that gap when you schedule them.

**List-only scenarios (in scope)**

| Scenario | Expected UX |
|----------|-------------|
| User **inside LITA** on thread list | **Every** row’s banner shows **Active / Completed / Failed** (etc.) for that thread. |
| User **opens** a thread | List row and in-thread “Processing…” (SSOT) stay **consistent** with the same backend state. |
| Run **Completes** or **Fails** | That row’s identifier updates to **Completed** or **Failed** (timely once server knows terminal state). |
| User **cancels** | That thread’s banner moves to **Cancelled** (or **Idle**); no other module updates in this increment. |

**Edge cases to design explicitly**

- **Completed + unread:** Define whether **Completed** (or a “needs review” variant) clears when the user **opens** the thread, **scrolls to bottom**, or **explicitly dismisses**—only affects **list + optional header echo** until nav exists.
- **Failed then new message:** New **Active** supersedes **Failed** on the row, but **history** might still show the failed turn in the transcript.
- **Stale client:** If WebSocket drops, **poll on focus** (or periodic refresh while LITA is visible) so row identifiers **resync**.

**Explicitly not in this increment**

- LDO **nav badge**; **notification center**; **toasts**; **web push**; **email** — see §3.1 / §3.1.1 when prioritized.

---

## 4. Progress vs notification tradeoffs

| Dimension | **Progress (while running)** | **Completion notification** |
|-----------|------------------------------|-----------------------------|
| **User need** | Reduces uncertainty during long runs; supports prioritization (“wait vs switch”) | Brings user back when **safe to review** or when **action required** |
| **Honesty** | Risk of **misleading** stages if still facade-only; prefer **coarse** real stages or **indeterminate** spinner | Requires **reliable terminal state** from server |
| **Noise** | Frequent updates → alert fatigue if pushed globally | Fewer events if gated to **meaningful transitions** only |
| **Privacy** | Stage labels might leak intent (“querying HR devices…”) | OS/email bodies must avoid sensitive **fleet or PII snippets** |
| **Implementation** | Often needs **streaming**, **WebSocket**, or **polling** + run metadata | Often needs **notification inbox** + idempotent “delivered” semantics |
| **Best combo** | **LITA-first** (sidebar, in-module list) for progress; **LDO** for **completion** and **failure** (and optional “needs approval”) | Same **run ID** ties both |

**Product judgment (current scope):** “Track without being in the **conversation**” is met by **per-thread list banners** (§3.4)—**Active / Completed / Failed** without opening that thread. **“Track while outside LITA”** is **not** met until a **later** LDO mechanism (e.g. §3.1.1) ships; call that gap in release notes or internal comms so expectations stay aligned.

---

## 5. Competitive / market scan

**Method:** Enterprise set from `industry-context.md` plus Microsoft Copilot patterns; SMB toggle is **yes** — mid-market tools may inspire **UX only**, labeled **non-enterprise / inspiration**.

| Vendor / product | What they do (relevant) | Source & verification |
|------------------|-------------------------|------------------------|
| **Microsoft 365 Copilot (Graph)** | **Change notifications** for Copilot **aiInteraction** resources: subscribe when a user queries Copilot or **when Copilot responds**; tenant- or user-scoped subscriptions; optional encrypted resource payload. | Verified: [Get change notifications for Copilot AI interactions using Microsoft Graph](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/api/ai-services/change-notifications/aiinteraction-changenotifications) |
| **Microsoft 365 Copilot — custom engine agents** | **Asynchronous patterns**: user can keep chatting while a task runs (minutes–days); **after completion, the agent sends a notification to the user**; distinguishes follow-up vs long-running vs proactive messages. Notes **Copilot Studio–built custom engine agents don’t support async messages** (platform split). | Verified: [User Experience for Custom Engine Agents in Microsoft 365 Copilot](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/ux-custom-engine-agent) |
| **Microsoft Intune** | **Device-targeted** notifications (custom notifications, enrollment notifications); adjacent pattern for **IT admin surfaces** and notification infrastructure — not a direct “chat completion” analog. | Verified (adjacent): [Send custom notifications](https://learn.microsoft.com/en-us/mem/intune/remote-actions/custom-notifications) |
| **ServiceNow — Virtual Agent** | **Async web** configuration and **VA notifications / proactive triggers** (enhanced chat). Exact UX for “leave page, get ping when bot finishes” **not confirmed** from excerpts used here. | Partially cited; **unverified** for completion UX: [Configure Async Web](https://www.servicenow.com/docs/bundle/zurich-conversational-interfaces/page/administer/virtual-agent/task/configure-async-web.html), [VA notifications / proactive triggers](https://www.servicenow.com/docs/r/conversational-interfaces/now-assist-in-virtual-agent/va-notifications-proactive-triggers-enhanced-chat.html) |
| **Tanium Ask** | AI-assisted natural language / agentic querying; **specific “notify when answer ready” UX** not verified from primary docs in this pass. | Positioning: [Tanium Ask Agent — Tanium](https://www.tanium.com/resources/tanium-ask-agent-data-sheet/) — **unverified** for completion notifications |
| **Ivanti Neurons, ManageEngine, Freshservice (Freddy)** | Assistant / automation in ITSM–ITAM adjacent suites; **no primary-source verification** in this research for async completion notifications. | **Unverified** — follow-up competitive deep-dive if sales prioritizes |
| **NinjaOne, Adaptiva** (industry list) | Endpoint / automation platforms; **no primary-source verification** here for LITA-like chat completion. | **Unverified** |

**Non-enterprise / inspiration (SMB toggle yes):** Mid-market products sometimes use **email digests** or **in-app toasts** for long reports — **ideas only**, not enterprise comparables.

---

## 6. Enterprise considerations

**Security**

- Notifications must **not leak** another user’s threads or tenant data (**authorization** on every run/thread).
- **Deep links** enforce session and role checks; avoid sensitive fleet details in **OS notification bodies** (prefer generic “Response ready in LITA” + non-sensitive thread label).
- Any future **subscription / webhook** API needs **signature validation, secret rotation, replay protection**.

**Privacy**

- **PII minimization** in payloads; configurable verbosity; tenant/regional rules for **email** and **push**.
- **Retention** of “completed / unread” in a center affects storage and data-subject workflows.

**Cost**

- Avoid notifying on every token — gate on **meaningful state transitions** (completed, failed, cancelled, needs_approval).
- Prefer **orchestration** without extra model calls over “AI summarizing progress” per stage unless justified.

**Latency**

- Value is **timely** delivery once the server knows completion; avoid blocking navigation on **client-only** timers.

---

## 7. Compliance (cross-cutting)

*Not legal advice. Brief themes only; article-level depth if the feature later ties to high-risk automated decision-making or regulated data flows.*

- **Human oversight & usability (NIST AI RMF — Govern / Map / Manage):** Surfacing **completion** when the user is not in the chat supports **timely human review** of outputs and proposed actions. Reference: [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework).
- **Transparency (EU AI Act):** Users should understand **what completed** (e.g. informational answer vs. action proposal) and that content is **AI-generated**, consistent with common **labeling** patterns in enterprise assistants. For official text, see e.g. consolidated EU AI Act publications via [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689) — specific articles apply by deployment role and system class; **confirm with legal** for your offering.
- **Logging & audit:** Correlating **notification delivery** (channel, timestamp, user) with **run / thread ID** may support incident response; balance with minimization.
- **Third-party channels:** **OS notifications and email** add **processors and policy** surface (MDM, DLP); default **in-app** reduces exposure until opt-in.

---

## 8. Open questions for stakeholders

1. **Source of truth:** Will the backend expose a **durable run/job ID** and terminal states (`completed`, `failed`, `cancelled`, `awaiting_user`) for every user-visible “processing,” including **multi-step agents**?
2. **Multi-tab / multi-device:** Per **browser session** only, or **cross-device** for the same user (implies server-side notification inbox)?
3. **Notification content:** Minimum viable text vs thread title vs **preview** — what passes **DLP / privacy** review?
4. **Failure modes:** How to surface **partial** completion, **timeout**, or **guardrail block** (not only happy path)?
5. **Rate limits:** Expected concurrent runs per user/tenant for **fan-out** and anti-abuse?
6. **Stack constraints:** If parts of LITA mirror the Microsoft split (**async messaging not supported** on a given builder), which experiences are in/out?
7. **Legal / policy:** Are **browser push** or **email** allowed by default, or **tenant opt-in** only?

---

## 9. Explicit scope boundaries

**In scope — *this* delivery (requirements can narrow here)**

- **LITA thread list only:** **Per-thread banner** / row region with a **state identifier** per thread: **Active**, **Completed**, **Failed** (plus optional **Cancelled** / **Awaiting user** / **Idle**), backed by **server truth** when available (see Open Questions).
- Optional **conversation-header echo** of the same state (polish); primary scan surface remains the **list**.
- **Honest coarse states** only; fine-grained progress stages remain a future enabler unless backend already exposes them.

**Deferred — same research doc, later delivery**

- **All LDO-level attention:** nav badge (§3.1.1), notification center, shell toasts, browser/OS push, email.
- Dedicated **running-jobs drawer**; **customer-facing webhooks** — revisit when needed.

**Out of scope / separate initiatives**

- **Embedding LITA in every page** (planned separately per SSOT).
- **Model latency** or **agent planning** changes — only **awareness** of outcomes.
- **End-user device notifications** (Intune-style device push) — different problem from **admin web console** completion.

**Depends on product decision**

- Whether “completion” means **chat response only** vs **downstream action** milestones (e.g. scan finished on endpoints) — may split templates: **“response ready”** vs **“operation complete”**.

---

## Revision note

Update this file when the product exposes **backend-driven** processing states (beyond UI-only facade) so requirements can bind to **observable events** and notification rules.

**2026-04-17:** Strengthened **nav affordance** (§3.1.1) and added **v1 slice: nav + thread-level banner** (§3.4) per stakeholder direction. **Clarified:** “Thread banner” = **per thread row** in the list, each with an **Active / Completed / Failed** (etc.) **identifier**, not only an in-conversation strip.

**2026-04-17 (revision):** **Current delivery** narrowed to **thread-list identifiers only**; LDO/nav and other channels marked **deferred** (§9, §3.4, §3.1.1).
