# Auto-Rename Chat Threads — Feature Research

**Feature:** Automatically rename chat threads/sessions based on the user's prompts and responses.

**Context:** Thread = named conversation session (like ChatGPT sidebar history), persists across visits. Planned/upcoming concept. Naming triggers after first AI response. Fully automatic with user able to manually rename.

---

## 1. Problem Statement

### Why IT Admins need named chat sessions

IT Admins using the fleet management Gen AI chatbot run **multiple types of queries** in parallel or over time:

- **KB Q&A** — "How to configure VPN for remote users"
- **Data insights** — "Show me devices with low disk space in EMEA"
- **Actions** — "Run a system scan on device XYZ"
- **Agentic workflows** — "Plan and execute a patch rollout for Windows 10"

Without named sessions, the session list shows "New Conversation" or meaningless IDs. This causes:

1. **Conversation hunting** — Users must click through each session to find the one they need. Full-text search helps but is often ineffective when the topic shifted or keywords don't match.
2. **Cognitive friction** — Scanning a list of identical or near-identical labels is slow and error-prone.
3. **Lost context** — Long-running agentic workflows or multi-step investigations become hard to resume; users can't quickly identify "that scan I started yesterday" vs "the VPN KB query from last week."
4. **Reduced return rate** — ChatOllama reports ~23% increase in returning to previous conversations when titles are meaningful vs generic.

### Pain from unnamed/auto-numbered sessions

- **Auto-numbered** (e.g. "Session 47", "Chat 2025-03-10-14:32") — No semantic signal; users rely on timestamps and memory.
- **First-prompt-as-title** (e.g. Microsoft Copilot before March 2025) — Long prompts truncate poorly; short prompts ("help", "?") are useless; PII in prompts can leak into titles.

**Bottom line:** Named sessions reduce "conversation hunting" time, improve discoverability, and align the session list with the user's mental model of what each conversation was about.

---

## 2. How ChatGPT and Similar Products Do It

### ChatGPT

- **Process:** Two **parallel** requests when the user sends the first message:
  1. Message goes to a "Generate Conversation Title" agent
  2. Message goes to the main model for the response
- **Input:** First user message (and sometimes first AI response) used for title generation.
- **Model:** Typically a cheaper model (e.g. GPT-3.5-turbo) for titles, not the active chat model.
- **Fallback:** "New Conversation" if title generation fails.
- **User control:** User can manually rename at any time.

### Claude (Anthropic)

- **Claude.ai:** Auto-generates titles similar to ChatGPT (implied from feature parity).
- **Claude Code / VS Code:** Manual rename only via `/rename`; no auto-naming. Multiple feature requests exist for auto-generated titles after first exchange.

### Microsoft Copilot (M365)

- **Before March 2025:** Title = first prompt text (often poor quality).
- **After March 2025:** LLM-generated title after first Copilot response. User can manually rename or delete. Rollout: early–late March 2025.

### Google Gemini

- Auto-generates descriptive titles from conversation content, similar to ChatGPT.
- Manual renaming supported.
- Session browser shows auto-generated titles, creation dates, message counts, first-message preview.

### Trade-offs

| Approach | Cost | Latency | Accuracy | Notes |
|---------|------|---------|----------|-------|
| Separate LLM call (parallel) | +&lt;2% conversation cost if cheap model | No user-facing delay | High | ChatGPT pattern; use cheap model |
| Same model as chat | Can double cost per conversation | Same | High | Avoid |
| Truncation only | Zero | Zero | Low for vague prompts | Fallback |
| Template-based | Near zero | Zero | Medium | Depends on intent/entity quality |

**Recommendation:** Use a cheap model for title generation, or avoid an extra LLM call where possible (see §3).

---

## 3. Naming Strategies — Which Is Best for This Product?

The product already has **intent classification** and **capability routing** (KB, DATA_INSIGHTS, ACTIONS, AGENTIC, UNSUPPORTED). This creates an opportunity for **template-based** or **hybrid** naming without a dedicated LLM call in many cases.

### Option A: LLM summarisation

- **Input:** First user prompt + first AI response.
- **Output:** 3–6 word title (e.g. "VPN setup for remote users").
- **Pros:** High quality, handles varied prompts.
- **Cons:** Extra LLM call (~&lt;2% cost if cheap model), latency, PII risk if not sanitised.

### Option B: Truncation of first prompt

- **Input:** First user message, truncated to N chars (e.g. 50).
- **Pros:** No extra call, zero latency.
- **Cons:** Poor for "help", "?", long prompts, or prompts with PII.

### Option C: Template-based (intent + entities)

- **Input:** Intent (KB, DATA_INSIGHTS, ACTIONS, AGENTIC) + extracted entities (e.g. "VPN", "device scan", "EMEA").
- **Examples:** "KB: VPN setup", "Data: Low disk EMEA", "Action: System scan", "Agentic: Patch rollout".
- **Pros:** No extra LLM call, fast, predictable, audit-friendly.
- **Cons:** Quality depends on entity extraction; may be generic.

### Option D: Hybrid (recommended)

1. **Primary:** Use intent + entity extraction to build a template title (e.g. "KB: {topic}", "Action: {action_type} – {target}").
2. **Fallback:** If template yields a weak title (e.g. "KB: help" or "Action: ?"), call a cheap LLM for summarisation.
3. **Final fallback:** "Chat – {date}" or "New conversation – {date}".

**Conclusion:** A hybrid approach leverages existing classification and reduces cost. LLM is used only when template-based naming would be poor. For enterprise (cost, speed, security), prefer automation first, AI as fallback.

---

## 4. When Exactly to Rename

### Confirmed: After first AI response

Trigger when the first AI response is available. Do not trigger on first user message alone (insufficient context).

### First response is short or generic

If the first response is "Sure, let me look that up…" or "I'll help with that.", the **first substantive response** (e.g. first response with real content) is a better trigger. Options:

- **A:** Use first AI response regardless — simpler, may produce weak titles.
- **B:** Wait for first "substantive" response (e.g. length threshold, or first response after tool/agent output) — better quality, more complex.

**Recommendation:** Start with (A) for simplicity; refine to (B) if user feedback indicates poor titles from generic first responses.

### Multiple user messages before first response

If the user sends rapid follow-ups before the first AI response (e.g. "help" then "actually I mean VPN"):

- **Option:** Use the **first user message** only for consistency with ChatGPT.
- **Alternative:** Concatenate all user messages before first response — more context, more tokens/cost.

**Recommendation:** Use first user message only; keep scope narrow and predictable.

### Agentic workflows (long-running)

For plan-and-execute flows, the "first response" may be a plan or a "I'm working on it" message. Title generation should still trigger after the first AI response. The title may reflect the initial ask (e.g. "Agentic: Patch rollout plan") rather than the final outcome. Acceptable for v1; dynamic re-titling is out of scope initially.

---

## 5. Edge Cases

| Edge case | Recommendation |
|-----------|----------------|
| **Very short/vague first prompt** ("help", "?", "hi") | Fallback to "Chat – {date}" or "New conversation – {date}". Do not use prompt as title. |
| **PII in first prompt** (device serials, usernames) | Sanitise before sending to LLM or before display. Use regex/entity detection to redact or replace with placeholders (e.g. [DEVICE_ID]). Enterprise requirement. |
| **User manually renames session** | Do **not** auto-rename again. Treat manual rename as user override; respect it. |
| **Long thread, topic has shifted** | Out of scope for v1. Static title from first exchange. Future: optional dynamic re-titling with user control. |
| **Session with no AI response yet** | No title until first AI response. Show "New conversation" or similar placeholder. |
| **Title generation fails** | Fallback to "Chat – {date}" or "New conversation – {date}". |
| **Multi-topic thread** | Title reflects first exchange only. No multi-topic summarisation in v1. |

---

## 6. Automation vs AI

### Can existing signals generate titles without an LLM call?

**Yes, for many cases.** Intent classification (KB, DATA_INSIGHTS, ACTIONS, AGENTIC) plus entity extraction (topics, targets, regions) can produce template titles:

- "KB: {topic}" — e.g. "KB: VPN setup"
- "Data: {query_summary}" — e.g. "Data: Low disk EMEA"
- "Action: {action} – {target}" — e.g. "Action: Scan – Device XYZ"
- "Agentic: {goal}" — e.g. "Agentic: Patch rollout"

Entity extraction may already exist or can be lightweight (keywords, regex for common patterns). If not, a small set of rules or a lightweight model could suffice.

### When is an LLM call needed?

- Vague prompts where template yields "KB: help" or "Action: ?"
- Prompts that don't map cleanly to intent
- When template-based title would be misleading or unhelpful

### Cost and latency

- **Template-based:** Negligible cost, no added latency.
- **LLM fallback:** Use cheap model (e.g. GPT-3.5-turbo equivalent); &lt;2% of conversation cost if optimised. Run async so user does not wait.
- **Piggyback on response:** Possible but adds complexity; separate call is cleaner and allows different model.

---

## 7. Enterprise Considerations

| Consideration | Recommendation |
|---------------|-----------------|
| **Searchability** | Thread names should be searchable in session history. Store in search index. |
| **Auditability** | Store and log thread names (with PII redacted if applicable). Support compliance and forensics. |
| **Shared sessions** | If multiple admins can see a session: define who can rename (e.g. creator, or any viewer). Document in requirements. |
| **Title length** | 50–60 characters max. Truncate or summarise to fit. |
| **Localisation** | Generate titles in the language of the user's prompt when possible. Support at least the product's supported locales. |
| **PII in titles** | Never surface PII in thread names. Sanitise before storage and display. |

---

## 8. Requirements (REQ-THREAD-01, REQ-THREAD-02, …)

| ID | Requirement |
|----|--------------|
| **REQ-THREAD-01** | The system SHALL automatically generate a thread title after the first AI response in a new session. |
| **REQ-THREAD-02** | The system SHALL use a hybrid naming strategy: template-based (intent + entity extraction) as primary, with LLM summarisation as fallback when the template would produce a weak or generic title. |
| **REQ-THREAD-03** | The system SHALL fall back to "Chat – {date}" or equivalent when the first prompt is too short/vague, or when title generation fails. |
| **REQ-THREAD-04** | The system SHALL sanitise PII (e.g. device IDs, usernames) from thread names before storage and display. |
| **REQ-THREAD-05** | The system SHALL NOT auto-rename a thread after the user has manually renamed it. |
| **REQ-THREAD-06** | Thread titles SHALL be limited to 50–60 characters. |
| **REQ-THREAD-07** | Thread titles SHALL be searchable in session history. |
| **REQ-THREAD-08** | Thread titles SHALL be stored and logged for auditability (with PII redacted). |
| **REQ-THREAD-09** | The user SHALL be able to manually rename a thread at any time. |
| **REQ-THREAD-10** | When the first AI response is not yet available, the session SHALL display a placeholder (e.g. "New conversation") until the title is generated. |
| **REQ-THREAD-11** | Title generation SHALL run asynchronously so it does not block or delay the user-facing response. |
| **REQ-THREAD-12** | Thread titles SHALL be generated in the language of the user's prompt when the product supports that locale. |

### Out of scope (v1)

- Dynamic re-titling as conversation topic shifts
- Multi-topic or periodic title updates
- Shared session rename permissions (can be deferred if shared sessions are not yet implemented)

---

## Summary

IT Admins need named sessions to avoid "conversation hunting" and to quickly find past KB queries, data insights, actions, and agentic workflows. The product's existing intent classification enables a **hybrid** approach: template-based titles from intent + entities first, with LLM fallback for weak cases. This keeps cost and latency low while meeting enterprise needs for searchability, auditability, and PII safety. Trigger after the first AI response; respect manual renames; handle edge cases with clear fallbacks.

---

*Research complete. Awaiting user sign-off before handover to publish_confluence agent.*
