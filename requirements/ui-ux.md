# UI/UX Requirements

## Language And Localization
- German is the default UI language.
- English must be supported.
- UI text must be prepared for translation from the beginning.
- Dates, numbers, currencies, and units must render according to locale.

## Product Surface
The first project phase focuses on a customer-presentable frontend. It should communicate the intended product clearly while remaining compatible with the future v1 API.

Approved first-demo scope:
- Build the first customer-presentable frontend for Community/Clerk users only.
- "V1 demo" means the first customer-presentable frontend demo, not the production v1 backend.
- Admin and Energy Consultant UI sections are not required in the first demo.
- Mocked login and generated/mock data are acceptable.
- The UI should appear feature-complete and operational from the clerk perspective.
- Mock behavior must use clean API-shaped interfaces to prepare for backend replacement.

## Role-Based Experience
- Admin UI can expose setup and configuration complexity.
- Community UI must be clean, simple, and limited to common workflows.
- Community Admin UI may expose automations, schedules, CSV import, and organization tools.
- Energy Consultant UI must focus on estimates, anomaly requests, findings, and report release.
- Guest/Public UI must be accessible without login and read-only.

## Core Screens
First customer-presentable frontend demo should include:
- Mocked login.
- Portfolio overview.
- Site/building detail.
- Current and historic readings.
- Ratings and anomaly request.
- Actor controls and schedules as mocked clerk workflows.
- Report request/download for an imaginary Harsefeld 2026 report.
- Public overview and public reports.

Later authenticated role screens should include:
- Admin datapoint and user setup views.
- Consultant report review view.
- Community Admin configuration views.

Full product frontend should eventually include:
- Rating overview.
- Anomaly marking / request consultant flow.
- Actor control view.
- Automation and schedule editor.
- Report request/download view.

## Design Requirements
- Prioritize clarity and scanability for municipal users.
- Use traffic-light status consistently, with accessible labels and not color alone.
- Avoid exposing technical datapoint details to Community users unless needed.
- Provide clear confirmations for control actions.
- Provide clear error states for stale data, offline sites, failed imports, failed commands, and missing readings.
- Use responsive layouts for desktop and tablet-first municipal office use.

## Accessibility
- Follow WCAG-aware design.
- Ensure keyboard usability for administrative forms.
- Ensure charts have text alternatives or tabular equivalents.
- Do not rely only on red/yellow/green color to communicate state.
