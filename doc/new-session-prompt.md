# New Session Prompt

Use this prompt to start a new implementation session:

```text
We are building the first customer-presentable frontend demo for a municipal energy management product.

Start by reading these files in the main repository:
- AGENTS.md
- requirements/overview.md
- doc/v1-demo-handoff.md
- requirements/features.md
- requirements/ui-ux.md
- requirements/deployment.md

Important context:
- "V1 demo" means the first customer-presentable frontend demo, not the production v1 backend.
- The demo is Community/Clerk-level only.
- Admin, Community Admin, and Energy Consultant UIs are out of scope for the first demo.
- Everything may be mocked, including login, data, readings, ratings, report download, weather, actor controls, and schedules.
- Mock behavior must use clean API-shaped adapters/interfaces so the real backend can replace it later.
- Use Samtgemeinde Harsefeld-style fictional 2026 mock data.
- Required object types: schools, town halls/admin offices, libraries, fire departments, traffic lights, pumping stations, gyms/sports halls, kindergartens/daycare, public pools.
- Required demo screens: mocked login, portfolio overview, site/building detail, current and historic readings, ratings/anomaly request, actor controls and schedules as mocked clerk workflows, report request/download for imaginary Harsefeld 2026 report, public overview/public reports.
- German is the default UI language; English must be supported.
- DWD weather should be real if practical; otherwise use an API-shaped mock behind the same interface.
- Docker Compose from the main repo should build from source/submodules where possible. Avoid GHCR unless necessary.

Before coding, inspect the current repository layout and confirm whether frontend/backend submodules or repos are present. Then propose or implement the next concrete step needed to build the frontend demo.
```
