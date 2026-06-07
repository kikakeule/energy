# Municipal Energy Management Product - Requirements Overview

## Product Goal
Build a software product for communities to improve energy usage across many distributed properties and infrastructure objects. The product must support monitoring, control, reporting, and consultant-assisted recommendations.

The first project phase focuses on a customer-presentable frontend. A v1 backend will follow and should use a mostly final REST API contract from the beginning.

## Repository Strategy
- Main coordination repository: `https://github.com/kikakeule/energy`
- Frontend repository: `https://github.com/kikakeule/energy-frontend`
- Backend repository: `https://github.com/kikakeule/energy-backend`

Requirements, general documentation, Docker Compose deployment files, and cross-project coordination belong in the main `energy` repository. The frontend application lives in `energy-frontend`; the backend application lives in `energy-backend`.

The project must be usable from scratch through Docker Compose from the main repository, without a manual frontend or backend precompile step.

## Core Capabilities
- Monitor current and historic energy readings.
- Compare consumption against prior years, estimates, benchmarks, and expected usage.
- Rate readings and properties using a green/yellow/red traffic-light model.
- Control energy-affecting actors such as heating, cooling, lighting, shades, and blinds.
- Track energy-relevant devices such as heat pumps, PV systems, batteries, and ventilation systems, including measurements, warnings, maintenance, and available controls.
- Configure simple automations and time schedules.
- Generate annual energy reports similar to the Harsefeld 2023 report.
- Support community branding such as a community logo in the UI and reports.
- Allow community users to request consultant review for anomalous readings.
- Allow energy consultants to add findings, set estimates, and release reports.
- Provide a public/guest overview and public report downloads without login.

## Target Objects
The system must handle many far-apart, sometimes remote, objects with different monitoring and control requirements:
- Schools
- Town halls and administrative offices
- Libraries
- Fire departments
- Traffic lights
- Pumping stations
- Gyms and sports halls
- Kindergartens and daycare facilities
- Public pools
- Public buildings, community halls, pools, street lighting, and other municipal assets

## User Levels
The initial role model is documented in `requirements/user-roles.md`:
- Admin
- Community
- Community Admin
- Energy Consultant
- Guest/Public

## Key Requirement Documents
- `requirements/features.md`
- `requirements/user-roles.md`
- `requirements/api.md`
- `requirements/security-auth.md`
- `requirements/ui-ux.md`
- `requirements/architecture.md`
- `requirements/deployment.md`
- `requirements/reporting.md`
- `requirements/integrations.md`
- `requirements/mobile-app.md`
- `requirements/open-questions.md`

## General Documentation
- `doc/report-gap-analysis.md`
- `doc/research-similar-products.md`
- `doc/project-splitting-and-stack.md`

## Initial Assumptions
- German is the default UI language; English is also required.
- REST is the preferred API style.
- The v1 backend should already define stable concepts for readings, datapoints, devices, actors, automations, reports, users, and roles.
- Data import via CSV is required for historical readings.
- API security for external data ingestion and actor control is a required open topic and must be resolved before production use.
- Docker Compose must be the default from-scratch deployment path.
