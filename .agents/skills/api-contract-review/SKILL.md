---
name: api-contract-review
description: Review or design REST/OpenAPI contracts for the municipal energy product. Use when working on backend endpoints, frontend API clients, OpenAPI files, external ingestion, actor control APIs, report APIs, RBAC checks, or API compatibility between energy, energy-frontend, and energy-backend.
---

# API Contract Review

Read `requirements/overview.md`, `requirements/api.md`, `requirements/security-auth.md`, and `requirements/architecture.md` before reviewing or changing API behavior.

Prefer explicit REST resources and stable OpenAPI contracts. Keep frontend mock APIs shaped like the planned backend API.

Check each API change for:

- Clear resource ownership across organization, site, building, datapoint, actor, report, user, and role concepts.
- Backend-enforced RBAC and organization or site scoping.
- Audit logging for control actions, role changes, token management, report publication, imports, and consultant release decisions.
- Validation of units, timestamps, source identity, quality status, import method, command payloads, and report workflow state.
- Public endpoints separated from authenticated administrative endpoints.
- Machine/API credential handling that avoids leaking token secrets after creation.
- Compatibility with generated frontend clients once OpenAPI exists.

For actor control APIs, require command status, failure reason, authorization, logging, and safe failure behavior. Treat these as safety-sensitive even in demo code.

If a contract decision is unresolved, update or reference `requirements/open-questions.md` instead of guessing.
