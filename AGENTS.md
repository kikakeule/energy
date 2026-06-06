# Agent Guidelines

## Project Context
This repository is for a municipal energy management product. The product is intended to help communities monitor energy usage, control energy-affecting appliances, generate legally useful energy reports, and coordinate energy consultant input.

The frontend is a WebUI. German is the default product language, with English also supported. The backend is planned for v1 and should expose a mostly final REST API between backend, frontend, data providers, and controlled actors.

## Repository Layout
- Main coordination repository: `https://github.com/kikakeule/energy`
- Frontend repository: `https://github.com/kikakeule/energy-frontend`
- Backend repository: `https://github.com/kikakeule/energy-backend`

Requirements, general documentation, Docker Compose deployment files, shared deployment configuration, and cross-project coordination belong in the main `energy` repository. Frontend application code belongs in `energy-frontend`. Backend application code belongs in `energy-backend`.

The project must remain deployable from scratch with Docker Compose from the main `energy` repository. Do not require a user to manually precompile frontend or backend artifacts before running the compose deployment.

## Living Requirements
- Always read `requirements/overview.md` before planning or implementation.
- Also read `requirements/deployment.md` before changing repository layout, Docker Compose, build, runtime, or deployment behavior.
- Treat all files in `requirements/` as living requirements documents.
- Keep `requirements/overview.md` concise. When a topic becomes detailed, move the detail into a specific living requirements document and link it from the overview.
- General documentation belongs in `doc/`.
- When new decisions are made, update the relevant requirements document instead of leaving decisions only in chat history.
- When research adds or changes product assumptions, update both the topic document and `requirements/open-questions.md` when unresolved decisions remain.

## Planning And Alignment
- Do not guess when a product, API, security, data model, or UX decision is unclear. Ask the user.
- During longer tasks, periodically realign with the current plan and the requirements overview.
- After context compaction or a resumed session, reread `requirements/overview.md`, check related topic documents, and realign to the current plan before continuing.
- Keep the plan updated as work progresses.
- If implementation details conflict with requirements, stop and clarify before making irreversible or broad changes.

## Engineering Guidelines
- Prefer simple, maintainable architecture over premature abstraction.
- Prefer a documented REST API contract for frontend/backend communication.
- Favor explicit role-based permissions and auditability for administrative and control actions.
- Treat actuator control as safety-sensitive. Require clear authorization, logging, validation, and rollback/failure handling.
- Plan for secure authentication from the start, including 2FA, role management, and integration with external identity providers.
- Prefer accessible, responsive, multilingual UI patterns.
- Keep public/guest features separate from authenticated administrative features.
- Keep generated reports reproducible and archived.

## Documentation Style
- Write requirements in clear English unless a document specifically captures German UI wording.
- Use concrete acceptance criteria where a feature is ready for implementation.
- Record assumptions explicitly.
- Link source material and research notes from `doc/` or the relevant requirements document.
