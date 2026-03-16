# Bolt Prompt Template

This template defines the structure and quality instructions for bolt.new prompts. The `generate_bolt_prompt` agent fills this template from stories/research and the base application prompt.

---

## Tech stack (hardcoded — do not ask)
React + Tailwind CSS + Vite. Clean, component-based structure. No backend required for prototype.

---

## Mode A — From scratch (full application + new feature)

Include all of the following sections in the prompt:

1. **App overview:** Lenovo IT Assist — fleet management Gen AI chatbot for IT Admins within Lenovo Device Orchestration. Enterprise-grade look and feel. (Use `bolt-prompts/base-app-prompt.md` as the detailed base; reference or inline it.)
2. **Color palette:** From `base-app-prompt.md` or extracted from screenshots.
3. **Base screens and navigation:** From `base-app-prompt.md` (sidebar, thread list, home page, input bar, response anatomy, in-progress state).
4. **Base chatbot capabilities (always protect these):** Read from `context/product-definition.md`, section "Current Solution". The key capabilities to always protect are:
   - KB Q&A — How-to question-and-answer (text, images, tables)
   - Data insights — Fleet analytics and reporting (text, charts, visualisations)
   - Actions — Device actions from the chat
   - Agentic workflows — Plan-and-execute flows
5. **New feature:** Full description of the feature to add, derived from stories/research. Include key interactions, states, and edge cases.
6. **Do not modify guard:** Explicitly instruct bolt not to break or modify the base capabilities listed above.

---

## Mode B — Existing UI in bolt (delta-only)

Include all of the following sections in the prompt:

1. **Existing app (brief grounding):** Summarise `bolt-prompts/base-app-prompt.md` in 3–5 lines. Do NOT ask bolt to rebuild it.
2. **Add the following feature:** Full description of the new feature (from stories/research). Include interactions, states, edge cases.
3. **Do not modify guard:** Explicitly instruct bolt to leave all existing screens, navigation, and base chatbot capabilities (KB, Data insights, Actions, Agentic) unchanged. Only add what is described.

---

## Quality instructions (always include in both modes)

- Use clean, reusable React components.
- Use Tailwind CSS for all styling. Keep the enterprise feel (professional, minimal, accessible).
- Do not add placeholder lorem ipsum content — use realistic IT Admin / fleet management data (e.g. "Device: LENOVO-LAPTOP-001", "Status: Offline").
- Make the prototype interactive enough to demonstrate the new feature flow end-to-end.
