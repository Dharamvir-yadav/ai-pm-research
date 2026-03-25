# Response Feedback Enhancement — Feature Research

**Product:** Lenovo IT Assist (Lenovo Device Orchestration) | **Persona:** IT Admin  
**Topic:** What comes after binary thumbs up/down — richer, actionable feedback for users and the product team.

**Current baseline (live):** Thumbs up / thumbs down per response; plus reasoning toggle, smart suggestions, in-progress/stop, thread management (per product definition).

---

## 1. User Problem

### Why binary feedback is not enough

**For IT Admins (expressible need):**

- **Ambiguous signal.** A thumb down can mean “wrong fact,” “wrong for *my* tenant,” “unsafe to run,” “too vague to act on,” “bad chart,” “agent went off the rails,” or “I’m frustrated with latency”—the product team cannot distinguish these without more structure. The user often *knows* which it is; the UI does not let them say it quickly.
- **Actionability.** Fleet and ops work is **decision- and execution-oriented**. If the answer is “sort of right” but missing a step, a scope caveat, or a link to the right KB article, thumbs down over-penalises; thumbs up teaches the wrong lesson. Users need a way to signal **“needs correction in this specific dimension.”**
- **Trust and accountability.** In enterprise IT, “wrong” can imply **compliance, change risk, or outage risk**. Binary feedback does not let an admin flag **policy/safety** separately from **quality**, which matters for audit mindset and escalation behaviour.
- **Effort vs reward.** If the only channel is binary, admins who would otherwise give a one-tap reason skip feedback entirely—**signal drops to noise** and product teams infer from aggregates alone.

**For the product team (operational need):**

- **Routing.** KB gaps, model hallucination, bad retrieval, bad chart interpretation, and **action/agent failures** need different owners (content, ML, data pipeline, workflow engine). Binary feedback does not route work.
- **Prioritisation.** Without categories or text, teams cannot **stack-rank** fixes (e.g. “security-flagged” vs “tone”) or tie feedback to **response type** or **tenant segment**.
- **Measurement.** Thumbs ratios alone are weak proxies for **resolution**, **time-to-action**, or **safe automation**—especially for agentic workflows where success is multi-step.

**What users want to express that they cannot today (hypothesis, user-validation needed):**

- “Correct but **incomplete** / missing prerequisite.”
- “**Not relevant** to my question or fleet context.”
- “**Outdated** vs current portal/policy.”
- “**Too verbose** / too terse for a ticket handoff.”
- “**Chart or number** doesn’t match what I asked or what I see elsewhere.”
- “I **would not run** this action / workflow as written.”
- “**Reasoning** helped / misled” (orthogonal to thumbs on the final answer).

---

## 2. Competitor & Best-Practice Analysis

*Note: Public docs and community sources vary in detail; treat product-specific UI as **patterns**, not copy-paste specs. Validate against live UIs during design.*

| Product / pattern | Mechanism | Enterprise-relevant notes |
|-------------------|-----------|---------------------------|
| **Microsoft Copilot Studio (custom agents)** | Thumbs up/down **plus optional comments**; analytics aggregates counts; comments visible in Analytics (docs state **28-day** availability for comments in Analytics UI); data also in **Dataverse** transcript table. Makers can **disable** collection. | Strong precedent: **binary + optional free text**, analytics for makers, **tenant control** of collection. Aligns with “cost & governance”: retention and storage are explicit. |
| **Microsoft 365 Copilot** | User thumbs feedback; **admins** can submit feedback from admin center; orgs can **turn off** user feedback. | Shows **admin-mediated** and **policy-off** patterns for regulated tenants. |
| **ChatGPT / consumer AI** | Thumbs down (and reporting flows for policy); community discussions note UX changes over time (e.g. visibility of thumbs up). | Consumer-first; less about **fleet context** and **action safety**; still shows expectation of **post-hoc elaboration** on negative signals. |
| **ServiceNow (Virtual Agent / AI analytics)** | Thumbs feedback discussed in community; **Assistant Analytics** and sentiment-style views appear in platform materials. | Relevant: tying conversational feedback to **analytics dashboards** and **operational** ownership inside ITSM stack. |
| **Intercom Fin** | Negative ratings with **written remarks**; reporting on DSAT and **unresolved** conversations; product surfaces **optimization** workflows comparing failed AI to human replies. | Relevant pattern: **structured reporting** + **closed-loop content/workflow improvement** (even if Lenovo’s “content” is KB + prompts + tools, not Fin’s article model). |
| **Zendesk / similar** | Often **CSAT after resolution**, ticket-linked feedback, macros—not always 1:1 with generative turn-level feedback. | Useful for **handoff to ticket** journeys; optional for IT Assist if chat stays in-product. |

**Patterns that work well for enterprise IT contexts**

1. **Progressive disclosure:** One tap (thumb) → optional **short reason chips** → optional **comment**; never block the user on a form.
2. **Maker/admin visibility:** Dashboards with filters (time, topic, channel, **response type** if available)—not only raw logs.
3. **Governance:** Org or tenant controls: enable/disable detailed feedback, **retention** limits, **export** rules.
4. **Separation of “safety/policy” from “quality”:** Distinct path or tag for **security/compliance** flags (may trigger different handling than “unclear answer”).
5. **Automation vs AI for triage:** **Rule-based** routing from categories and keywords is cheaper and more explainable than LLM-on-every-feedback for V1; reserve ML for **clustering/summarisation** at aggregate level when volume justifies cost.

---

## 3. Proposed Feedback Taxonomy

### 3.1 Core categories (candidate set — validate with admins)

Group into **diagnostic buckets** that map to likely owners:

| Category | User-facing label (example) | Typical owner / lever |
|--------|------------------------------|------------------------|
| **Incorrect / hallucinated** | “Factually wrong or made up” | Retrieval, model, grounding, KB |
| **Outdated** | “Out of date vs current policy/UI” | KB freshness, versioned docs |
| **Not relevant** | “Doesn’t match my question or context” | Intent routing, prompts, scope |
| **Incomplete** | “Missing steps or prerequisites” | KB structure, answer templates |
| **Too verbose / too terse** | “Hard to scan” / “Not enough detail” | Response formatting, summarisation settings |
| **Data / visualisation issue** | “Chart or numbers seem wrong” | Query layer, chart spec, data freshness |
| **Action / workflow concern** | “I wouldn’t run this” / “Steps unsafe or unclear” | Action definitions, guardrails, agent planning |
| **Reasoning mismatch** | “Reasoning doesn’t match answer” | Chain-of-thought presentation, logging |
| **Performance / reliability** | “Too slow / failed / stopped” | Infra, timeouts, cancel semantics (may overlap non-feedback channels) |
| **Security / compliance flag** | “Sensitive or policy concern” | Security review, redaction, policy (handle with care—see §7) |

**Rules of thumb**

- **3–7 visible chips** at thumbs-down (merge synonyms in UI; map to finer internal codes if needed).
- Allow **multi-select** only if it stays rare (or use single-select + “Something else”).
- **Thumbs up:** optional single chip (“What worked?”) is enough for V1—e.g. **Clear, Fast, Accurate, Good chart, Saved time**—to avoid positive-class ambiguity.

### 3.2 Per-response-type considerations

| Response type | Extra or emphasised categories | Notes |
|---------------|-------------------------------|--------|
| **KB Q&A** | Outdated, Incomplete, Not relevant | Strong link to **article ID / citation** if the product surfaces sources (improves routing without PII). |
| **Data insights** | Data / visualisation issue, Not relevant (wrong metric/dimension) | Feedback should capture **which visual or table** (message id, widget id)—**automation** to attach context beats asking the user to describe the chart. |
| **Actions** | Action / workflow concern, Incorrect | Emphasise **safety** and **reversibility** language; consider mandatory **short reason** only for “security flag” (policy decision). |
| **Agentic workflows** | Incomplete, Action concern, Incorrect, Performance | Multi-step outputs may need feedback **per final message** or **per run**; avoid duplicate submission UX—pick one model and be consistent. |

---

## 4. UX Flow Recommendations

### 4.1 Principles

- **Default path stays one tap.** Anything beyond thumbs is **opt-in** except where policy explicitly requires more (e.g. security flag—stakeholder call).
- **Minimise cognitive load.** Show **only** chips relevant to response type (see §3.2).
- **Dismissible.** Escape / click-out / “Skip” closes the panel without nagging; **do not** show the same prompt again on every message in the session unless the user opts in.
- **No blocking on free text.** Free text is always optional for standard flows.

### 4.2 Thumbs down (recommended flow)

1. User taps **thumbs down** → brief inline expansion or bottom sheet: **“What went wrong?”** with **3–6 chips** (+ “Something else”).
2. **Optional:** If “Something else” or a chip that implies detail (e.g. Action concern) → single-line **optional** text field with placeholder **“Optional: what should we improve?”**
3. **Optional:** “**Include last user message and assistant reply**” checkbox **on by default** for enterprise debugging (with **short privacy notice** link)—or inverse: off by default in strict tenants; **configuration**, not one-size-fits-all.
4. Submit shows **immediate acknowledgement** (§5); sheet closes.

**Required fields:** Avoid requiring text for generic thumbs-down; it **suppresses volume**. If product needs minimum signal, require **one chip** only (still fast).

### 4.3 Thumbs up (recommended flow)

- **Default:** thumbs up records positive signal only (no second step)—maximises completion.
- **Optional expansion:** “What worked?” **1–3 chips** or single optional comment—collapsible or “Tell us more (optional).”

### 4.4 Regenerate / stop interactions

- **Stop/cancel** is not automatically “bad quality”; avoid conflating with thumbs down unless product explicitly ties them (usually **do not** auto-thumb-down on cancel).
- If user **regenerates** after thumbs down, treat as new assistant message; **feedback attaches to the message instance** that was rated.

### 4.5 Accessibility & speed

- Full keyboard path, visible focus, **ARIA** labels for chips; **no** heavy animations that delay submit.
- **Offline / error:** Queue locally with retry or show failure toast—enterprise networks flake; losing feedback silently erodes trust.

---

## 5. Closing the Loop

### 5.1 Immediate acknowledgement (testable)

- After submit: **short, honest confirmation**—e.g. “Thanks—this helps us improve IT Assist.” Avoid promising **human follow-up** unless a process exists.
- If **security flag** path: different copy—e.g. “Received. If this is urgent, contact [your internal channel].” (Exact routing is org-specific.)

### 5.2 Transparency boundaries

- **Do not** promise “we fixed your answer” unless there is a **defined remediation loop** (rare for generic KB).
- **Optional later:** Aggregated **“You’ve contributed N feedback items”** in settings—low priority unless admins ask for it.

### 5.3 Feedback history / status

- **V1 recommendation:** **No** per-user ticket-style status for each piece of feedback (high cost, privacy, expectation management)—unless product already has a **support ticket** integration.
- **Later:** Admin-only **export** or dashboard slice “my org’s feedback trends” for IT leads—distinct from end-user “status.”

---

## 6. Analytics & Improvement Pipeline

### 6.1 Product team dashboard (minimum useful slice)

- Volume over time: thumbs up/down, **chip distribution**, optional comment rate.
- Filters: **response type**, **feature area** (KB / insights / actions / agents), **app version**, **tenant** (for internal ops), **locale**.
- **Drill-down** to conversation/thread id with **redaction** rules for display (see §7).

### 6.2 Auto-flagging (automation-first)

- **Rules:** Spike in thumbs down on a **specific KB source id**, **query pattern**, or **action type** → alert channel (email/Slack/internal ticket).
- **Thresholds** configurable; start **conservative** to avoid alert fatigue.
- **LLM summarisation** of weekly negative themes: **optional** Phase 2+ when volume/cost justify; not required for V1.

### 6.3 Model / training data use

- Enterprise reality: **customer content may not be eligible** for model training. Default assumption: feedback is for **product analytics, KB updates, and prompt/tool tuning**, not for **foundation model fine-tuning**, unless legal/contracts explicitly allow.
- If training is allowed: **separate consent/banner** and **data class** tagging—do not conflate with operational logs.

### 6.4 Prioritisation signals

- Weighted score: thumbs + **severity tags** (e.g. security, action concern) + **repeat failures** on same intent cluster.
- Tie to **engineering metrics**: latency, error rate on same period to separate “model bad” from “system slow.”

---

## 7. Privacy & Security Considerations

### 7.1 What to collect (lean by default)

- **Always:** Reaction, **timestamp**, **message ids**, **response type**, **tenant/org id** (for enterprise routing), **app version**, **anonymised session id** where possible.
- **Optional (user or tenant controlled):** **Free text**, **screenshot**, **full prompt/response** payload for debugging.
- **Automatically attach** (with care): **cited KB ids**, **chart/query metadata** without raw fleet rows where possible.

### 7.2 What not to collect (unless strictly necessary and approved)

- **Secrets**, passwords, tokens, full **serial numbers** or **end-user PII** in clear text.
- **Raw export** of full fleet tables in feedback attachments—prefer **aggregates** and **internal ids** with RBAC.

### 7.3 Free-text PII handling

- **Placeholder copy** nudging admins not to paste credentials or personal data.
- **Server-side:** scanning/redaction pipeline (patterns for emails, IPs, etc.) **before** storage or dashboard display; **role-gated** access to raw fields.
- **Retention:** align with Copilot-style **bounded retention** for analyst-visible comments (e.g. 30–90 days) unless contract requires longer—**shorter** reduces risk.
- **Regional / tenant policies:** Some tenants will want **EU-only** storage or **disable** free text entirely—**feature flags** per tenant.

### 7.4 Security-flag path

- Ensure **RBAC** on who can view flagged items; consider **break-glass** audit log when viewing full content.

---

## 8. Recommended Scope for V1

**Build first (narrow, high leverage)**

1. **Thumbs down → single-step reason chips** (response-type-aware); optional one-line comment; **immediate thanks** acknowledgement.
2. **Server metadata capture:** message id, thread id, response type, chips, timestamps, tenant; **redaction** on free text at ingest (basic patterns).
3. **Internal dashboard v0:** counts, filters by response type and chip, drill-down with **redacted** view for analysts.
4. **Tenant/org controls:** master switch for **optional comment** and **strict** vs **standard** payload attachment (if attachment is offered at all).

**Phase 2**

- Thumbs-up optional “what worked” chips; **alerting rules** on spikes; export to SIEM/ticket webhook.
- **Per-message vs per-run** refinement for long agentic threads; saved **admin** views.

**Explicitly out of scope for “feedback enhancement” unless separately chartered**

- Full **public roadmap** tied to each submission; automatic **answer correction** in-thread; **gamification**—each creates expectation and cost beyond feedback capture.

---

## 9. Open Questions

1. **Legal / DPA:** Is any customer content in feedback eligible for **storage outside tenant boundary**? For **aggregated** analytics only?
2. **KB citations:** Does the UI always expose **stable source ids** for grounding? Without them, “wrong KB” routing stays manual.
3. **Actions/agents:** Should **negative feedback on an action proposal** trigger a **hard block** or **warning** recurrence for similar prompts—product risk decision.
4. **Identity:** Is feedback **per-user** identifiable to managers, or **aggregated only** for customer admins—impacts adoption honesty.
5. **Locale:** Will chips and prompts be **fully localised** at launch; if not, which markets first?
6. **Volume expectations:** Expected thumbs-down rate and volume—drives whether **LLM thematic summarisation** is worth cost in year one.
7. **Integration:** Should negative feedback create a **Support Ticket** or **Jira** item automatically—only if workflow ownership is clear.
8. **Reasoning toggle:** Should feedback explicitly ask **“Was reasoning helpful?”** as a separate toggle—orthogonal signal for debugging chain-of-thought UX.

---

*Document produced for requirements/story drafting. Validate taxonomy and policy-heavy items (§7, §9) with Legal, Security, and customer IT stakeholders before locking V1 scope.*
