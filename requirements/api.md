# API Requirements

## API Direction
The v1 backend should expose a REST API with a mostly final contract for frontend and external integrations. The API must support readings, datapoints, devices, actors, automations, reports, users, roles, imports, and public access.

OpenAPI should be used for documentation and frontend client generation once implementation starts.

External research confirms that REST APIs are common in comparable systems:
- aedifion exposes platform functionality through a RESTful HTTP API and complements it with MQTT for streaming building time-series data.
- EnergyCAP exposes a REST API for programmatic access to organization energy data.

Sources:
- https://docs.aedifion.io/en/products/io/apis/
- https://developer.energycap.com/api-getting-started/getting-started/index.html

## Core API Areas
- Authentication and session management.
- User and role management.
- Fine-grained clerk permission assignments for later versions.
- Organization/community branding settings, including configured logo metadata and logo asset retrieval.
- Organization, municipality, site, building, and asset hierarchy.
- Datapoint configuration and metadata.
- Reading ingestion and reading queries.
- Historical import workflows.
- Ratings, thresholds, estimates, and anomalies.
- Benchmarks, reference values, normalized comparisons, sensor datapoints, warnings, and user notification preferences.
- Device inventory, device measurements, maintenance tracking, device warnings, and device-exposed controls.
- Consultant review request creation, update, closure state, and protocol/log queries.
- Actor discovery, configuration, control, and command history.
- Automation and schedule management.
- Report generation, consultant edits, release workflow, and downloads.
- Public read-only endpoints for guest/public dashboards and released reports.

## Reading API
The reading API must support:
- Adding readings via API.
- Checking readings via API.
- Querying current readings.
- Querying historic readings by time range.
- Querying time-series data for graph drilldowns by focus date, horizon, aggregation level, cumulative/period mode, site/object, datapoint, medium, and category.
- Querying portfolio aggregate time-series data for filtered object sets, including an "all objects" selection where appropriate.
- Filtering by organization, site, building, datapoint, medium, and category.
- Filtering object/time-series queries by village and object type.
- Storing source, timestamp, unit, value, quality status, and import method.
- Returning cost metadata with consumption values where costs are known or calculated, including currency and enough information for the frontend to show cost as a secondary or primary value.
- Returning device-scoped measurements where a reading belongs to a specific physical device, such as heat-pump electricity consumption, produced heat, COP, PV production, battery state of charge, or ventilation operating values.
- Handling billing-period readings and calendar-period normalized readings.
- Querying year-comparison summaries for selected years, with measurements as rows, years as columns, deltas, and missing-data flags.
- Returning enough metadata for the frontend to select specific days, weeks, months, quarters, or years depending on the chosen horizon.
- Returning display labels or label metadata with enough year context for week, month, quarter, and year views.
- Supporting the approved horizons of one day, one week, one month, one year, three years, and five years; three-year and five-year responses must support quarter-level buckets.
- Returning values, units, bucket timestamps, bucket labels, and drilldown targets so the frontend can show hover values and navigate from a clicked bucket to the next useful detail view.
- Rejecting or normalizing future focus dates according to product policy; frontend date inputs should not send future dates, but the backend must not rely only on UI validation.

## Benchmark And Comparison API
The benchmark/comparison API must support:
- Configurable benchmark/reference values by organization, object type/category, construction-year range, normalization basis, value, unit, source/citation, and validity period.
- Per-object benchmark overrides such as kWh/(m2*a), including author, timestamp, and note/reason metadata.
- Normalized peer/category comparison results, including peer group, normalized value, position or range, and completeness status.
- Explicit incomplete/limited comparison states when usable area, weather-normalization data, or other required metadata is missing.

## Sensor, Warning, And Message API
The sensor/warning API must support:
- Querying sensor datapoints separately from consumption metrics where needed.
- Returning sensor type, current value, unit, quality/status, last update timestamp, warning-capable flag, and warning-enabled state.
- Admin-defined warning thresholds by warning category or datapoint type.
- User notification preferences by warning category and channel, with at least `web`, `mail`, and `app`.
- Device fault and device maintenance notification preferences must support shared Web/Mail/App channels plus a selected set of included device types.
- Warning/message instances with severity, status, object/site, datapoint or category, measured value, threshold, timestamps, source/channel, and target link metadata.
- Device fault and device maintenance warning categories in addition to consumption and sensor warning categories.
- Message queries must be filterable by message kind, severity, village, object type, site/object, warning category, channel, and status.
- Message queries for user-facing Web messages must respect both user Web delivery preferences and object/datapoint warning-enabled state.
- Consultant review updates as message-like entries for the frontend messages screen.

## Device API
The device API must support:
- Querying devices by organization, village, object type, site/object, device type, status, warning state, and maintenance state.
- Querying devices for "all objects" selections where the frontend shows a filtered device set.
- Returning device identity and metadata, including device ID, object/site assignment, display name, device type, smart/legacy capability, manufacturer/model/serial metadata where available, installation date where known, and operational status.
- Supporting at least the V1 device types `heat_pump`, `pv_system`, `battery`, and `ventilation_system`, with localized labels such as "Wärmepumpe", "PV-Anlage", "Batterie", and "Lüftungsanlage".
- Returning device measurements/datapoints with value, unit, quality/status, timestamp, cost where applicable, warning capability, and display tier such as `summary` or `detail`.
- Returning line-chart-capable time-series data for device measurements in device detail views.
- Returning heat-pump summary measurements for electricity consumed, heat produced, and COP; detail measurements should additionally include flow temperature, return temperature, and operating mode where available.
- Returning PV summary measurements for electricity produced, self-consumption, and feed-in; detail measurements should additionally include current output where available.
- Returning battery summary measurements for state of charge and charge/discharge power; detail measurements should additionally include charge/discharge energy and capacity where available.
- Returning ventilation summary measurements for electricity consumed, operating state, and filter state; detail measurements should additionally include airflow and CO2/air-quality values where available.
- Representing legacy devices that only have manual measurements, manual maintenance state, and no live controls.
- Representing smart devices that expose live telemetry, device warnings, and optional controls.
- Returning warning-enabled state for device measurements, device-level warning categories, and device maintenance warnings.
- Returning device warnings separately from building consumption warnings and general sensor warnings while still exposing them through the shared message API.
- Returning maintenance configuration and state, including maintenance interval or next-maintenance date, last maintenance date, status/severity, responsible party where known, and notes.
- Recording manual maintenance completion events with timestamp, user, optional note, and resulting next-maintenance date.
- Creating warning/message instances when maintenance is due within 60 days, due within 30 days, or overdue.
- Keeping maintenance warnings active until maintenance is recorded as completed.
- Returning device-exposed controls only as actor-backed controls in V1, including actor ID, allowed actions, current state, and command metadata.
- Reusing actor-control command, permission, audit-log, and acknowledgement semantics for all device controls.

## Branding API
The branding API must support:
- Reading organization/community branding settings.
- Storing and retrieving a community logo or logo reference.
- Returning logo metadata such as media type, dimensions where known, alt text, and last update timestamp.
- Making the configured logo available to authenticated UI, public UI, and report generation.
- Enforcing Admin-only mutation permissions for branding settings.

## Anomaly And Consultant Review API
The anomaly/review API must support:
- Creating a consultant review request for an anomalous reading, site, object, or metric.
- Returning immediate status for request creation or update.
- Enforcing at most one open consultant review request per site/object or equivalent review scope until the Energy Consultant closes it.
- Adding updates to an existing open request instead of creating parallel duplicate requests.
- Keeping closed requests and all updates in a protocol/log.
- Querying request logs with timestamp, actor/user, site/object, message, status, and entry type such as request opened, request updated, or request closed.
- Returning consultant response fields when present, including a short assessment for overview/status surfaces and a full assessment for detail views.
- Returning enough state for the frontend to distinguish no request, request in progress, and consultant answered/closed states.
- Allowing Energy Consultants to close a request in later consultant workflows.

## Actor Control API
The actor API must support:
- Reading actor state.
- Returning actor type/kind, allowed actions, and enough label metadata for timetable target dropdowns.
- Sending control commands.
- Supporting non-binary controls such as target temperature, mode, level, and shade position.
- Returning command status and failure reason.
- Recording audit logs.
- Enforcing role permissions.

## Automation API
The automation API must support:
- Time schedules.
- Simple condition-based rules.
- Manual enable/disable.
- Editing schedule/timetable fields, including name, days, start time, end time, selected actor IDs, target action, and enabled status.
- Validating that a timetable containing multiple actors only combines actors of the same actor type.
- Validating that the selected target action is included in the allowed-actions intersection for all selected actors.
- Execution history.
- Conflict detection and safe failure behavior.

## Object List And Filter API
Portfolio, ratings, control, and object-selection endpoints must support:
- Filtering by village, object type, and rating where the consuming view exposes filter controls.
- Returning critical objects for portfolio and ratings views when the critical-object exception is enabled, even when other filters would exclude them.
- Returning actor availability metadata so control object selectors can focus users on controllable objects without requiring a separate control filter panel.
- Returning device availability metadata so device selectors can show object sets that contain devices without requiring users to scroll through unrelated objects.
- Sorting by alphabetical name, rating, object type, village, and CO2 consumption.
- Combining sort key and direction in frontend-facing option metadata where direction is meaningful.
- Ascending and descending sort directions for alphabetical, village, and CO2 sorting.
- Type sorting groups objects by type label and sorts objects alphabetically inside each type.
- Rating sort order of red, yellow, green, then unrated/grey unless a future requirement changes the unrated placement.
- Placing objects without CO2 values at the bottom for CO2 sorting in both directions.
- Returning distinct villages, object types, objects, and available measurements needed for cascaded object selectors.
- Returning aggregate measurement availability for "all objects" portfolio selections.

## User And Permission API
The user/role API must be designed to later support fine-grained clerk permission assignments, including read access, device read access, actor command access, device-control access, maintenance edit access, timetable edit access, and temporary overwrite access by organization, village/site, object, device, actor, or action scope.

## Reporting API
The reporting API must support:
- Creating report requests.
- Generating draft reports.
- Consultant editing and findings.
- Release approval.
- Public/private visibility.
- PDF download.
- Archive access.

## API Security TODO
The security model for external reading ingestion and actor control must be defined before production use.

Approved API credential direction:
- External ingestion and actor-control APIs should use OAuth 2.0 Client Credentials with scoped, short-lived access tokens as the production direction.
- Scopes should express permissions such as `readings:write`, `readings:read`, `actors:control`, and `reports:read`.
- Scoped API tokens may be acceptable for early demo/development use only.
- mTLS should be planned as an optional higher-security mode for actor control, gateways, and sensitive deployments.

Open questions:
- Should Admin users manage tokens in the UI?
- What audit, rotation, expiry, and revocation rules are required?
- How are remote endpoints authenticated when a municipal site is offline or behind NAT?

Approved external integration scoping:
- User/action-oriented permissions are scoped at the organization level.
- Data-ingestion/query permissions are scoped at the site level.
- Protocol/integration-specific permissions should be additionally scoped by protocol or connector type where relevant, such as `loxone`, `csv-import`, `smart-meter`, `dwd`, or `bacnet`.
- Finer scoping by datapoint or actor remains a future option, but is not the default v1 scoping model.

Research note:
- MaStR web services use HTTPS-only access on port 443 and separate web-service users. This is not a direct blueprint for this product, but it reinforces that machine access should be explicit, encrypted, scoped, and operationally manageable.

Source:
- https://www.marktstammdatenregister.de/MaStRHilfe/files/webdienst/2025-10-01%20Dokumentation%20MaStR%20Webdienste%20V25.2.pdf

## MQTT / Streaming Consideration
REST remains the preferred v1 API for frontend/backend and external command/query workflows. MQTT or another streaming transport should be considered later for:
- live readings from edge gateways;
- offline-capable remote sites;
- alarms and event streams;
- bidirectional device/gateway communication.

This should not replace the REST contract for administrative and reporting workflows.
