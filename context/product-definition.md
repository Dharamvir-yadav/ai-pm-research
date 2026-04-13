# Product Definition — Lenovo IT Assist

**Personas, market, competitors, and industry norms:** see **`context/industry-context.md`**. This file lists **product and platform identity** and **current capabilities only** (update after each release).

## Product & Platform

- **Product name**: **Lenovo IT Assist**, housed within the **Lenovo Device Orchestration** platform.
- **Parent platform**: Lenovo Device Orchestration includes: Dashboard, Device Management, Device Insights, **Lenovo IT Assist**, Support Tickets, Configurations & Settings. IT Assist is one module in this broader platform.

## Current Solution

The product today includes:

1. **KB (Q&A)** — "How to" question-and-answer over knowledge base. Responses include text, images, and data tables.
2. **Data insights** — Questions about the user's IT fleet (analytics, reporting). Responses include text, charts, and visualisations.
3. **Actions** — Initiating actions from the chatbot (e.g. system scan, system update, device onboarding).
4. **Agentic workflows** — Plan-and-execute agents (single or multi-flow); user manually triggers planning via a prompt today; the product is evolving toward more autonomous agents.
5. **Chatbot access** — The chatbot must be navigated to (e.g. from a dropdown in the platform nav); it is not integrated with all pages today. Integration across more pages is planned.
6. **Thread management** — Chat sessions are organised as named threads. The sidebar shows **Pinned threads** and **Recent threads**. Each thread supports: Rename, Pin, and Delete. Threads are already named (manually or auto-named).
7. **Reasoning** — Responses include a **"Show reasoning / Hide reasoning"** toggle. Reasoning is shown as a one-shot output at the end (not live-streamed); it guides the user on how the answer was derived.
8. **Pre-canned prompts** — The chatbot home page shows suggested prompt tiles (e.g. "How many expired warranties are in my fleet?"). Users can also access **Explore** and **Favourite prompts** from the input bar.
9. **Smart suggestions (Recommendations)** — After a response, follow-up prompt suggestions are shown. These are currently **not personalised** — they are a simple semantic match against a prompt store.
10. **In-progress state** — A "Processing your request…" indicator is shown while a response is being generated. Currently a **UI facade only** (not tied to backend progress stages). A **stop/cancel button** is visible during processing.
11. **Response feedback** — Thumbs up / thumbs down feedback is available on responses. Already live.
