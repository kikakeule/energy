---
name: compose-deployment-check
description: Check or implement Docker Compose deployment behavior for the municipal energy project. Use when changing repository layout, compose files, Dockerfiles, environment examples, deployment docs, build steps, service startup, health checks, volumes, or from-scratch setup instructions.
---

# Compose Deployment Check

Read `requirements/overview.md`, `requirements/deployment.md`, and `requirements/architecture.md` before changing deployment behavior.

The main `energy` repository owns compose files, deployment docs, environment examples, and cross-repository setup. Frontend and backend app code stay in their own repositories.

Maintain the from-scratch Compose requirement:

- No manual frontend precompile step.
- No manual backend precompile step.
- No required local Node.js, package-manager, or backend runtime outside Docker for normal deployment.
- Persistent data uses named volumes or documented bind mounts.
- Environment variables are documented with safe examples.
- Core services get health checks once implementation exists.

When choosing source handling, prefer the documented options: sibling checkouts, submodules, remote build contexts, or versioned prebuilt images. Do not invent a new deployment ownership model without updating requirements.

After deployment changes, verify the compose config can be parsed and summarize any checks that could not be run.
