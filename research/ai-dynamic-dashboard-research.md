# Research: AI-Powered Dynamic Dashboards — Platform Capability

## Summary

This research assesses the feasibility and value of making the Lenovo Device Orchestration Dashboard dynamic using AI. The core direction: build **NL-to-Dashboard as a platform capability** — an NL input component on the Dashboard page that uses LITA's core NL engine (extracted as a shared platform service) to generate visualizations. Users can create personal dashboards and publish them for the organization.

The focus is on **user-problem first**, **honest separation of AI vs simple automation**, and **platform-level architecture** that any module can leverage — not a feature locked inside IT Assist.

---

## 1. Effectiveness Assessment

### 1.1 IT Admin Pain Points with Static Dashboards

**Evidence from industry and user behaviour:**

| Pain Point | Evidence |
|------------|----------|
| **Manual reporting burden** | 43% of IT teams spend 10+ hours/week on manual endpoint tasks; only 17% have a unified dashboard showing end-to-end patch status (Automox 2026 State of Endpoint Management). |
| **Visibility gaps at scale** | At thousands of devices, admins miss firmware mismatches, offline fleet portions, and lack audit trails for configuration changes. |
| **One-size-fits-all** | Static dashboards show the same widgets to everyone. Procurement admins care about warranties; security admins care about compliance; ops admins care about uptime. No role-based tailoring. |
| **Ad-hoc questions** | Long tail of one-time investigations (e.g. "devices with warranty expiring in 30 days in South Room") require either IT Assist queries or manual exports — no persistent view. |
| **Dashboard bypass** | ~72% of users reportedly export to Excel when dashboards don't meet expectations (Luzmo). |

**For Lenovo Device Orchestration specifically:** The current Dashboard shows Total Devices, Device Connectivity, Current Issue Summary, System Update status, Overall Health Score, and Current Alerts & Events. These are useful defaults but fixed. IT Assist already answers natural language questions and returns charts (e.g. "Provide me a pie chart of total device groups in my fleet?") — yet those insights live only in chat threads, not on a persistent dashboard.

### 1.2 Industry Patterns: AI-Driven Dashboards

| Vendor | Approach | What AI Does |
|--------|----------|--------------|
| **ServiceNow** | Data Visualization generation (Now Assist for Creator) | Natural language → create visualizations; requires semantic layer and governed metrics. |
| **Datadog** | Bits AI + App Builder | Natural language → generate complete apps (UI, actions, logic) mapped to data; iterative refinement via chat. |
| **Splunk** | ML-SPL, Anomaly Detection App | Anomaly detection dashboards via ML commands; not NL-to-dashboard. |
| **Microsoft Intune** | Power BI + Data Warehouse | No native AI dashboard; custom dashboards via Power BI, Graph API, Log Analytics. Intune's built-in dashboard is fixed; customization is external. |
| **Flexera One** | Customizable Management Dashboard | Add/remove/rearrange widgets; save as templates; no AI — pure configuration. |

**Takeaway:** AI-driven dashboard creation is emerging (ServiceNow, Datadog) but not yet standard in device/fleet management. Most device management platforms (Intune, Flexera) offer **configurable** dashboards, not AI-generated ones. The opportunity: Lenovo already has LITA's NL-to-data capability — extracting it as a platform service and surfacing it on the Dashboard page creates a differentiated, AI-native experience.

### 1.3 Realistic Benefits vs Hype

| Benefit | Realistic? | Notes |
|---------|------------|-------|
| **Faster dashboard creation** | Yes | NL-to-dashboard can reduce time from days to minutes for first draft; iteration still needed. |
| **Role-based defaults** | Yes | AI can suggest widgets based on role/fleet profile; rule-based logic can also do this. |
| **Anomaly surfacing** | Yes, but narrow | ML anomaly detection is proven (Splunk, Datadog); requires clear metrics and thresholds. |
| **"AI optimizes my layout"** | Uncertain | Usage-based suggestions (e.g. "add widget X") are plausible; automatic rearrangement is less proven and may annoy users. |
| **Replacing drag-and-drop entirely** | No | Many users prefer explicit control. NL is best for **initial creation** and **suggestions**; fine-tuning should remain manual. |

**Honest assessment:** AI adds the most value for (1) **first-draft generation** from natural language, (2) **smart defaults** based on role/context, and (3) **anomaly highlighting**. It does **not** replace the need for a solid **widget library** and **drag-and-drop layout** — those are table stakes. AI accelerates discovery and setup; configuration handles precision.

---

## 2. AI's Role — Where AI Adds Real Value vs Simple Automation

### 2.1 Where AI Adds Real Value

| Capability | AI Value | Why |
|------------|----------|-----|
| **Natural language to dashboard** | High | "Show me a dashboard for warranty expiration tracking" → AI maps intent to widgets (warranty expiry list, count by group, timeline). User types into an NL component on the Dashboard page itself — no context switching to IT Assist. |
| **Smart defaults / suggestions** | High | Pre-populate based on: user role (e.g. Security Admin → compliance widgets), past queries, fleet profile (e.g. large fleet → performance widgets). Requires minimal model logic; high perceived value. |
| **Anomaly surfacing** | Medium–High | "Unusual spike in BSOD in South Room" → suggest adding a BSOD-by-location widget or highlight in existing widget. Needs defined metrics and anomaly detection (statistical or ML). |

### 2.2 Where Simple Automation / Configuration Suffices (No AI Needed)

| Capability | Approach | Why |
|------------|----------|-----|
| **Add/remove/rearrange widgets** | Drag-and-drop builder | Standard UX; no AI. |
| **Widget library** | Catalog of pre-built widgets | Total Devices, Connectivity, Issue Summary, etc. — same data as current static dashboard, configurable. |
| **Save layout** | Save/reset preferences | Pure configuration. |
| **Filter by device group, date range** | Filter controls | Standard; no AI. |
| **Publish approval flow** | Workflow (e.g. submit → approve → publish) | Governance logic; no AI. |
| **Role-based access to published dashboards** | RBAC | Permission model; no AI. |

### 2.3 Where AI Is Overkill

| Idea | Recommendation |
|------|----------------|
| **AI rearranges my dashboard automatically** | Skip. Users expect control; auto-rearrangement can feel intrusive. |
| **AI writes custom SQL for every widget** | Avoid. Use governed data sources and pre-defined widget types; NL maps to those, not ad-hoc queries. |
| **AI suggests widgets on every visit** | Use sparingly. Occasional "Based on your recent queries, consider adding X" is fine; constant prompts are noise. |

### 2.4 Summary: AI vs Automation

- **AI:** NL-to-dashboard (on Dashboard page), smart defaults, anomaly surfacing.
- **Automation/Config:** Widget library, drag-and-drop, filters, save, publish workflow, RBAC.

---

## 3. Platform Architecture — Three-Layer Model

### 3.1 Design Principle: Platform Capability, Not Solution Feature

The NL-to-Dashboard capability must be built as a **platform service** within Lenovo Device Orchestration — not a feature tied to IT Assist or any single module. This means:

- The NL-to-visualization engine is extracted from LITA as a **shared platform service** that any module can consume.
- The Dashboard page has its own **NL input component** ("What do you want to see?") — a focused creation tool, not a chatbot.
- Other modules (Device Management, Reports, future modules) can leverage the same service for their own visualization needs.

### 3.2 Three-Layer Architecture

```
┌──────────────────────────────────────────────────┐
│  Layer 1: LITA Core — NL-to-Data Engine          │
│  (Shared platform service)                       │
│  NL input → structured data + chart intent       │
│  Uses LITA's existing NL capabilities            │
└──────────────────────┬───────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────┐
│  Layer 2: Widget Specification (Platform Contract)│
│  Library-agnostic JSON schema describing:        │
│  - Chart type, data mapping, title, filters      │
│  - Data source reference + refresh policy        │
│  - Layout metadata (size, position)              │
└──────────────────────┬───────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────┐
│  Layer 3: Platform Chart Renderer Component      │
│  <PlatformChart spec={widgetSpec} />             │
│  Reads widget spec → renders via charting library│
│  Charting library is an internal implementation  │
│  detail, abstracted behind this component        │
└──────────────────────────────────────────────────┘
```

**Layer 1 — LITA Core (NL-to-Data Engine):**
LITA's NL engine is already capable of interpreting user questions, querying the data layer, and returning structured data with visualizations. For the platform capability, this engine is extracted as a shared service. It receives an NL query and returns: structured data + a chart intent (visualization type, series mapping, axes, etc.) expressed as a widget specification.

**Layer 2 — Widget Specification (Platform Contract):**
A defined, library-agnostic JSON schema that describes what to render without referencing any specific charting library. This is the **platform API contract**. LITA produces it; any consumer (Dashboard page, Device Management, Reports) reads it and renders. The spec includes: chart type, data mapping (fields → axes/series), title, filters, refresh policy, and layout metadata.

**Layer 3 — Platform Chart Renderer Component:**
A shared UI component that takes a widget specification and renders it using a charting/visualization library. The library is an **internal implementation detail** — consumers interact only with the widget spec, never with the library directly. This abstraction allows the library to be swapped or upgraded without affecting any consumer.

### 3.3 Visualization Library

**Action required:** The specific visualization/charting library to power the Platform Chart Renderer component needs to be researched and selected by the engineering team. Key selection criteria:

- **LLM compatibility:** The library's configuration format should be easily generated by LLMs (JSON-based, well-documented, widely known).
- **Licensing:** For a platform capability used across modules and teams, open-source / permissive licensing is preferred to avoid per-developer commercial license costs at scale.
- **Rendering performance:** Must handle datasets typical of fleet management (thousands to tens of thousands of data points) without degradation.
- **Framework flexibility:** Should work across frontend frameworks (or at minimum, the platform's primary framework) to support platform-level reuse.
- **Chart type coverage:** Must support the visualization types needed for IT fleet management — bar, line, pie, gauge, table, count cards, tree/hierarchy at minimum.
- **Enterprise maturity:** Active maintenance, strong community, production stability.

The three-layer architecture ensures this is a contained decision: the library sits behind the `<PlatformChart>` component and can be changed without impacting any consumer of the widget spec.

### 3.4 How It Plays Out on the Dashboard Page

1. User is on the Dashboard page. An NL input component is available ("What do you want to see?").
2. User types: "Show me warranty expirations by device group."
3. Request goes to LITA Core (shared platform NL-to-data service).
4. LITA returns structured data + widget spec (chart type: bar, x-axis: device group, y-axis: count, filter: expiry window).
5. Dashboard's `<PlatformChart>` component reads the spec and renders the visualization.
6. User can adjust (change chart type, add filter, resize, reposition) — these modify the widget spec, not library internals.
7. User saves — the widget spec is persisted; re-rendered on next load using the same spec.

### 3.5 UX Boundary: Creation Tool, Not Chatbot

The NL component on the Dashboard page is a **creation tool** — short, focused interactions for adding/modifying widgets. It is explicitly **not** a chatbot or conversation thread. Users type an intent, get a widget, confirm or adjust, done. If they want multi-turn exploration, Q&A, or agentic workflows, they go to IT Assist.

---

## 4. Personal Dashboards

### 4.1 How Personal Dashboard Creation Works

**Flow:**

1. **Create** → User creates a new personal dashboard (blank or from template/smart default).
2. **Add widgets** → Via NL component on the Dashboard page ("add a warranty expiry widget") **or** from widget library (drag-and-drop).
3. **Arrange** → Drag to reorder/resize.
4. **Configure** → Per-widget filters (device group, date range) where applicable.
5. **Save** → Dashboard is saved to user's personal space; persists across sessions.

**Primary entry point:** Dashboard module — "Create dashboard" or "Customize" on the Dashboard page.

### 4.2 Widget Types for IT Fleet Management

Based on current Dashboard + Data Insights + industry (Flexera, TeamDynamix, Infraon):

| Category | Widget Types | Data Source |
|----------|--------------|-------------|
| **Device counts** | Total devices, Active/Licensed/Unlicensed, By group, By category | Device inventory |
| **Connectivity** | Online/Offline, Uptime | Device telemetry |
| **Issues** | BSOD, High CPU Apps, Storage, Batteries (counts, trends) | Issue/event data |
| **Updates** | Critical/Recommended/Optional (counts, % of fleet) | System update status |
| **Health** | Overall Health Score (gauge) | Health aggregation |
| **Alerts & Events** | Current alerts list, Event timeline | Alerts/events |
| **Warranty** | Expiring soon, By group, Renewal timeline | Warranty data |
| **Compliance** | Policy compliance status | Policy engine |

**MVP widget set:** Start with widgets that mirror current static dashboard + warranty (high user demand) + NL-generated custom widgets via the platform service.

### 4.3 Shared Data Model with LITA

Widgets and LITA's Data Insights must use the **same data layer** — same semantic model, metrics definitions, and access controls. This is an architectural requirement, not optional. It ensures:

- A widget showing "devices with expiring warranties" uses the same metric definition as a Data Insights query asking the same question.
- Data access permissions are enforced consistently (a user cannot create a widget for data they cannot access).
- No divergence in numbers between Dashboard and IT Assist.

---

## 5. Publishing for Organization

### 5.1 Governance: Who Can Publish? Review/Approval?

| Aspect | Recommendation |
|--------|----------------|
| **Who can publish** | Configurable: e.g. users with "Dashboard Publisher" or "Admin" role. Default: restrict to admins/stewards. |
| **Approval flow** | Optional but recommended for enterprise: Submit → Reviewer approves → Published. |
| **Scope** | Published dashboards visible to org (or to a chosen audience, e.g. security team). |
| **Audit** | Log who published what, when; who approved. |

### 5.2 Discoverability

| Mechanism | Description |
|-----------|-------------|
| **Dashboard gallery / catalog** | List of org-published dashboards with name, description, owner. |
| **Endorsement** | Mark dashboards as "Recommended" or "Certified" to surface trusted content. |
| **Search** | Search by name, tags, or description. |
| **Role-based suggestions** | "Dashboards for your role" or "Popular in your org." |

### 5.3 Forking / Copy

Allow users to **copy** an org dashboard to their personal space and customize. Original remains unchanged; user's copy is independent. Avoid true "fork" semantics (linked updates) for MVP — add later if needed.

### 5.4 Role-Based Published Dashboards

Support role-aware publishing:

- Publisher can target "Security Admins," "Procurement," "All IT" etc.
- Discoverability filters by user's role.
- Example: "Security Admin Dashboard" appears for users with security role; "Procurement Dashboard" for procurement.

**Implementation:** Use existing RBAC; add "audience" or "role" metadata to published dashboards.

---

## 6. Implementation Approach

### 6.1 Phased Approach

| Phase | Scope | AI Involvement |
|-------|-------|----------------|
| **Phase 1 (MVP)** | NL input component on Dashboard page. Platform NL-to-visualization service (extracted from LITA Core). Widget library + drag-and-drop. Personal dashboards (create, arrange, save). Three-layer architecture (LITA Core → Widget Spec → Platform Chart Component). | AI: NL-to-dashboard via LITA Core. |
| **Phase 2** | Smart defaults (role-based, fleet-profile-based). Dashboard templates. Iterative refinement of NL-generated dashboards. | AI for context-aware suggestions. |
| **Phase 3** | Org publishing: submit, approval, gallery, discoverability, fork/copy. Role-based audience targeting. | No new AI; governance and UX. |
| **Phase 4** | Anomaly surfacing: highlight unusual patterns, suggest widgets. Usage-based optimization suggestions. | AI for anomaly detection and usage-based recommendations. |

### 6.2 Architecture Considerations

| Concern | Recommendation |
|---------|----------------|
| **Data access** | Widgets use same data layer as LITA Data Insights. Enforce row-level security (RLS) by user/org/device group. |
| **Permissions** | Dashboard visibility follows user's data permissions. User cannot add widget for data they cannot access. |
| **Performance** | Widgets should support lazy load, pagination, and caching. Avoid N+1 queries; batch widget data where possible. |
| **Security** | Published dashboards: validate that publisher has permission to share underlying data; audit publish/approve actions. |
| **Visualization library** | Must be researched and selected by engineering. Criteria defined in Section 3.3. Library sits behind `<PlatformChart>` abstraction. |

### 6.3 Integration Points

| Integration Point | How |
|-------------------|-----|
| **LITA Core** | NL engine extracted as shared platform service. Dashboard and IT Assist both consume it. |
| **Data Insights** | Shared semantic layer and data model. Same metrics, same access controls. |
| **Agentic workflows** | No direct integration for MVP. Future: "Add workflow status to dashboard" (e.g. deployment progress). |
| **Other modules** | Device Management, Reports, etc. can consume the platform NL-to-visualization service and `<PlatformChart>` component for their own needs. |

### 6.4 Key Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| **NL engine extraction complexity** | LITA's NL-to-data capability must be cleanly separable into a shared service. If tightly coupled to the chatbot UI, extraction may require significant refactoring. Assess coupling early. |
| **Dashboard proliferation** | Governance: limit personal dashboards per user; require naming conventions for published. |
| **Stale data** | Widget refresh policy (e.g. on load, or every N minutes); user-controlled for heavy widgets. |
| **AI hallucination in NL-to-dashboard** | Map NL to governed widget types and data sources only; no free-form query generation. Validate widget config before render. |
| **Performance with many widgets** | Limit widgets per dashboard (e.g. 12–20); lazy load; background refresh. |
| **Scope creep** | Phase strictly. MVP = NL component + widget library + personal dashboards. Defer org publishing and anomaly to later phases. |
| **Platform adoption by other modules** | Build the three-layer architecture with clear APIs and documentation. If only Dashboard uses it, the "platform capability" claim is hollow. Plan at least one additional module integration in Phase 2–3. |

---

## 7. Out of Scope (Explicit)

- **Real-time streaming dashboards** (e.g. live device events): Current scope is periodic refresh.
- **Custom SQL or ad-hoc query builder**: Widgets use governed data sources via the NL engine, not free-form SQL.
- **Dashboard embedding in external apps**: In-scope is within Lenovo Device Orchestration only.
- **AI-generated natural language summaries of dashboard** (e.g. "Your fleet health improved 5% this week"): Phase 4 or later; not MVP.
- **Specific visualization library selection**: To be researched and decided by engineering based on criteria in Section 3.3.
- **Pin from IT Assist as primary mechanism**: The primary dashboard creation path is the NL component on the Dashboard page. Pin-from-IT-Assist may be considered as a secondary convenience feature in a future phase.

---

## 8. Open Questions for Product Decision

1. **Default dashboard:** When a user first gets personal dashboards, do they see the current static dashboard as read-only, or as an editable "My Dashboard" they can customize?
2. **Widget limit:** Max widgets per dashboard? (Suggestion: 12–20 for performance.)
3. **Approval workflow:** Mandatory for all org publishes, or configurable per tenant?
4. **NL component scope:** Should the NL component support only widget creation, or also widget modification (e.g. "change this to a line chart")?
5. **LITA Core extraction:** How tightly coupled is the current NL-to-data engine to the IT Assist chatbot? What is the effort to extract it as a shared service?
6. **Multi-module adoption:** Which module beyond Dashboard should be the first additional consumer of the platform NL-to-visualization service?

---

## 9. Summary: Recommendations

| Recommendation | Rationale |
|----------------|-----------|
| **Build as platform capability, not solution feature** | NL-to-visualization as a shared service; any module can consume. Compounds value across the platform. |
| **NL component on Dashboard page as primary creation path** | User stays in context; dashboard-native UX; no context switching to IT Assist. |
| **Three-layer architecture (LITA Core → Widget Spec → Chart Component)** | Clean separation: data generation, specification contract, rendering. Library is replaceable; spec is the contract. |
| **Visualization library: to be researched by engineering** | Criteria defined (LLM compatibility, licensing, performance, framework flexibility). Decision is contained behind the `<PlatformChart>` abstraction. |
| **Widget library + drag-and-drop alongside NL** | Table stakes for manual control. NL accelerates; drag-and-drop handles precision. |
| **Defer org publishing to Phase 3** | MVP focuses on personal dashboards + NL creation. Publishing adds governance complexity. |
| **Defer anomaly surfacing to Phase 4** | Requires ML/metrics infrastructure; validate demand first. |

---

*Research output is usable for requirements and stories. When satisfied, hand over to **publish_confluence** agent for Confluence requirement page creation.*
