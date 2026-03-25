# AI-Powered Dynamic Dashboards — Platform Capability

## Summary

Enable AI-powered dynamic dashboard creation as a **platform capability** within Lenovo Device Orchestration. IT Admins create personalised dashboards using natural language or manual widget selection, and can publish them for the organisation. Built on a three-layer architecture — NL-to-Data Engine, Widget Specification, and Platform Chart Renderer — designed for reuse across any platform module.

## User Problem / Context

The current Dashboard is static — fixed widgets, same view for every IT Admin regardless of role or priorities. IT Assist (LITA) already generates charts from natural language, but those insights live in chat threads and cannot be persisted.

- Different roles need different views (procurement → warranties, security → compliance, ops → uptime). The static dashboard serves none of them well.
- ~72% of users export to Excel when dashboards don't meet their needs (Luzmo). 43% of IT teams spend 10+ hours/week on manual endpoint tasks (Automox 2026).
- AI-driven dashboard creation is emerging in enterprise platforms (ServiceNow, Datadog) but not yet standard in device/fleet management — an opportunity for differentiation.

---

## Architecture — Three-Layer Model

This capability is a **platform service** — any module (Dashboard, Device Management, Reports) can consume it.

### NL → JSON → UI Rendering

```
┌─────────────────────────────────────────────────────────────────────┐
│                        BACKEND (Server-side)                        │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  LAYER 1: NL-to-Data Engine (LITA Core)                      │  │
│  │  ┌─────────────┐    ┌──────────────┐    ┌────────────────┐   │  │
│  │  │ NL Input    │ →  │ LLM interprets│ →  │ Queries data   │   │  │
│  │  │ "Show me    │    │ user intent   │    │ layer, builds  │   │  │
│  │  │  warranty   │    │ + maps to     │    │ structured     │   │  │
│  │  │  expirations│    │ widget catalog│    │ response       │   │  │
│  │  │  by group"  │    │              │    │                │   │  │
│  │  └─────────────┘    └──────────────┘    └───────┬────────┘   │  │
│  │                                                  │            │  │
│  │                          Outputs: JSON Widget Specification   │  │
│  └──────────────────────────────────────────────────┼────────────┘  │
│                                                     │               │
│  ┌──────────────────────────────────────────────────▼────────────┐  │
│  │  LAYER 2: Widget Specification (Platform JSON Contract)       │  │
│  │                                                               │  │
│  │  {                                                            │  │
│  │    "component": "BarChart",                                   │  │
│  │    "title": "Warranty Expirations by Group",                  │  │
│  │    "xAxis": "deviceGroup",                                    │  │
│  │    "yAxis": "count",                                          │  │
│  │    "data": [{"deviceGroup": "Group_1", "count": 23}, ...],   │  │
│  │    "filters": [{"field": "location", "type": "select"}]      │  │
│  │  }                                                            │  │
│  │                                                               │  │
│  │  Library-agnostic. Describes WHAT to render, not HOW.         │  │
│  └──────────────────────────────────────────────────┬────────────┘  │
└─────────────────────────────────────────────────────┼───────────────┘
                              JSON sent to frontend   │
                                                      ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       FRONTEND (Client-side)                        │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  LAYER 3: Platform Chart Renderer Component                   │  │
│  │  Lives in: Shared Platform UI Library (e.g. @lenovo/charts)   │  │
│  │                                                               │  │
│  │  ┌─────────────────┐   ┌─────────────────────────────────┐   │  │
│  │  │ Spec Parser     │   │ Component Catalog                │   │  │
│  │  │ Reads widget    │ → │ BarChart  → renders bar chart    │   │  │
│  │  │ spec JSON,      │   │ PieChart  → renders pie chart    │   │  │
│  │  │ looks up        │   │ Gauge     → renders gauge        │   │  │
│  │  │ component type  │   │ CountCard → renders count card   │   │  │
│  │  │ in catalog      │   │ Table     → renders data table   │   │  │
│  │  └─────────────────┘   │ ...                              │   │  │
│  │                         │                                  │   │  │
│  │                         │ Internally uses a visualisation  │   │  │
│  │                         │ library (implementation detail)  │   │  │
│  │                         └─────────────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Imported by: Dashboard, Device Management, Reports, any module     │
└─────────────────────────────────────────────────────────────────────┘
```

**Where the renderer lives:** The Platform Chart Renderer is a **shared frontend UI library** (package) imported by any module. It contains chart component implementations, the spec parser, and the component catalog. The visualisation library used internally is an implementation detail — consumers interact only with the widget spec.

---

## Requirements

Requirements are organised by phase. Each phase is incrementally deliverable and builds on the previous.

### Phase 1 — Platform Foundation + Personal Dashboards

**Value delivered:** IT Admins can create personal dashboards using NL or manual widget selection. The three-layer platform architecture is established and reusable.

| ID | Requirement |
|--------|--------------------------|
| REQ-1 | **NL-to-Visualisation Platform Service & Component Catalog.** LITA's NL-to-data engine shall be available as a shared platform service. It accepts a natural language query + user context (permissions, org), maps intent to a component catalog of available widget types (bar chart, pie chart, line chart, gauge, count card, data table, etc.), and returns structured data + a widget specification JSON. The catalog defines what types exist and their properties; the NL engine targets only catalog-listed components. |
| REQ-2 | **Widget Specification Contract.** The platform shall define a library-agnostic JSON schema that describes visualisations — component type, data mapping, title, filters, refresh policy, layout metadata. This is the contract between backend and frontend. Widget specs shall be validated against the catalog schema on both backend (before sending) and frontend (before rendering). Invalid specs are rejected with a user-friendly error, never rendered with incorrect data. |
| REQ-3 | **Platform Chart Renderer Component.** A shared frontend UI component library shall read widget specifications and render them using chart components. The visualisation/charting library powering this component is an implementation detail behind the abstraction — consumers never import it directly. **The specific visualisation library shall be researched and selected by engineering** based on: LLM compatibility (JSON config easily generated by LLMs), licensing (open-source preferred for platform-wide use), rendering performance (thousands to tens of thousands of data points), framework flexibility, chart type coverage (bar, line, pie, gauge, table, count cards, tree at minimum), and enterprise maturity. |
| REQ-4 | **NL Input Component on Dashboard.** The Dashboard page shall include a natural language input component ("What do you want to see?") for creating and modifying widgets. This is a focused creation tool — not a chatbot or conversation thread. |
| REQ-5 | **Personal Dashboards with Widget Management.** Users shall be able to create, save, and load personal dashboards that persist across sessions. Widgets can be added via NL input or from a widget library (drag-and-drop). Widgets can be rearranged, resized, and configured per-widget (filters, chart type, title) where applicable. The saved state is the collection of widget specs + layout positions. Widgets refresh on dashboard load by default. Users may enable **live refresh** (auto-refresh at a configurable interval) per widget or per dashboard, with a visible disclaimer that live refresh may impact performance on dashboards with many widgets. |
| REQ-6 | **Data Access & Security.** Widgets and LITA Data Insights shall use the same data layer — same semantic model, metrics, and access controls. Row-level security (RLS) shall be enforced per user's permissions (org, device group, role). A user cannot create or view a widget for data they are not authorised to access. |
| REQ-7 | **NL Resilience & Graceful Degradation.** When the NL engine cannot fulfil a request (ambiguous query, unsupported question, hallucination), the system shall provide a clear fallback — suggested alternatives, error message, or prompt to refine. If the NL platform service is unavailable, saved dashboards shall still load from persisted widget specs, and the widget library shall remain functional. Only the NL input becomes unavailable. |

### Phase 2 — Organisation Publishing (Simple)

**Value delivered:** Teams can share useful dashboards. Governance starts simple — permission-based publishing, no approval workflow.

**Why start without approval workflows:** In early adoption, the publishing user base is small (admins/stewards). Permission-based control (only users with "Dashboard Publisher" role can publish) is sufficient and avoids adding workflow complexity before there is volume to govern. Approval workflows are introduced in Phase 3 when publishing scales and trust/quality controls become necessary.

| ID | Requirement |
|--------|--------------------------|
| REQ-8 | **Dashboard Publishing.** Users with the "Dashboard Publisher" role (or Admin) shall be able to publish a personal dashboard for the organisation. The published dashboard is visible to the org or to a selected audience. Publishing creates a snapshot — changes to the user's personal dashboard do not automatically propagate to the published version. |
| REQ-9 | **Dashboard Gallery & Discovery.** Published dashboards shall be discoverable via a gallery with name, description, owner, and tags. Users can search and browse. |
| REQ-10 | **Dashboard Copy.** Users shall be able to copy an org-published dashboard to their personal space and customise it. The copy is independent — changes to the original do not propagate. |

### Phase 3 — Governance & Refinement

**Value delivered:** Enterprise publishing controls. Smarter dashboard creation for returning users.

| ID | Requirement |
|--------|--------------------------|
| REQ-11 | **Publishing Governance.** Published dashboards shall support: (a) an optional approval workflow (Submit → Reviewer approves → Published), configurable per tenant; (b) role-based audience targeting — publishers can target "Security Admins", "Procurement", "All IT", etc., with discoverability filtering by user's role; (c) endorsement — dashboards can be marked "Recommended" or "Certified" to surface trusted content; (d) audit logging of publish, approve, and revoke actions (who, what, when). |
| REQ-12 | **Smart Defaults & Templates.** The system shall offer dashboard templates and role-based smart defaults — pre-populated dashboard layouts based on user role (e.g. Security Admin → compliance widgets) or fleet profile. Users can accept, modify, or discard suggestions. |

### Phase 4 — AI-Generated Dashboard Summaries

**Value delivered:** AI explains what the dashboard is showing in plain language — users get context without interpreting every chart.

| ID | Requirement |
|--------|--------------------------|
| REQ-13 | **AI-Generated Natural Language Summaries.** The system shall generate plain-language summaries of dashboard state (e.g. "Your fleet health improved 5% this week", "12 devices have critical updates pending in South Room"). Summaries can be shown as a dashboard-level digest or per-widget annotation. Summaries are refreshed when the dashboard loads or when the user requests an update. |

---

## Architectural Consideration: A2UI Protocol

[A2UI](https://a2ui.org/) (Agent to UI) is a Google-created, Apache 2.0 licensed protocol for agent-driven interfaces. Agents send declarative JSON messages describing UI components; clients render using their own native components — no executable code.

**Why it's relevant:** A2UI's architecture mirrors the three-layer model above — Agent (Layer 1), Messages (Layer 2), Renderer with Catalog (Layer 3). Key features that align: declarative-only (no code execution), custom catalogs (allowlisted components), LLM-friendly flat JSON, framework-agnostic, two-phase validation.

**Current maturity (March 2026):** v0.8 stable, v0.9 draft. Renderers for Angular, Flutter, Lit. React renderer not yet officially available. Some documentation incomplete. No public enterprise production case studies.

**Recommendation:** Design the Widget Specification (REQ-2) following A2UI's structural patterns — flat component lists, ID references, data binding via paths, catalog-driven validation. This makes the architecture **A2UI-compatible** without formally adopting the protocol. When A2UI reaches production readiness for the platform's frontend framework, migration cost will be low. Formal adoption to be revisited at that point.

---

## Out of Scope

- **Custom SQL or ad-hoc query builder**: Widgets use governed data sources via NL engine, not free-form SQL.
- **Dashboard embedding outside LDO**: Lenovo Device Orchestration (LDO) is the first consumer of this platform capability. Embedding dashboards in external applications is out of scope for now; the platform architecture supports broader adoption by other consumers in the future.
- **Anomaly detection & proactive widget suggestions**: Not planned in the current phases. May be revisited in the future based on demand.
- **Visualisation library selection**: Engineering decision per REQ-3 criteria.
- **A2UI formal adoption**: Architectural consideration only. Deferred to maturity assessment.

---

## NFRs

| Area | Target |
|------|--------|
| **Dashboard load (saved, up to 12 widgets)** | ≤ 2.5 seconds. Dashboards with more widgets use lazy loading to stay under 4 seconds. |
| **NL-to-widget (end-to-end)** | ≤ 5 seconds from user submit to widget visible. Progressive feedback ("Generating your chart...") within 500ms. |
| **Interaction responsiveness** | ≤ 200ms for any dashboard interaction (filter, drag, menu). |
| **Security** | Widget spec validated on both backend and frontend. Published dashboards enforce that the audience has permission to view the underlying data. |

---

*Requirements use stable IDs (REQ-1 through REQ-13) for traceability to Jira stories.*
