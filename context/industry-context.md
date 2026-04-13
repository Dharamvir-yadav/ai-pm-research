# Industry context — Lenovo IT Assist

**Customize this file** when forking the repo for another product. Keep it aligned with **`context/product-definition.md`** (product identity and capabilities).

---

## Industry & domain

- **Vertical:** IT **fleet** and **IT asset / endpoint management** in **enterprise** context.
- **Research and requirements** should stay inside this problem space unless the user explicitly expands scope in chat.

## Industry snapshot

- Enterprise IT orgs centralize **device lifecycle**, **compliance**, and **service operations** across large fleets.
- **ITSM and ITAM** tooling often integrates with endpoint management; buyers expect **auditability**, **role-based access**, and **multi-tenant** or **org-boundary** safety.
- **AI assistants** in this space are judged on **trust**, **action safety**, **latency**, and **grounding** in fleet data and KB—not generic chat quality alone.
- **Regulated industries** (finance, healthcare, public sector) amplify requirements for **logging**, **data residency**, and **change control**.
- **Cost and operational load** of LLM-backed features matter next to simpler automation where automation suffices.

## Industry norms (best practices)

- Apply **norms and common practices** from **IT fleet, IT asset management, and adjacent enterprise endpoint management** when researching and writing requirements.
- Do **not** substitute vague “best practices” from unrelated domains (e.g. consumer apps, unrelated B2B verticals) for domain-appropriate judgment.

## Personas & jobs-to-be-done (examples)

**Primary persona — IT Admin** (aligns with product; expand segments here as needed.)

| Persona | Example JTBD |
|--------|----------------|
| **IT Admin** | Answer fleet health and inventory questions quickly without switching tools. |
| **IT Admin** | Trigger or guide **actions** (e.g. scan, update, onboard) with clear audit trail and guardrails. |
| **IT Admin** | Use **KB and data insights** together to explain “why” and “how many” for incidents and planning. |
| **IT Operations lead** | Compare options and vendor patterns when evolving **agentic** or **automated** workflows safely. |

*(Add or replace rows for your organization.)*

## Example enterprise customer archetypes

*Illustrative profiles only—not named customers.*

- **Global manufacturer** — multi-site Windows fleet, compliance-driven patching, central ITAM.
- **Financial services** — strict access control, emphasis on audit logs and approved change paths for any automated action.
- **Professional services / hybrid workforce** — mix of corporate and mobile endpoints; needs fast self-service answers from KB + fleet data.

## Research toggle — SMB / mid-market comparables

**Consider SMB / mid-market comparables for inspiration:** **yes**

- **yes** — You may use **small / medium / startup** products in the same problem space for **ideas and UX patterns** only; label them **non-enterprise / inspiration**, not like-for-like enterprise comparables.
- **no** — Restrict market scan for comparables to **enterprise** lists below only; do not use SME products as research inputs.

## Key competitors — enterprise (direct: fleet / ITAM / endpoint)

*Primary like-for-like market scan targets. Replace when your vertical changes.*

- **ServiceNow ITAM / Virtual Agent** — IT service management with AI assistant capabilities
- **Ivanti Neurons** — IT asset management with AI-driven automation
- **Tanium** — Endpoint management and security with conversational interfaces
- **ManageEngine (Zoho)** — IT asset and endpoint management suite
- **Freshservice (Freshworks)** — IT service management with AI features (Freddy AI)
- **Microsoft Intune / Copilot** — Endpoint management with Copilot integration

## Key competitors — enterprise (AI / assistant patterns, not fleet-specific)

*Enterprise AI UX and workflow patterns relevant to assistant features.*

- **Microsoft Copilot Studio / 365 Copilot** — Enterprise AI assistant platform
- **ServiceNow Now Assist** — Generative AI across ITSM workflows
- **Intercom Fin** — AI customer support agent (relevant for feedback, resolution patterns)

## Key competitors — small / medium / startup (inspiration only)

*Use only when **Research toggle** is **yes**. Label as **non-enterprise / inspiration** in research output.*

- **Lansweeper** — IT asset discovery and inventory (often mid-market)
- **Snipe-IT** — Open-source IT asset management (lighter-weight / SMB–mid patterns)
- *(Add others your team tracks.)*
