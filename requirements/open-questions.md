# Open Questions

## Product Scope
- Resolved: Meaning of v1 demo.
  - Decision: "V1 demo" means the first customer-presentable frontend demo, not the production v1 backend.
- Resolved: First customer-presentable frontend scope.
  - Decision: Everything may be mocked for the first frontend demo.
  - Decision: The first demo is Community/Clerk-level only.
  - Decision: Admin and Energy Consultant UI are not required for the first demo.
  - Decision: Login may be mocked and data can be generated.
  - Decision: The UI should look feature-complete and appear operational.
  - Decision: Mocked behavior must use proper API-shaped interfaces/adapters.
- Resolved: First-demo municipal object types.
  - Decision: Required first-demo object types are schools, town halls / administrative offices, libraries, fire departments, traffic lights, pumping stations, gyms / sports halls, kindergartens / daycare facilities, and public pools.
  - Decision: Optional first-demo object types include street lighting, public buildings, community halls, and other municipal assets.
- Resolved: First-demo actor-control behavior.
  - Decision: Actor-control screens may be included, but simulated real command execution is not required.
  - Decision: First-demo controls may be UI-only or use simple mocked acknowledgements.
  - Decision: Detailed command history, control failure simulation, and live actor feedback are not required for the first demo unless needed visually.
- Resolved: First-demo screen set.
  - Decision: The first demo includes mocked login, portfolio overview, site/building detail, current and historic readings, ratings/anomaly request, actor controls and schedules as mocked clerk workflows, report request/download for an imaginary Harsefeld 2026 report, and public overview/public reports.
  - Decision: Admin and Energy Consultant screens are moved out of the first-demo screen list because they are explicitly out of scope.
- Resolved: Demo data identity.
  - Decision: Use Samtgemeinde Harsefeld-style mock data, fictionalized for 2026 so it does not imply real current values.

## Reporting
- Resolved: First report template target.
  - Decision: Future product direction is configurable report templates.
  - Decision: The first frontend demo should offer a mocked downloadable imaginary Harsefeld 2026 energy report.
  - Decision: Admin/consultant-level template configuration UI may be excluded from the clerk-only demo unless needed to properly define API-shaped interfaces.
- Resolved: Report output and editing.
  - Decision: Initial report output is PDF only.
  - Decision: Report edits happen through WebUI and backend/API data structures before final PDF generation or release.
  - Decision: Word export and separate editable HTML draft export are not required initially, but should remain possible later.
- Resolved: Final report approval authority.
  - Decision: Energy Consultant has final report approval and release authority.
  - Decision: Community/Admin roles may request, view, download, and prepare inputs where permitted, but do not perform final release unless a later requirement changes this.
- Resolved: Public report detail visibility.
  - Decision: Public reports hide site-level details by default.
  - Decision: Guest/Public users receive aggregated or summarized report data unless a report section or data item is explicitly marked public.
  - Decision: Publication workflow needs visibility controls with "hide detail from public" as the safe default.

## Ratings
- Resolved: Rating thresholds.
  - Decision: For history-based ratings, green is below the historical 75th percentile, yellow is from the 75th percentile up to the 95th percentile, and red is above the 95th percentile.
  - Decision: For consultant-based ratings, the Energy Consultant defines three threshold fields corresponding to rating bands or equivalent target/warning/critical thresholds.
  - Open detail: The exact historical comparison window/dataset is TBD.
  - Open detail: Simple predictions may be useful for trend reporting and should be evaluated for the rating/reporting model.
- Resolved: Rating source precedence.
  - Decision: Use Energy Consultant thresholds/estimates when available.
  - Decision: If no consultant thresholds exist, use historical percentile-based rating when sufficient history exists.
  - Decision: If neither consultant thresholds nor sufficient history exist, show the rating as grey/unrated.
  - Decision: Legal benchmarks may still be displayed for context or reporting, but are not the primary rating source unless a later requirement changes this.
- Resolved: Missing/incomplete data rating behavior.
  - Decision: If data is missing or incomplete beyond a configured completeness threshold, show the rating as grey/unrated.
  - Decision: Rating views should expose why a rating is greyed out, using a data-completeness indicator or explanation.
  - Open detail: The exact data-completeness threshold is TBD.

## API Security
- Resolved: API credential model for external ingestion and actor control.
  - Decision: Use OAuth 2.0 Client Credentials with scoped, short-lived access tokens as the production direction.
  - Decision: Use scopes such as `readings:write`, `readings:read`, `actors:control`, and `reports:read`.
  - Decision: Scoped API tokens may be acceptable for early demo/development use only.
  - Decision: Plan mTLS as an optional higher-security mode for actor control, gateways, and sensitive deployments.
- Resolved: Admin API credential management UI.
  - Decision: Admin users need a UI to manage machine/API credentials.
  - Decision: For production OAuth2 Client Credentials, the UI should manage API clients/integration credentials rather than only raw tokens.
  - Decision: Admin users must be able to create API clients, assign scopes, assign allowed organization/site/protocol scope once finalized, view metadata, rotate credentials, disable/revoke credentials, and view last-used/audit metadata.
  - Decision: Client secrets must be shown only once at creation and never shown again.
  - Decision: For early demo/development scoped API tokens, the same UI can be represented as "API credentials" without implementing full OAuth yet.
- Resolved: External integration scoping.
  - Decision: User/action-oriented permissions are scoped at the organization level.
  - Decision: Data-ingestion/query permissions are scoped at the site level.
  - Decision: Protocol/integration-specific permissions are additionally scoped by protocol or connector type where relevant.
  - Decision: Finer scoping by datapoint or actor remains a future option, but is not the default v1 scoping model.

## Identity
- Resolved: Identity provider integration priority.
  - Decision: OIDC is first priority as the preferred modern SSO protocol.
  - Decision: LDAP / Active Directory is second priority for municipalities without OIDC-capable identity infrastructure.
  - Decision: SAML is third priority for customers whose existing SSO requires it.
  - Decision: Direct local login remains available for initial/demo use and for deployments without an external identity provider.
- Resolved: Privileged user 2FA.
  - Decision: All privileged users must use 2FA.
  - Decision: Email-based one-time codes are allowed as a supported 2FA method, alongside authenticator app/TOTP.

## Architecture
- Resolved: Edge connector timing.
  - Decision: The edge connector is a v2 feature area and is not part of v1.
- Resolved: Automation execution location.
  - Decision: Whether automations run centrally in the backend or locally at remote sites is postponed as a v2 decision.
- Resolved: V1 actor-control availability and safety.
  - Decision: V1 only demonstrates actor-control intent in the UI and does not perform real device control.
  - Decision: V1 does not define production safety guarantees for actor control.
  - Decision: V1 UI may show allowed actions, confirmations, and mocked success feedback.
  - Decision: Real actor-control availability and safety requirements are a v2 topic.
  - Decision: The v1 API shape may include command request/acknowledgement concepts, but no real safety guarantees are defined yet.
- Resolved: Main repository consumption of frontend/backend.
  - Decision: The main `kikakeule/energy` repository consumes `energy-frontend` and `energy-backend` via Git submodules.
- Resolved: Default Docker Compose target.
  - Decision: The default Docker Compose setup should support both local demo and production-like deployment through Compose profiles or separate compose overlays.
  - Decision: The local demo path should be easy to start, while the production-like path should remain available from the main `energy` repository.
- Resolved: Initial private container registry.
  - Decision: Prefer building from source through Docker Compose for the demo and avoid GHCR unless it is necessary.
  - Decision: GHCR is available as an optional private image registry when prebuilt images are necessary.
  - Decision: Add cleanup/retention from the beginning and keep only useful tags such as `latest`, `demo`, and the last few version tags.
  - Decision: Delete untagged images and avoid permanently publishing every branch build.
  - Decision: Normal local/demo deployment must build from frontend/backend submodules where possible so registry pulls are optional.
  - Decision: Keep self-hosted private Docker Registry as the quick replacement/fallback if GHCR quota, pricing, or policy becomes a problem.

## Data Model
- Resolved: Required v1 media/data categories.
  - Decision: V1 data model must support electricity, heat, water, gas, oil, biomass, PV, feed-in, CO2, and cost.
- Resolved: Reading type separation timing.
  - Decision: Whether billing data, meter readings, and high-frequency telemetry should be separate reading types is postponed until after the frontend demo.
- Resolved: Resident count timing.
  - Decision: Resident count is postponed until after the first frontend demo because Admin UI is out of scope for the demo.

## Research Follow-Up
- Resolved: Kom.EMS requirement adoption.
  - Decision: Use Kom.EMS as a requirements validation and maturity checklist.
  - Decision: Align the v1 demo with visible Kom.EMS-style municipal energy-management concepts: monitoring, portfolio views, reports, anomalies, CSV/API ingest, and weather normalization.
  - Decision: Production v1 should adopt Kom.EMS-aligned basics where they support monitoring and reporting correctness, such as building/site structure, meter/readings, cost/consumption, weather correction, report archive, and anomaly detection.
  - Decision: Invoice reconciliation and supply-contract reconciliation remain future roadmap candidates, not first-demo requirements.
- Resolved: QR/manual reading support.
  - Decision: V1 supports CSV import and API ingestion for readings only.
  - Decision: V2 needs a mobile reading app with app-based login, local offline buffering, sync when internet returns, organized reading workflow support, camera support, and QR-code support.
  - Decision: Mobile app requirements live in `requirements/mobile-app.md`.
- Resolved: RLM/iMSys timing.
  - Decision: RLM/iMSys integrations are v2 production integration requirements, not v1/demo requirements, unless an easy metering-provider or EWE/LiMBO access path becomes available early.
- Resolved: DWD weather data integration.
  - Decision: DWD weather data integration is required for v1 and should also be represented in the demo.
  - Decision: Use real DWD data in the demo if practical.
  - Decision: If real DWD fetching is not practical for the first frontend-only demo, provide an API-shaped mock behind the same interface.
  - Decision: Demo deployment may set site weather location through Docker Compose configuration.
  - Decision: In the full product, Admin users configure weather location per site.
- Resolved: SMARD/ENTSO-E in reports.
  - Decision: SMARD and ENTSO-E should stay out of v1 reports except as future optimization/context sources.
- Resolved: First target BMS context.
  - Decision: The first target municipality does not currently run a BMS such as Desigo, EcoStruxure, or Niagara.
  - Decision: The known existing system is EWE LiMBO for reporting.
- Resolved: First real customer building automation protocol.
  - Decision: Loxone is a known building automation protocol/platform in the first real customer context and should be tracked for integration planning.
- Resolved: Invoice and supply-contract reconciliation.
  - Decision: Invoice reconciliation and supply-contract reconciliation are v3 roadmap features.
  - Decision: They are part of the long-term product vision for municipal energy controlling.
  - Decision: They are excluded from the first frontend demo and not required for core v1 unless a pilot customer makes them mandatory.
