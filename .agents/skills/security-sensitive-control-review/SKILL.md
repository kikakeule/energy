---
name: security-sensitive-control-review
description: Review safety-sensitive security behavior for actuator control, API credentials, RBAC, audit logging, imports, report publication, and consultant release workflows. Use when implementing or reviewing commands that affect heating, cooling, lighting, shades, blinds, automations, external ingestion, user management, or administrative actions.
---

# Security-Sensitive Control Review

Read `requirements/overview.md`, `requirements/security-auth.md`, `requirements/api.md`, and `requirements/integrations.md` before reviewing or changing safety-sensitive behavior.

Treat actor control, automation, CSV import, API token management, user/role management, report publication, and consultant release decisions as security-sensitive.

Check for:

- Explicit authorization in the backend, not only in the UI.
- Organization and site scoping for users, tokens, datapoints, actors, reports, and integrations.
- MFA policy support for Admin and Community Admin roles.
- Audit logs with principal, action type, target, timestamp, source IP or integration identity, result, and practical before/after summaries.
- Input validation for command payloads, schedules, imported readings, report state transitions, and token metadata.
- Safe command failure behavior, command status, failure reason, and rollback or recovery expectations where applicable.
- Token secrets shown only once, with rotation, disable, delete, expiry, and least-privilege scope considerations.
- Public/guest access kept read-only and separate from authenticated administrative surfaces.

If the security model is unresolved, mark the issue in `requirements/open-questions.md` and ask before implementing production-facing behavior.
