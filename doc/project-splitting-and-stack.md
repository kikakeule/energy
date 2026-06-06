# Project Splitting And Stack Recommendations

## Recommended Project Parts
- Frontend WebUI.
- Backend REST API.
- Database and time-series storage.
- Reporting pipeline.
- Automation engine.
- Integration/edge connector layer.
- Public portal.
- Shared API/schema package.
- Infrastructure and deployment.

## Repository Locations
- Main coordination repository: `https://github.com/kikakeule/energy`
- Frontend repository: `https://github.com/kikakeule/energy-frontend`
- Backend repository: `https://github.com/kikakeule/energy-backend`

The main repository owns requirements, documentation, Docker Compose, environment examples, and cross-repository coordination. The frontend and backend repositories own their application source code.

## Recommended Languages And Technologies
Initial recommendation:
- Frontend: TypeScript with React and Vite.
- Backend API: TypeScript with NestJS, or another structured Node.js REST framework.
- Database: PostgreSQL, with TimescaleDB considered for time-series readings.
- Edge connector: Go if a separate gateway service is needed.
- Reporting: backend-owned HTML-to-PDF pipeline initially.
- API contract: OpenAPI.
- Infrastructure: Docker Compose for local v1.

## Rationale
- TypeScript keeps frontend and backend models aligned.
- REST and OpenAPI match the stated API preference and support customer/integration documentation.
- PostgreSQL handles relational municipal configuration well.
- TimescaleDB is a pragmatic extension for readings and time-series queries.
- Go is suitable for compact, reliable edge services when remote-site gateways are needed.

## Split Timing
- Start with frontend and backend as separate apps.
- Keep automation and reporting inside the backend until complexity justifies extraction.
- Create an edge connector only when real remote integration requirements are known.

## Suggested Repository Shape

### `kikakeule/energy`
- `requirements/`: living requirements.
- `doc/`: general documentation.
- `compose.yaml` or `docker-compose.yaml`: default from-scratch deployment.
- `deploy/`: production-like compose files and deployment notes if needed.
- `.env.example`: documented environment defaults.
- optional `api-contract/`: OpenAPI contract if it should be owned centrally.
- Git submodules for `energy-frontend` and `energy-backend`.

### `kikakeule/energy-frontend`
- Customer-presentable WebUI.
- Public portal UI.
- Role-specific authenticated UI.
- Frontend Dockerfile that can build/run without manual precompile.

### `kikakeule/energy-backend`
- REST API, auth, RBAC, data model, reporting workflow, automation orchestration.
- Backend Dockerfile that can build/run without manual precompile.
- Database migrations and seed/demo data.
- Optional future internal modules for edge integration, reporting, and automation.

## Language Tradeoffs
- TypeScript frontend is the default choice because React/Vite gives fast iteration for the demo and strong ecosystem support.
- TypeScript backend keeps API types close to frontend types and is pragmatic for REST/OpenAPI, auth, and admin workflows.
- Go for edge connectors is useful if the connector must be small, reliable, cross-compiled, and deployed to remote sites.
- Python is useful for analysis prototypes but should not be the first choice for the main API unless analytics/AI becomes the dominant backend concern.
- Java/Kotlin or C# would also be viable for enterprise/public-sector backends, but they add more ceremony for the current frontend-first phase.

## Further Split Recommendation
Backend and frontend are necessary but not sufficient as concepts. Split by responsibility:
- Presentation: WebUI and public portal.
- Contract: OpenAPI and shared schemas.
- Core API: users, roles, organization model, datapoints, readings, actors.
- Time-series ingestion: reading ingestion, import, quality status, aggregation.
- Automation/control: schedules, rules, commands, safety/audit.
- Reporting: calculations, templates, consultant workflow, archive.
- Integration: edge/gateway adapters and external data provider clients.

Do not create all services immediately. Start as a modular monorepo and split runtime services only when operational needs require it.

## Compose From Scratch Requirement
Docker Compose is the default deployment path. The main `energy` repository must provide a compose file that can start the stack without a user manually precompiling either application.

Acceptable implementation patterns:
- Compose builds frontend and backend images from source directories.
- Compose pulls prebuilt images for tagged releases.

The deployment must avoid requiring local build tools outside Docker for normal use.

## Container Registry Direction
- Build from source through Docker Compose for local/demo deployments wherever possible.
- For private repositories, authorize Git on the host and initialize submodules before Compose runs.
- The default local/demo Docker build consumes local submodule source and should not receive GitHub credentials.
- The demo does not require pulling a prebuilt application image from Docker Hub, GHCR, or another registry.
- Base images may still be pulled unless the deployment overrides them with internal mirrored images.
- Avoid GHCR for the demo unless prebuilt private images become necessary.
- Use GHCR private images only as the initial optional private registry for prebuilt images.
- Use strict image retention to stay within early quota.
- Keep self-hosted Docker Registry as the quick fallback/replacement option.
