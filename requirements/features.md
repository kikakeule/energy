# Feature Requirements

## Overview And Monitoring
- Show current consumption across the community portfolio.
- Show current readings and historic readings per site, building, datapoint, category, and medium.
- Allow users to open reusable time-series graphs from historic readings and summary metric cards.
- Historic month entries should drill down to daily usage for the selected month.
- Summary metric cards such as electricity, heat, water, and CO2 should drill down to the same graph component, focused on the last 12 months by default.
- The time-series graph should be a separate authenticated screen/tab named "Verlauf" in German.
- Clicking a metric card or historic row should navigate to the graph screen with the clicked object, medium, date/period, horizon, and mode preselected.
- The graph screen must include a back button that returns to the previously active view.
- Time-series graphs must support cumulative and period-based views where meaningful.
- Time-series graphs must support clear time horizon labels for one day, one week, one month, one year, three years, and five years.
- Time-series graphs must allow selecting specific days, weeks, months, quarters, or years based on the current horizon/view.
- The three-year graph view must show 12 quarters instead of three single annual bars.
- The five-year graph view must show 20 quarters and replaces the earlier ten-year view.
- Clicking a graph value should drill down to the next useful view: a month goes to the selected month view, a day/week value goes to the relevant smaller time view where available, and a quarter in the three-year or five-year view goes to the year view containing that quarter.
- Time-series graphs must include a focus date field where users can enter a specific date.
- Date fields that represent "today" or the current working date should default to the user's browser date.
- Users must not be able to select future dates in date fields.
- Graph labels and table alternatives must include the year for week, month, quarter, and year views so period context is unambiguous.
- The graph must not include a separate "Auswahl" dropdown if the same selection is already represented by click navigation, horizon controls, and focus date.
- The graph screen must also allow manual selection through four dropdowns in this order: village, object type, object, and measurement.
- Village and object type default to "all".
- The object dropdown lists only objects matching the selected village and type, sorted alphabetically.
- The object dropdown should include "Alle Objekte" for portfolio-level aggregate graphs.
- When "Alle Objekte" is selected, the measurement dropdown should offer aggregate media such as electricity, water, heat, and CO2 where those media exist in the filtered object set.
- When a single object is selected, the measurement dropdown should offer only measurements available for that object.
- Support electricity, heat, water, CO2 equivalents, costs, and energy production.
- Compare readings against:
  - last year;
  - multi-year history;
  - consultant-provided estimates;
  - benchmark/reference values;
  - expected usage.
- Provide portfolio-level, building-level, and datapoint-level views.
- Support objects that only need reporting, such as traffic lights or pumping stations.
- Support objects that need monitoring and control, such as schools, libraries, gyms, and town halls.

## First Customer-Presentable Frontend Demo
Approved decision:
- The first demo frontend is limited to the Community/Clerk-level experience.
- "V1 demo" means the first customer-presentable frontend demo, not the production v1 backend.
- Admin and Energy Consultant interfaces are not required for the first demo.
- Login may be mocked.
- Data, readings, ratings, report download, and control-related flows may be mocked.
- The UI should still look feature-complete and feel interactive from the clerk perspective.
- Mocked behavior must sit behind proper interface/API-shaped adapters so it can later be replaced by the real backend without redesigning the frontend.
- The demo should show the provided Harsefeld community logo in the application branding.
- The first demo does not expose Admin personalization settings, but it should visually demonstrate the future branding capability through the fixed demo logo.
- Required municipal object types for the first demo:
  - schools;
  - town halls / administrative offices;
  - libraries;
  - fire departments;
  - traffic lights;
  - pumping stations;
  - gyms / sports halls;
  - kindergartens / daycare facilities;
  - public pools.
- Optional first-demo object types include street lighting, public buildings, community halls, and other municipal assets.
- Actor-control screens may be shown in the first demo, but realistic command execution simulation is not required.
- Actor controls should also be visible from the object detail screen, not only from a separate control screen.
- First-demo actor controls may be UI-only or use simple mocked acknowledgements.
- Detailed command history, control failure simulation, and live device feedback are not required for the first demo unless needed for visual completeness.
- V1 only demonstrates actor-control intent in the UI and does not perform real device control.
- V1 does not define production safety guarantees for actor control.
- V1 UI may show allowed actions, confirmations, and mocked success feedback.
- Real actor-control availability and safety requirements are a v2 topic.
- The v1 API shape may include command request/acknowledgement concepts, but no real safety guarantees are defined yet.
- The first demo should include a mocked downloadable report positioned as an imaginary Harsefeld 2026 energy report.
- Configurable report templates are a future product direction, but admin/consultant-level template configuration may be excluded from the clerk-only demo unless needed to define proper interfaces.
- Demo data should be Samtgemeinde Harsefeld-style mock data, fictionalized for 2026 so it does not imply real current values.
- Demo DWD/weather integration should be included if practical. If real DWD fetching is too much for the first frontend-only demo, use an API-shaped mock with the same interface.
- Historic month rows should be clickable and open a daily-usage graph for that month.
- Historic readings should offer a toggle between "Kumuliert" and "Pro Monat" in German, and clear equivalent English labels.
- Summary fields for electricity, heat, water, and CO2 should be clickable and open the same graph component with a last-12-month default focus.
- Graph horizon controls should use clear German and English labels, not abbreviations.
- The first demo should offer one day, one week, one month, one year, three years, and five years as graph horizons; ten years is out of scope for the demo.
- The ratings/anomaly screen should show immediate text feedback after a review request is sent or updated.
- The ratings/anomaly screen should show a protocol/log of requested consultant reviews and updates below the request form.
- If a site/object already has an open consultant review request, the primary button should change from "Anfrage senden" to "Anfrage aktualisieren".
- The demo should include mocked existing consultant-review request data in addition to Pumpwerk Aue-Sued, so the log and update behavior are visible.
- The first demo screen set is:
  - mocked login;
  - portfolio overview;
  - site/building detail;
  - current and historic readings;
  - time-series graph / "Verlauf";
  - ratings and anomaly request;
  - actor controls and schedules as mocked clerk workflows;
  - report request/download for an imaginary Harsefeld 2026 report;
  - public overview and public reports.

## Ratings And Anomalies
- Provide green/yellow/red traffic-light ratings for readings and properties.
- Ratings may be based on historic consumption, consultant estimates, benchmarks, or configured thresholds.
- For history-based ratings:
  - green means the value is below the historical 75th percentile;
  - yellow means the value is from the historical 75th percentile up to the 95th percentile;
  - red means the value is above the historical 95th percentile.
- For consultant-based ratings, the Energy Consultant defines three threshold fields corresponding to rating bands or equivalent target/warning/critical thresholds.
- Rating source precedence:
  - use Energy Consultant thresholds/estimates when available;
  - otherwise use historical percentile-based rating when sufficient history exists;
  - otherwise show the rating as grey/unrated.
- Legal benchmarks may still be displayed for context or reporting, but are not the primary rating source unless a later requirement changes this.
- If data is missing or incomplete beyond a configured completeness threshold, show the rating as grey/unrated rather than green/yellow/red.
- The exact data-completeness threshold is TBD.
- Rating views should expose why a rating is greyed out, using a data-completeness indicator or explanation.
- Open detail: the exact historical comparison window/dataset is TBD.
- Open detail: simple predictions may be useful to report on trends and should be evaluated for the rating/reporting model.
- Users must be able to mark readings as anomalous.
- Marking an anomaly initially triggers an email or task to the energy consultant.
- A site/object may have one open consultant review request at a time until the Energy Consultant closes it.
- While a consultant review request is open, Community/Clerk users can add updates to the existing request rather than creating a parallel request.
- Closed consultant review requests remain visible in the protocol/log, and a new request may be opened afterwards.
- The UI must show immediate text feedback when a review request is sent or updated.
- Review request protocol entries should show at least timestamp, site/object, message, status, and whether the entry opened a request or updated an existing request.
- Review requests must support consultant response fields in the API model, including a short assessment for overview/status surfaces and a full assessment for drill-in detail.
- Rating summary text has two layers:
  - an automatically generated assessment such as "Alle Werte sind vollständig und liegen im grünen Bereich", "Strom deutlich erhöht", "Strom und Wasserverbrauch leicht erhöht", or "Wasserverbrauch für Mai und Juni unvollständig";
  - a request/consultant subtext shown only after a request exists, such as request status while pending or the consultant's short assessment after response.
- Clicking a request/consultant subtext should reveal the full consultant answer where one exists.
- When a ratings object is selected, the ratings screen should expand it and show its measurements for electricity, water, heat, and CO2 again.
- Entering the ratings screen normally must not automatically select or expand the first object.
- Navigating from an object-detail warning to the ratings screen should expand the relevant object and show its request context.
- The expanded ratings object must include a small close button on the right of the expanded fields; closing hides the expanded detail without clearing the globally selected object.
- On the ratings screen, the request log, text field, and action button should appear directly below the currently selected object and its measurements, not at the page bottom.
- On object detail, non-green objects should show a dismissible warning at the top.
- The object detail warning should show the automatic warning text, a request-in-progress status, or the consultant's short assessment depending on request state.
- Clicking the object detail warning should navigate to the ratings screen with the relevant object selected and ready to send a request or review the consultant answer.
- Later versions may route anomalies to AI analysis.

## Filtering, Sorting, And Object Selection
- Portfolio, ratings, and control views must provide shared filters because communities may manage many objects such as traffic lights, street lights, buildings, and technical sites.
- Required shared filters are village, object type, and rating.
- Portfolio and ratings views must include an exception toggle that shows red/critical objects even when they do not match the current village or type filters.
- The critical-object exception applies only to red ratings, not yellow or unrated objects.
- The control view must include a filter to hide objects without controllable actors.
- Shared filters should persist across navigation between portfolio, ratings, and control views.
- Sorting must include alphabetical, rating, type, village, and CO2 consumption.
- Alphabetical, village, and CO2 sorting must support ascending and descending order.
- Type sorting groups objects by type label and sorts objects alphabetically inside each type.
- Village sorting sorts villages alphabetically and then sorts objects alphabetically within each village.
- Rating sorting always orders red first, then yellow, then green, with unrated/grey entries after rated entries unless a later requirement changes this.
- CO2 sorting places objects without CO2 data at the bottom in both ascending and descending order.
- Object selection controls outside the ratings view should use a cascaded selection order: village, object type, object.
- Cascaded village and object-type dropdowns default to "all".
- Cascaded object dropdowns list only matching objects and sort them alphabetically.
- The ratings view uses filters instead of a single-object dropdown.

## Branding And Personalization
- Admin users must be able to configure community personalization options.
- The minimum required personalization option is a community logo.
- The community logo should be used in the authenticated WebUI, public portal, and generated/downloaded reports where appropriate.
- The first customer-presentable frontend demo should use the provided Harsefeld logo PNG as a fixed demo asset and must not use an invented or hand-drawn replacement logo.
- The provided logo asset should live in a normal frontend public/static asset location.
- Unused generated logo assets should be removed from the demo frontend.
- Admin branding configuration UI is out of scope for the first Community/Clerk-only demo, but the demo should make the resulting branded experience visible.

## Control And Automation
- Support controlled actors including heating, cooling, lights, shades, blinds, and similar appliances.
- Support more than on/off controls where the actor allows it, such as setpoints, mode, target temperature, and position.
- Allow schedules for recurring usage patterns:
  - schools need reduced heating on weekends;
  - gyms may have low or no usage in mornings;
  - offices and libraries may follow opening hours.
- Timetables should show a compact read-only row by default.
- A row edit icon opens timetable edit mode for that row; edit mode remains active until the user saves or cancels.
- Timetable edit mode must include an X icon to cancel editing and restore the previous read-only row.
- Users should be able to edit all schedule/timetable fields exposed in the demo: name, days, start time, end time, controlled actor selection, target action, and enabled status.
- Timetable actor selection must support selecting multiple actors of the same actor type through a dropdown with checkboxes.
- Once an actor type is selected for a timetable, actors of other types should be greyed out because mixed actor types should not be combined in one timetable.
- The timetable target field ("Ziel") must be a dropdown populated from the selected actor's allowed actions.
- For timetables with multiple selected actors, the target dropdown must show only actions available on all selected actors.
- Schedule/timetable editing must use API-shaped interfaces that can map to the future backend.
- Allow simple sensor-based automations:
  - heating based on temperature sensors;
  - blinds or shades based on sunlight;
  - lighting based on schedules or occupancy in later versions.
- Control operations must be permissioned, validated, logged, and visible in history.
- Pending actor command confirmations and schedule/timetable confirmations should automatically cancel when the selected object changes.

## Reporting
- Generate annual energy reports similar to the Harsefeld 2023 report.
- Automate report generation where possible.
- Keep an energy consultant in the loop for findings and recommendations in early versions.
- Allow reports to be released for download.
- Allow reports to be marked public and downloadable without login.
- Report requirements are detailed in `requirements/reporting.md`.

## Data Management
- Admins must be able to connect datapoints and define their meaning.
- Admins and Community Admins must be able to rename and reorganize datapoints.
- Admins and Community Admins must be able to import historic readings from CSV.
- The system must support data completeness notes, especially when years or billing periods are not comparable.
- V1 supports CSV import and API ingestion for readings.
- A mobile reading app is planned for v2, with app login, offline buffering, sync, camera support, and QR-code support. Details are in `requirements/mobile-app.md`.

## Initial Missing Feature Candidates
These are derived from the Harsefeld report and need validation during product design:
- Legal reporting deadline and publication tracking.
- Weather-normalized heating consumption.
- Cost tracking by medium, property, category, and resident.
- CO2 emission factors per energy carrier.
- Water usage reporting.
- Energy production, self-consumption, and feed-in reporting.
- Net floor area and kWh per square meter indicators.
- Building category and portfolio benchmarking.
- Internal detail reports separate from public summaries.
- Measure and renovation tracking for savings recommendations.

## Research-Derived Feature Candidates
The following features appeared in comparable products or municipal energy-management guidance and should be considered for roadmap placement:
- Manual meter reading workflows with QR codes or mobile prefilled forms.
- RLM/iMSys smart-meter integration.
- Alerts for individually configured thresholds.
- Invoice-to-meter-reading reconciliation.
- Invoice-to-supply-contract reconciliation.
- Building equipment and renovation-state tracking.
- Monthly reports and building-specific reports in addition to annual reports.
- Report archive with stable released versions.
- Word or editable report draft export, not only PDF.
- Budget, tariff, and rate tracking.
- Energy-saving project tracking with expected and actual savings.
- Public embeddable dashboards or shareable public dashboard links.
- Weather correlation charts and weather-sensitive meter classification.
- Scheduled report distribution.

These should not all be treated as v1 requirements. They should be prioritized after the first frontend demo and backend API contract are clearer.

## Kom.EMS Alignment
Approved decision:
- Use Kom.EMS as a requirements validation and maturity checklist.
- Align the v1 demo with visible Kom.EMS-style municipal energy-management concepts: monitoring, portfolio views, reports, anomalies, CSV/API ingest, and weather normalization.
- Production v1 should adopt Kom.EMS-aligned basics where they support monitoring and reporting correctness, such as building/site structure, meter/readings, cost/consumption, weather correction, report archive, and anomaly detection.
- Invoice reconciliation and supply-contract reconciliation remain future roadmap candidates, not first-demo requirements.

## V3 Roadmap Candidates
- Invoice reconciliation.
- Supply-contract reconciliation.

These are part of the long-term product vision for municipal energy controlling, but excluded from the first frontend demo and not required for core v1 unless a pilot customer makes them mandatory.
