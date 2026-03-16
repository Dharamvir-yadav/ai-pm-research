# Base Features Screenshots

This folder contains screenshots of the **current application** for **visual reference only**.

They are used by the `generate-bolt-prompt` agent to extract:
- **Color palette** — primary, secondary, background, and text colors used in the UI.
- **Layout patterns** — navigation structure, sidebar, chat panel placement, component spacing.
- **Chatbot use cases** — how the three current use cases appear in the UI today (KB Q&A, Data insights, Actions).

## What to put here

| File | What it shows |
|------|---------------|
| `Parent_application_landing page.png` | This is parent application homepage where chatbot it housed |
| `Dropdown on landing page.png` | This is the parent page navigation through dropdown. "LITA" AI Chatbot is one of the options in the dropdown to navigate to the AI bot |
| `Device_management_page_system_update_view` | Page under "Device management" showing list of available system updates |
| `Device_management_page_device_view.png` | Page under "Device management" showing list of device. Use can select one or more devices to act on it |
| `chatbot_home_page.png` | This is chatbot home page. Notice precanned prompts which can be clicked to trigger. There are sections for favourite prompts and exfiend prompts|
| `KB_prompt_response.png` | This is view of KB prompt and its reponse. Output supports text, image and data table|
| `Data_insights_prompt_response.png` | This is view of data insights prompt. It support text and visuals. Notice the Recommendations which are smart suggestions based on previous pormpts and responses|
| `Prompt_in_progress.png` | View of in progress prompt processing|
| `thread_level_feature.png` | These are chat thread level features|

Add more screenshots as the UI evolves. Keep filenames descriptive.

## What this folder is NOT for

- **Not a source of requirements or business rules.** For project context and boundaries, see `.cursor/rules/00-project-context.mdc`.
- **Not a design system or spec.** Screenshots are for visual pattern extraction only.
- **Not updated automatically.** Refresh screenshots when the UI changes significantly.
