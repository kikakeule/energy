---
name: frontend-demo
description: Build or review the first customer-presentable WebUI demo for municipal community users. Use when implementing React/Vite frontend screens, mock data, German/English UI text, responsive layouts, accessibility, traffic-light ratings, charts, actor controls, automations, or report views.
---

# Frontend Demo

Read `requirements/overview.md` and `requirements/ui-ux.md` first. Read `requirements/api.md` when mock data or API-shaped interfaces are involved.

Optimize for a customer-presentable Community/Clerk experience. German is the default UI language; English must remain supportable through translation-ready text.

Use mock data only behind clean API-shaped interfaces so backend replacement is straightforward.

Prioritize:

- Portfolio overview, building detail, current and historic readings, comparisons, rating overview, anomaly/consultant request flow, actor control view, schedules, report request/download, and public overview/report surfaces as required by the current scope.
- Clear, scanable layouts for municipal office users on desktop and tablet.
- Traffic-light status with labels or icons, never color alone.
- Confirmations and clear failure states for control actions, stale data, offline sites, failed imports, failed commands, and missing readings.
- Accessible forms, keyboard navigation, responsive tables, chart alternatives, and locale-aware dates, numbers, currencies, and units.

Avoid exposing technical datapoint details to Community users unless the task requires it.

Before finishing UI work, run available lint/build/test checks and, when a browser is available, inspect the UI at relevant desktop and tablet/mobile widths.
