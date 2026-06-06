# V1 Demo Handoff

## Purpose
Build the first customer-presentable frontend demo for the municipal energy management product. In this context, "v1 demo" means the first frontend demo, not the production v1 backend.

The demo must feel feature-complete from a Community/Clerk perspective while using mock/generated data and API-shaped interfaces that can later be replaced by the real backend.

## Repositories
- Main coordination/deployment repo: `https://github.com/kikakeule/energy`
- Frontend repo: `https://github.com/kikakeule/energy-frontend`
- Backend repo: `https://github.com/kikakeule/energy-backend`

The main repo owns requirements, docs, Docker Compose, deployment configuration, and submodules for frontend/backend. The frontend application lives in `energy-frontend`. The backend application lives in `energy-backend`.

## Required First-Demo Scope
- Community/Clerk-level experience only.
- Admin, Community Admin, and Energy Consultant UIs are out of scope for the first demo.
- Login may be mocked.
- Readings, ratings, reports, weather, actor control, and schedules may be mocked.
- Mocked behavior must sit behind clean API-shaped adapters/interfaces.
- UI should look operational and feature-complete from the clerk perspective.
- The demo should show the provided Harsefeld PNG logo as fixed branding.
- Do not use an invented or hand-drawn replacement logo; move the provided logo into a normal public/static frontend asset location and remove unused generated logo assets.
- Admin personalization UI is still out of scope, but the demo should demonstrate the resulting branded experience.
- Demo fields that normally use today's date should use the user's browser date.
- Date inputs must not allow future dates.

## Demo Screens
Required first-demo screens:
- Mocked login.
- Portfolio overview.
- Site/building detail.
- Current and historic readings.
- Time-series graph / "Verlauf".
- Ratings and anomaly request.
- Actor controls and schedules as mocked clerk workflows.
- Report request/download for an imaginary Harsefeld 2026 report.
- Public overview and public reports.

Object detail should include actor-control access for the selected object where actors exist.

Do not build Admin or Energy Consultant screens for the first demo unless a later requirement explicitly changes scope.

## Demo Data
Use Samtgemeinde Harsefeld-style fictional mock data for 2026. The data should include the required object types:
- schools;
- town halls / administrative offices;
- libraries;
- fire departments;
- traffic lights;
- pumping stations;
- gyms / sports halls;
- kindergartens / daycare facilities;
- public pools.

Optional objects can include street lighting, public buildings, community halls, and other municipal assets.

The data should be clearly fictionalized and must not imply real current values.

## Ratings
Rating source precedence:
1. Use Energy Consultant thresholds/estimates when available.
2. Otherwise use historical percentile-based rating when sufficient history exists.
3. Otherwise show grey/unrated.

History-based rating:
- green: below historical 75th percentile;
- yellow: 75th percentile up to 95th percentile;
- red: above 95th percentile.

Open details not blocking the demo:
- exact historical comparison window/dataset;
- exact data-completeness threshold;
- simple prediction/trend model.

For the demo, use sensible mock values and expose grey/unrated states where data is intentionally incomplete.

Rating/anomaly request behavior:
- sending or updating a request must show immediate text feedback;
- if there is no open consultant review request, the primary action is "Anfrage senden";
- if there is an open consultant review request, the primary action changes to "Anfrage aktualisieren";
- one site/object may have one open review request until the Energy Consultant closes it;
- updates are appended to the open request instead of creating parallel duplicate requests;
- closed requests stay in the protocol/log, and a new request may be opened afterwards;
- the demo should include mocked existing request data so the protocol/log and update behavior are visible.
- the API-shaped request model should include consultant short assessment and full assessment fields;
- rating rows should show automatic status text first, then request status or consultant short assessment after a request exists;
- clicking request/consultant subtext should show the full consultant answer where available;
- the selected rating object should expand and show Strom, Wasser, Waerme, and CO2 measurements;
- the request log, text field, and button should appear directly below the selected object and measurements;
- object detail should show a dismissible warning for non-green objects, and clicking it should open the rating screen in context.

## Graph Drilldowns
- Historic month rows should open a graph focused on daily usage for the selected month.
- Summary metric cards for electricity, heat, water, and CO2 should open the same graph component, focused on the last 12 months by default.
- The graph should be a separate authenticated tab named "Verlauf".
- Metric/history clicks should navigate there with the clicked field preselected and a back button to return to the previous view.
- Remove the redundant graph "Auswahl" dropdown.
- The graph should support cumulative and period-based views.
- The German toggle labels for the month-based demo view are "Kumuliert" and "Pro Monat".
- English labels should use clear words, such as "Cumulative" and "Per month".
- The graph should support clear horizon labels for one day, one week, one month, one year, three years, and ten years.
- Users should be able to select individual days, weeks, months, or years depending on the current horizon/view.
- The graph should include a focus date field.
- Week, month, and year graph labels and table rows should include the year.
- The graph should include a table/text alternative.

## Weather / DWD
DWD weather integration is required for v1 and should be represented in the demo.

Implementation preference:
- Use real DWD data in the demo if practical.
- If real DWD fetching is too much for the first frontend-only demo, implement an API-shaped mock behind the same interface.
- Demo deployment may set site weather location through Docker Compose configuration.
- In the full product, Admin users configure weather location per site.

## Reports
- First demo should offer a mocked downloadable imaginary Harsefeld 2026 energy report.
- First demo report branding should use the provided Harsefeld PNG logo.
- The generated PDF must not draw boxes or panels over the logo.
- Report output is PDF only for initial scope.
- Configurable templates are a future product direction but Admin/Consultant template configuration is not required for the clerk-only demo.
- Public reports hide site-level details by default.

## Actor Control And Schedules
- V1 demo only demonstrates actor-control intent in the UI.
- No real device control.
- No production safety guarantees.
- UI may show allowed actions, confirmations, schedules, and mocked success feedback.
- Pending actor command and schedule/timetable confirmation windows should automatically cancel when the selected object changes.
- Demo users should be able to edit all exposed timetable fields: name, days, time window, target label, and enabled status.
- Detailed command history, control failure simulation, and live device feedback are not required unless needed visually.
- Real actor-control availability and safety requirements are v2.

## Deployment
- The main `energy` repository consumes `energy-frontend` and `energy-backend` via Git submodules.
- Docker Compose is the default from-scratch deployment path.
- The local demo builds the application image from the checked-out `energy-frontend` submodule and tags it locally.
- Private repository access is handled by authorized host-side Git clone/submodule setup before Compose runs.
- The default Docker build should not receive GitHub credentials.
- Prefer building from source through Docker Compose for the demo.
- Avoid GHCR unless prebuilt private images become necessary.
- GHCR remains the optional private registry for prebuilt images, with strict cleanup/retention.
- Self-hosted private Docker Registry is the quick fallback if GHCR quota, pricing, or policy becomes a problem.

## Implementation Notes
- German is the default UI language; English must be supported.
- Use accessible traffic-light statuses with text labels, not color alone.
- Keep UI clean and clerk-focused.
- Keep mock data and service interfaces shaped like future backend APIs.
- Use a global high-contrast text style for dark green primary buttons so report and rating request buttons remain readable.
- Do not overbuild v2/v3 features during the first demo.

## Source Requirements
Before implementation, read:
- `AGENTS.md`
- `requirements/overview.md`
- `requirements/features.md`
- `requirements/ui-ux.md`
- `requirements/reporting.md`
- `requirements/integrations.md`
- `requirements/deployment.md`
- `doc/project-splitting-and-stack.md`
