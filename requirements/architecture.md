# Architecture Requirements

## Initial Shape
The project should be split across three GitHub repositories:
- Main coordination repository: `https://github.com/kikakeule/energy`
- Frontend repository: `https://github.com/kikakeule/energy-frontend`
- Backend repository: `https://github.com/kikakeule/energy-backend`

The main `energy` repository owns requirements, general documentation, Docker Compose deployment files, environment examples, and cross-project coordination. The frontend and backend repositories own their application source code.

The project should also be split into frontend and backend responsibilities, with further subdivision where it reduces risk and keeps responsibilities clear.

Recommended high-level components:
- Web frontend.
- Backend REST API.
- Database and time-series storage.
- Reporting pipeline.
- Automation engine.
- Integration/edge connector layer.
- Public portal surface.

## Frontend
- Repository: `https://github.com/kikakeule/energy-frontend`
- WebUI for all user roles.
- German default, English supported.
- API-client generated from OpenAPI when backend contract exists.
- Should be presentable before the backend is complete by using mock data aligned to planned API models.
- Must be runnable through Docker Compose from the main `energy` repository without manual precompile.

## Backend
- Repository: `https://github.com/kikakeule/energy-backend`
- REST API.
- Authentication and authorization.
- Readings ingestion and queries.
- Actor control and command logging.
- Automation scheduling and execution.
- Report generation workflow.
- User and role management.
- Must be runnable through Docker Compose from the main `energy` repository without manual precompile.

## Deployment
- Repository: `https://github.com/kikakeule/energy`
- Docker Compose is the required from-scratch deployment path.
- A user should be able to clone the needed repositories or use compose configuration from the main repository and start the product without manually building frontend or backend artifacts first.
- Compose may build images from source or reference prebuilt images, but the workflow must not require a separate precompile command.
- Deployment requirements are detailed in `requirements/deployment.md`.

## Data Storage
The system needs:
- Relational storage for organizations, sites, users, roles, reports, actors, and configuration.
- Time-series storage for readings and actor state history.
- Document/file storage for generated reports.
- Audit log storage.

V1 data model must support these media/data categories:
- electricity;
- heat;
- water;
- gas;
- oil;
- biomass;
- PV;
- feed-in;
- CO2;
- cost.

Whether billing data, meter readings, and high-frequency telemetry should be separate reading types is postponed until after the frontend demo.

## Integration/Edge Layer
Because municipal objects are distributed and sometimes remote, the architecture should support an integration or edge connector layer that can:
- collect data from local systems;
- buffer readings during connectivity loss;
- forward readings securely;
- receive validated control commands where appropriate;
- integrate with building automation and metering protocols.

The edge connector is a v2 feature area and is not part of v1.

## Reporting Pipeline
The reporting pipeline should:
- generate reproducible report drafts;
- support consultant edits/findings;
- archive released versions;
- allow public/private visibility decisions;
- produce PDF downloads.

## Automation Engine
The automation engine should initially support simple schedules and sensor-based rules. It may start as part of the backend and split later if complexity grows.

Whether automations run centrally in the backend or locally at remote sites is a v2 decision.

## Actor Control Safety
- V1 only demonstrates actor-control intent in the UI and does not perform real device control.
- V1 does not define production safety guarantees for actor control.
- V1 UI may show allowed actions, confirmations, and mocked success feedback.
- Real actor-control availability and safety requirements are a v2 topic.
- The v1 API shape may include command request/acknowledgement concepts, but no real safety guarantees are defined yet.
