# Harsefeld 2023 Energy Report Gap Analysis

## Source
Local document inspected: `C:/Users/Sven/Downloads/energiebericht_2023_samtgemeinde_harsefeld.pdf`

The report has 26 pages and covers the Samtgemeinde Harsefeld reporting period 2020-2023. It was created on 27.05.2025 with LiMBO.

## Report Structure Observed
- Introduction.
- Investigated properties.
- Cost analysis:
  - electricity;
  - heat;
  - water;
  - total costs.
- Consumption analysis:
  - electricity;
  - heat;
  - water;
  - CO2 equivalents.
- Electricity production:
  - production;
  - self-consumption;
  - feed-in.
- Comparative analysis of property portfolio.

## Most Important Missing Product Requirements
1. Legal energy report compliance: support yearly and multi-year municipal reporting, publication status, deadlines, and stable archived released reports.
2. Property and portfolio model: support sites, addresses, building categories, municipalities/member municipalities, net floor area, metering points, and separate consumption categories.
3. Cost tracking: support electricity, heat, and water costs, cost trend, total cost, and cost per resident.
4. Weather-normalized heat consumption: heat reporting must distinguish raw cost-relevant consumption from weather-adjusted comparison values.
5. Benchmarking and ratings: support kWh/m2*a indicators, reference values, percentage deviations, and traffic-light rating logic.
6. CO2 accounting: support emission factors per energy carrier and special handling for renewable electricity procurement.
7. Water and production data: support water consumption plus electricity production, self-consumption, and grid feed-in.
8. Data completeness and comparability: support notes for incomplete years, baseline years, and billing periods that are not calendar-aligned.
9. Portfolio visualizations: support category-level cost/consumption charts, CO2 trends, production trends, and Strom-Waerme-Diagramm style prioritization.
10. Public and internal report split: support public summary reports while retaining internal property-level detail.
11. Measure tracking: capture building condition, age, renovations, planned measures, economic assessment, and saving potential.
12. Contact and metadata: reports should include responsible contact, creation date, source data status, and tool/version metadata.

## Implications For V1
- The reporting module must not be treated as a simple PDF export. It needs a data model for report periods, calculations, consultant findings, release workflow, public visibility, and archived versions.
- The monitoring model must include enough metadata for reporting: media, costs, CO2 factors, net floor area, building category, and comparability notes.
- Rating logic should be designed to support both operational anomalies and annual report benchmarking.
