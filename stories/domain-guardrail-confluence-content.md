# Domain Guardrail — Fleet Management Chat Scope Restriction

## Summary
A pre-generation guardrail restricts chatbot responses to fleet management and IT asset topics. It blocks or redirects off-topic and out-of-capability queries before the main LLM call, reducing trust erosion, hallucinations, cost, and security risks.

## User problem / context
**Who is affected:** IT Admins using the fleet management chatbot.

**Problem:** Without a guardrail, the chatbot answers off-topic queries (e.g. recipes, general knowledge), causing:
- **Trust erosion** — users lose confidence when the bot answers irrelevant questions
- **Hallucinations** — off-topic answers increase fabrication risk
- **Unnecessary cost** — tokens and latency wasted on non-fleet queries
- **Security risks** — jailbreaking, prompt injection, compliance issues

**Two distinct cases:**
1. **Out-of-domain** — queries outside fleet management / IT assets
2. **In-domain, out-of-capability** — fleet topic but not a supported capability today (KB, data insights, actions, agentic workflows)

## Requirements

| ID | Requirement description |
|----|--------------------------|
| REQ-1 | Pre-generation domain classification (rules layer) — block obvious out-of-domain queries before LLM call. |
| REQ-2 | Pre-generation domain classification (lightweight classifier) — classify remaining queries; high-confidence out-of-domain → redirect without LLM call. |
| REQ-3 | Pre-generation domain classification (LLM fallback) — for low-confidence queries only; structured classification call before main LLM. |
| REQ-4 | Two-stage classification — Stage 1 domain check (IN_DOMAIN / OUT_OF_DOMAIN); Stage 2 capability routing (KB, DATA_INSIGHTS, ACTIONS, AGENTIC, UNSUPPORTED). |
| REQ-5 | Out-of-domain redirect — clear message; no generation attempt; no hint of future support. |
| REQ-6 | In-domain, out-of-capability redirect — softer message; list supported capabilities; invite retry within scope. |
| REQ-7 | Observability — log classification result, confidence score, and path taken (rules / classifier / LLM) for tuning and auditing. |
| REQ-8 | System prompt reinforcement — domain rules also enforced in system prompt as secondary layer. |

**Redirect messages:**
- **Out-of-domain:** "I can only assist with fleet management and IT asset questions."
- **In-domain, out-of-capability:** "I don't support that yet. Right now I can help with: KB Q&A, data insights, device actions, and agentic workflows."

## Out of scope
- Post-generation output filtering (phase 1)
- Automated model retraining
- UI redesign

## NFRs (if any)
- **Latency:** Rules layer: <1ms; lightweight classifier: 5–20ms; LLM fallback: 100–500ms (only for ~5–10% of traffic)
- **Cost:** Rules and classifier near-zero cost; LLM fallback minimised to uncertain cases only
- **Security:** Guardrail reduces exposure to jailbreaking and prompt injection by blocking off-topic flows early
