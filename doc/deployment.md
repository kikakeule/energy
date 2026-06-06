# Deployment Notes

## Local Frontend Demo

The current customer-presentable demo can be started from the main repository with Docker Compose:

```bash
docker compose up --build
```

The default compose file builds the frontend from the `energy-frontend` submodule and serves it on `http://localhost:8080`.

Copy `.env.example` to `.env` only when you need to override the exposed port.

The backend submodule is present but does not yet contain a runnable backend service, so the current compose file intentionally starts the frontend demo only. Add the backend, database, and health checks once their implementation exists.
