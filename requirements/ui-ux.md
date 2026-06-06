# UI/UX Requirements

## Language And Localization
- German is the default UI language.
- English must be supported.
- UI text must be prepared for translation from the beginning.
- Dates, numbers, currencies, and units must render according to locale.
- Date fields that would normally default to today's date must use the user's browser date.
- Date inputs must prevent selecting future dates.
- Time horizon labels must use clear localized words, such as "1 Tag", "1 Woche", "1 Monat", "1 Jahr", "3 Jahre", and "10 Jahre" in German, and "1 day", "1 week", "1 month", "1 year", "3 years", and "10 years" in English.

## Product Surface
The first project phase focuses on a customer-presentable frontend. It should communicate the intended product clearly while remaining compatible with the future v1 API.

Approved first-demo scope:
- Build the first customer-presentable frontend for Community/Clerk users only.
- "V1 demo" means the first customer-presentable frontend demo, not the production v1 backend.
- Admin and Energy Consultant UI sections are not required in the first demo.
- Mocked login and generated/mock data are acceptable.
- The UI should appear feature-complete and operational from the clerk perspective.
- Mock behavior must use clean API-shaped interfaces to prepare for backend replacement.
- The first demo should show the provided Harsefeld logo in the application branding.

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
- Time-series graph / "Verlauf".
- Ratings and anomaly request.
- Actor controls and schedules as mocked clerk workflows.
- Report request/download for an imaginary Harsefeld 2026 report.
- Public overview and public reports.
- Object detail should include actor-control access for the selected object where actors exist.

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
- Admin personalization settings, including community logo configuration.

## Branding And Personalization
- Admin users must be able to configure a community logo for the product.
- The configured logo should appear consistently in authenticated UI, public UI, and reports where space and context allow.
- Logo presentation must not break responsive layouts or obscure navigation/status information.
- The first demo should use the provided Harsefeld logo as a fixed visual asset and should not expose Admin branding configuration.
- The first demo must use the provided Harsefeld PNG logo and should delete unused generated or invented logo assets.

## Graph And Drilldown Interaction
- Historic month rows should be clickable and open a graph focused on daily usage for that month.
- Summary metric cards such as "Strom", "Waerme", "Wasser", and "CO2" should be clickable and open the same graph component, focused on the last 12 months by default.
- The graph should be a separate authenticated tab named "Verlauf" in German.
- Metric and historic-row clicks should navigate to "Verlauf" with the clicked object, metric, period/date, horizon, and mode preselected.
- The graph screen should include a back button that returns to the previous authenticated screen.
- The graph component should support switching between cumulative and period-based views.
- The German labels for this toggle are approved as "Kumuliert" and "Pro Monat" for the month-based demo view.
- English labels must use clear wording, such as "Cumulative" and "Per month".
- The graph component must support horizon controls for one day, one week, one month, one year, three years, and ten years.
- The graph component must let users select individual days, weeks, months, or years depending on the current horizon/view.
- The graph component must include a date field where users can enter a focus date.
- The graph component should not include a redundant "Auswahl" dropdown.
- Graph labels must include years in week, month, and year views.
- Graph table alternatives must include the same year context as the visible graph labels.
- The same graph component should be reused for historic reading drilldowns and summary metric drilldowns.
- Graphs must include table/text alternatives for accessibility.

## Rating And Review Request Feedback
- The rating/anomaly request workflow must show immediate text feedback after a request is sent or updated.
- If a site/object has no open consultant review request, the primary action label should be "Anfrage senden" in German.
- If a site/object already has an open consultant review request, the primary action label should change to "Anfrage aktualisieren" in German.
- The screen should show a protocol/log above the request text field and action button.
- The currently selected object should expand and show its measurements again, including Strom, Wasser, Waerme, and CO2 where present.
- The protocol/log, request text field, and action button should appear directly below the expanded selected object and its measurements.
- Closed requests remain in the log; once closed, a new request may be opened.
- Rating rows and detail warnings should show an automatically generated status text first.
- After a consultant review request exists, a separate subtext should show request status while pending or the consultant's short assessment after response.
- Clicking the request/consultant subtext should reveal the full consultant answer when available.
- Object detail screens should show a dismissible top warning for non-green objects.
- The warning text should switch between automatic warning, request-in-progress state, and consultant short assessment depending on the review state.
- Clicking the warning should navigate to the rating screen with the object selected and the relevant request context visible.

## Control And Schedule Interaction
- Pending actor command acknowledgement dialogs should automatically cancel when the selected object changes.
- Pending schedule/timetable confirmation dialogs should automatically cancel when the selected object changes.
- Users should be able to edit all schedule/timetable fields exposed in the demo: name, days, time window, target label, and enabled status.

## Design Requirements
- Prioritize clarity and scanability for municipal users.
- Use traffic-light status consistently, with accessible labels and not color alone.
- Avoid exposing technical datapoint details to Community users unless needed.
- Provide clear confirmations for control actions.
- Provide clear error states for stale data, offline sites, failed imports, failed commands, and missing readings.
- Use responsive layouts for desktop and tablet-first municipal office use.
- Clickable metric cards, historic rows, and actor controls must have visible focus states and accessible names.
- Dark green primary buttons must use a global high-contrast white or off-white text color. This applies to report download/request buttons and review request buttons consistently.

## Accessibility
- Follow WCAG-aware design.
- Ensure keyboard usability for administrative forms.
- Ensure charts have text alternatives or tabular equivalents.
- Do not rely only on red/yellow/green color to communicate state.
