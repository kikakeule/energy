# Deployment Notes

## Local Frontend Demo

The current customer-presentable demo can be started from the main repository with Docker Compose:

```bash
docker compose up --build
```

The default compose file builds the frontend from the local `energy-frontend` submodule, tags the result as `energy-frontend-demo:local`, and serves it on `http://localhost:8080`.

Copy `.env.example` to `.env` only when you need to override the exposed port or base images.

## Private Repository Access

The application source repositories are private. Authorize Git on the host before starting Compose, then initialize the submodules locally. Compose must not need GitHub credentials for the normal demo path because it builds from the checked-out submodule directories.

Git access must cover the main repository and both private submodule repositories:

- `kikakeule/energy`
- `kikakeule/energy-frontend`
- `kikakeule/energy-backend`

Recommended SSH flow:

```bash
git config --global url."git@github.com:".insteadOf "https://github.com/"
git clone --recurse-submodules git@github.com:kikakeule/energy.git
cd energy
git submodule update --init --recursive
docker compose up --build
```

Configure the HTTPS-to-SSH rule before cloning when using SSH. The main repository may be cloned through SSH directly, but `.gitmodules` currently records HTTPS submodule URLs.

HTTPS with Git Credential Manager or `gh auth login` is also valid:

```bash
gh auth login
gh auth setup-git
git clone --recurse-submodules https://github.com/kikakeule/energy.git
cd energy
git submodule update --init --recursive
docker compose up --build
```

For an existing checkout, refresh the configured submodule URLs and fetch missing private submodules:

```bash
git submodule sync --recursive
git submodule update --init --recursive
docker compose up --build
```

If SSH is preferred while `.gitmodules` uses HTTPS URLs, configure Git once on the machine:

```bash
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

## Registry Use

The local demo does not require a pushed application image from Docker Hub, GHCR, or another image registry. Docker Compose compiles the frontend inside the Docker build from the local submodule source.

The frontend service sets `pull_policy: build` so Compose builds `energy-frontend-demo:local` from source instead of trying to pull that application image from a registry.

The build still uses base images and npm packages:

- `node:20-alpine` builds the frontend.
- `nginx:1.27-alpine` serves the built static assets.
- `npm ci` downloads frontend dependencies unless they are already cached by the builder.

For private or restricted environments, mirror those base images internally and override them in `.env`:

```env
FRONTEND_NODE_IMAGE=registry.example.local/node:20-alpine
FRONTEND_NGINX_IMAGE=registry.example.local/nginx:1.27-alpine
```

If the environment cannot reach Docker Hub or another configured registry, preload or mirror the base images first. The application image itself is still built locally from source by Compose; only the generic base images need to be available to Docker.

Useful diagnostics:

```bash
docker compose config
docker pull node:20-alpine
docker pull nginx:1.27-alpine
docker compose build --pull=false frontend
```

If `docker pull node:20-alpine` hangs or fails, fix Docker Desktop registry/proxy access or point `FRONTEND_NODE_IMAGE` and `FRONTEND_NGINX_IMAGE` at an internal mirror before retrying the Compose build.

## One-Click Demo

For compose, use `deploy/frontend-demo.compose.yaml` when manual checkout should be avoided. This compose file does not build a Docker image from the private source and does not mount the Docker socket. Instead:

1. `build-frontend` starts from `node:20-alpine`.
2. It uses a short-lived fine-grained GitHub token to clone `kikakeule/energy` and its private submodules.
3. It unsets the token before `npm ci` and `npm run build`.
4. It writes the built frontend assets into the `frontend_dist` named volume.
5. `frontend` serves that volume with `nginx:1.27-alpine`.

Minimal token scope:

- Fine-grained personal access token.
- Repository access only for `kikakeule/energy`, `kikakeule/energy-frontend`, and `kikakeule/energy-backend`.
- Repository permission `Contents: Read-only`.
- Short expiry, preferably one day or less for a demo install.

Install options:

- Include the compose file if the repository is already available:

```yaml
include:
  - /mnt/tank/apps/harsefeld/energy/deploy/frontend-demo.compose.yaml
```

- Or paste the contents of `deploy/frontend-demo.compose.yaml` into a custom App YAML editor.

Set these variables, or replace the placeholders in the pasted YAML:

```env
GITHUB_TOKEN=<fine-grained-read-only-token>
GIT_REF=master
FRONTEND_HTTP_PORT=8080
```

Optional base-image overrides for restricted networks:

```env
DEMO_BUILDER_IMAGE=registry.example.local/node:20-alpine
DEMO_NGINX_IMAGE=registry.example.local/nginx:1.27-alpine
```

After the first successful install, revoke the GitHub token. The frontend can keep serving from the named volume. A reinstall or update that rebuilds from GitHub needs a fresh short-lived token.

Do not use a bootstrap container with `/var/run/docker.sock` mounted for this demo path. That would let the container control the Docker host and would combine host-level Docker control with a private repository token.

The backend submodule is present but does not yet contain a runnable backend service, so the current compose file intentionally starts the frontend demo only. Add the backend, database, and health checks once their implementation exists.
