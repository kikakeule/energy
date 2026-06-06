# Feature Requirements

## Overview And Monitoring
- Show current consumption across the community portfolio.
- Show current readings and historic readings per site, building, datapoint, category, and medium.
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
- The first demo screen set is:
  - mocked login;
  - portfolio overview;
  - site/building detail;
  - current and historic readings;
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
- Later versions may route anomalies to AI analysis.

## Control And Automation
- Support controlled actors including heating, cooling, lights, shades, blinds, and similar appliances.
- Support more than on/off controls where the actor allows it, such as setpoints, mode, target temperature, and position.
- Allow schedules for recurring usage patterns:
  - schools need reduced heating on weekends;
  - gyms may have low or no usage in mornings;
  - offices and libraries may follow opening hours.
- Allow simple sensor-based automations:
  - heating based on temperature sensors;
  - blinds or shades based on sunlight;
  - lighting based on schedules or occupancy in later versions.
- Control operations must be permissioned, validated, logged, and visible in history.

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
