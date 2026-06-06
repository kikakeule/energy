# Deployment Requirements

## Goal
The project must be usable from scratch with Docker Compose. A user should not need to manually precompile the frontend or backend before starting the system.

## Repository Ownership
- Main coordination repository: `https://github.com/kikakeule/energy`
- Frontend repository: `https://github.com/kikakeule/energy-frontend`
- Backend repository: `https://github.com/kikakeule/energy-backend`

The main `energy` repository owns:
- requirements;
- general documentation;
- Docker Compose deployment files;
- environment examples;
- cross-project setup instructions;
- shared deployment configuration;
- references to frontend and backend source repositories.

The `energy-frontend` repository owns frontend application source code.

The `energy-backend` repository owns backend application source code.

## Docker Compose Requirement
The main repository must provide a Docker Compose deployment that can start the product from scratch.

Required behavior:
- No manual frontend precompile step.
- No manual backend precompile step.
- No local Node.js, package-manager, or backend runtime installation required outside Docker for normal deployment.
- Compose should build required images from source or pull prebuilt images.
- The local demo must build application images from local checked-out source/submodules rather than requiring a pushed application image from Docker Hub, GHCR, or another registry.
- Initial setup should be possible with a small number of commands after cloning the main repository.
- Environment variables should be documented and have safe examples.
- Persistent data must use named volumes or documented bind mounts.
- The deployment should include at least frontend, backend, database, and any required supporting services.
- Health checks should be added for core services once implementation exists.
- The default Docker Compose setup should support both local demo and production-like deployment through Compose profiles or separate compose overlays.
- The local demo path should be easy to start, while the production-like path should remain available from the main `energy` repository.

## Source Repository Handling
The exact source handling must be decided during implementation. Acceptable options:
- Compose builds from checked-out sibling directories for `energy-frontend` and `energy-backend`.
- The main repository includes Git submodules for frontend and backend.
- Compose references remote build contexts if supported and practical.
- Compose pulls versioned prebuilt images from a registry.

Default preference:
- Keep source in separate repositories.
- Consume `energy-frontend` and `energy-backend` from the main `energy` repository via Git submodules.
- Keep deployment orchestration in the main `energy` repository.
- Avoid requiring users to manually run build commands before `docker compose up`.
- For private repositories, authorize Git access on the host and initialize submodules before running Compose.
- Do not pass GitHub credentials into the default Docker build. The normal local/demo Compose path should consume already checked-out submodule directories.

## Deployment Files
The main repository should eventually contain:
- `compose.yaml` or `docker-compose.yaml` for local/default deployment.
- Optional `deploy/compose.yaml` or similar for production-like deployment.
- `.env.example`.
- deployment documentation in `doc/`.

The compose style should be similar in spirit to the referenced OpenKNX XML Navigator deployment example: one compose file should define the runnable stack so users do not need to understand or manually build each application part first.

Reference:
- https://github.com/kikakeule/OpenKNX-XML-Navigator/blob/main/deploy/deploy-compose.yaml

## Container Registry
Approved initial direction:
- The local/demo path builds application images from source through Docker Compose and tags them locally, for example `energy-frontend-demo:local`.
- The local/demo path must not require pulling a prebuilt application image from Docker Hub, GHCR, or any other image registry.
- GHCR private images are the initial optional private registry choice when prebuilt images are necessary.
- Prefer building from source through Docker Compose for the demo and avoid GHCR unless it is necessary.
- GHCR is available as an optional private image registry when prebuilt images are necessary.
- GHCR is expected to be sufficient for the early phase with the available plan quota if image publishing is disciplined.
- Add a cleanup/retention rule from the beginning.
- Keep only a small set of useful tags, such as `latest`, `demo`, and the last few version tags.
- Delete untagged images.
- Avoid permanently publishing every branch build.
- Normal local/demo deployment must build from the frontend/backend submodules where possible so registry pulls are optional.
- Public base images such as Node and nginx may still be pulled during the Docker build unless a deployment overrides them with internally mirrored images.
- Environments without Docker Hub or public registry access must provide base images through an internal mirror or preloaded images, while still building application images locally from source.
- Keep a self-hosted private Docker Registry as the quick replacement/fallback if GHCR quota, pricing, or policy becomes a problem.

## Open Questions
- What image publication strategy should production-like deployment use when source builds are too slow or unavailable?
- What default domain, TLS, and reverse proxy strategy should be used for production?
