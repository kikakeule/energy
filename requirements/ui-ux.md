# UI/UX Requirements

## Language And Localization
- German is the default UI language.
- English must be supported.
- UI text must be prepared for translation from the beginning.
- Dates, numbers, currencies, and units must render according to locale.
- Date fields that would normally default to today's date must use the user's browser date.
- Date inputs must prevent selecting future dates.
- Time horizon labels must use clear localized words, such as "1 Tag", "1 Woche", "1 Monat", "1 Jahr", "3 Jahre", and "5 Jahre" in German, and "1 day", "1 week", "1 month", "1 year", "3 years", and "5 years" in English.

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
- The graph component must support horizon controls for one day, one week, one month, one year, three years, and five years.
- The graph component must let users select individual days, weeks, months, quarters, or years depending on the current horizon/view.
- The three-year and five-year graph views should show quarters, not one bar per year.
- The three-year graph view shows 12 quarters; the five-year graph view shows 20 quarters.
- Clicking a graph value should navigate to the next useful detail level, including month-to-day drilldown and quarter-to-containing-year drilldown.
- The graph component must include a date field where users can enter a focus date.
- The graph component should not include a redundant "Auswahl" dropdown.
- The graph screen must include manual dropdown selection for village, object type, object, and measurement, in that order.
- Village and object type default to "all"; the object dropdown is filtered by both and sorted alphabetically.
- The object dropdown should include "Alle Objekte" for portfolio-level aggregate views.
- The measurement dropdown offers only measurements available for the current object selection.
- Hovering a graph field on desktop should show its value and unit.
- On mobile/touch devices, tapping a graph value navigates instead of opening a hover tooltip; mobile-specific value preview behavior is a later UX TODO.
- Month and day graph views should use compact spacing so daily or hourly values remain usable on smaller screens.
- Graph labels must include years in week, month, quarter, and year views.
- Graph table alternatives must include the same year context as the visible graph labels.
- The same graph component should be reused for historic reading drilldowns and summary metric drilldowns.
- Graphs must include table/text alternatives for accessibility.

## Rating And Review Request Feedback
- The rating/anomaly request workflow must show immediate text feedback after a request is sent or updated.
- If a site/object has no open consultant review request, the primary action label should be "Anfrage senden" in German.
- If a site/object already has an open consultant review request, the primary action label should change to "Anfrage aktualisieren" in German.
- The screen should show a protocol/log above the request text field and action button.
- When a ratings object is selected, it should expand and show its measurements again, including Strom, Wasser, Waerme, and CO2 where present.
- The ratings screen must not auto-select the first object when entered normally.
- If the user arrives from an object-detail warning, the relevant object should expand automatically.
- The expanded rating detail should include a small close button on the right side of the expanded fields.
- The rating badge/icon and explanation text should use stable aligned columns so rows align even when status labels have different widths.
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
- Timetables should show a compact read-only view by default.
- A row edit icon should open edit mode for a timetable row; saving returns to read-only view.
- Edit mode should provide an X icon to cancel without saving.
- Timetable edit forms should split "Zeitfenster" into start and end fields.
- Timetable edit forms should include a controlled-actor dropdown with checkboxes.
- Timetable actor selection may select multiple actors only when they have the same actor type; incompatible actor types are greyed out once an actor type is selected.
- The "Ziel" field should be a dropdown populated from the selected actor's allowed actions, or the common allowed actions when multiple same-type actors are selected.

## Navigation, Filters, And Sorting
- On small screens where navigation moves to the top, the menu must include an arrow control to minimize or expand it; the label may be visible when the full menu text is visible and must hide when menu text is hidden.
- The top menu should automatically minimize after changing to another page.
- On regular desktop/tablet layouts, users should be able to hide or show menu text and keep an icon-only navigation rail for the current session; the toggle label should follow the same visibility rule as the other menu labels.
- Portfolio and ratings views should share filters for village, object type, and rating.
- Portfolio and ratings filters should be hidden behind a title-level "Filter" button, with active selections summarized in smaller text below the button.
- Filter dropdowns should fit on one row where space allows; compact checkbox options should sit below the dropdowns.
- Portfolio and ratings filters must include a "show critical objects even if not selected by filter" option that includes red/critical objects only.
- The German UI wording should use "Kritische Objekte" instead of "Rote Objekte" for this filter.
- The control view should not show the shared filter panel in the first demo; it should use cascaded object selection only.
- Portfolio/rating filter state should persist while users navigate between portfolio and ratings views.
- Sorting options should include alphabetical, rating, type, village, and CO2 consumption.
- Sorting direction should be combined into the sort dropdown option where direction applies, such as "Alphabetisch up/down", "Ort up/down", and "CO2 up/down".
- Alphabetical, village, and CO2 sorting support ascending and descending order.
- Type sorting groups objects by type label and sorts objects alphabetically inside each type.
- Village sorting orders villages alphabetically and then orders objects alphabetically inside each village.
- Rating sorting always places red first, then yellow, then green.
- CO2 sorting places objects without CO2 values at the bottom in both directions.
- Object selectors outside ratings should use cascaded dropdowns: village, object type, then object.
- Cascaded village and object type dropdowns default to "all"; object options are filtered and sorted alphabetically.

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
