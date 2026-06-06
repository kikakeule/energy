---
name: requirements-alignment
description: Align municipal energy product work with living requirements. Use when planning or implementing features, changing assumptions, updating documentation, or checking whether a task is consistent with requirements/overview.md and related requirements documents.
---

# Requirements Alignment

Read `requirements/overview.md` first.

Then read the most relevant topic documents before planning or editing:

- Product scope or feature behavior: `requirements/features.md`
- Roles, permissions, or access: `requirements/user-roles.md`
- API shape or integration behavior: `requirements/api.md`, `requirements/integrations.md`
- Auth, RBAC, audit, or control safety: `requirements/security-auth.md`
- UI behavior, language, or accessibility: `requirements/ui-ux.md`
- Repository layout, runtime, or deployment: `requirements/architecture.md`, `requirements/deployment.md`
- Reports, PDFs, consultant workflow, or archives: `requirements/reporting.md`
- Unresolved decisions: `requirements/open-questions.md`

Keep `requirements/overview.md` concise. Move detailed decisions into the specific topic document and link from the overview only when needed.

When a new product decision is made, update the relevant requirements document in the same change. If the decision leaves uncertainty, update `requirements/open-questions.md`.

Stop and ask the user before making broad product, API, security, data model, or UX decisions that are not resolved by the requirements.
