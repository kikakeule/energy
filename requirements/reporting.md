# Reporting Requirements

## Goal
The system must generate municipal energy reports similar to the Harsefeld 2023 energy report. Reports should support legal/public reporting, internal analysis, consultant findings, and future AI-generated recommendations.

## Report Workflow
- Community user requests report.
- System generates draft from available data.
- Energy Consultant reviews draft.
- Energy Consultant adds findings, estimates, and recommendations.
- Energy Consultant releases report.
- Authorized users can download released report.
- Report can be marked public and become available to Guest/Public users.
- Final report approval and release authority belongs to the Energy Consultant role.
- Community/Admin roles may request, view, download, and prepare inputs where permitted, but they do not perform final release unless a later requirement changes this.
- Reports are released/downloaded as PDF only in the initial scope.
- Report edits happen through WebUI and backend/API data structures before final PDF generation or release.
- Word export and separate editable HTML draft export are not required initially, but the design should not prevent adding them later.

## Report Templates
Approved decision:
- Future product direction is configurable report templates.
- The report system must not be limited to a single hardcoded Harsefeld or Niedersachsen template.
- For the first clerk-level frontend demo, provide a mocked downloadable report positioned as an imaginary Harsefeld 2026 energy report.
- For the first clerk-level frontend demo, the mocked report should use the provided Harsefeld logo/branding.
- The demo PDF must use the provided Harsefeld PNG logo or the configured logo asset; it must not use a hand-drawn or invented substitute logo.
- Report layout must keep decorative boxes, status panels, and text from overlapping the logo.
- Downloaded PDFs should be visually checked after layout changes so logo, heading, and summary boxes do not obscure each other.
- The first demo may exclude admin/consultant-level template configuration UI unless it is necessary to properly define API-shaped interfaces.

## Report Contents
The Harsefeld report indicates these content areas should be supported:
- Title, municipality, reporting period, generation date.
- Community logo or configured report branding where available.
- Introduction and reporting context.
- List of investigated properties and sites.
- Building category and address.
- Net floor area where available.
- Cost analysis for electricity, heat, and water.
- Total costs and cost trend.
- Cost per resident where resident count is available.
- Resident count is postponed until after the first frontend demo.
- Consumption analysis for electricity, heat, and water.
- Weather-normalized heat consumption.
- CO2 equivalents for electricity and heat.
- Electricity production.
- Self-consumption and feed-in.
- Category-level comparisons.
- Building benchmark comparison using kWh/m2*a indicators.
- Strom-Waerme-Diagramm style prioritization.
- Notes about incomplete or non-comparable years.
- Recommendations for further investigations and savings measures.
- Contact information for responsible municipal staff.

## Legal Reporting Considerations
The Harsefeld report references Niedersachsen requirements and treats 2022 as a reporting baseline after changed reporting systematics. The product must support report periods, publication status, and comparability notes.

Researched Niedersachsen requirements:
- NKlimaG section 17 requires municipalities to create and publish an energy report.
- The report is intended to disclose energy use and identify reduction and cost-saving opportunities.
- Minimum content includes annual costs for electricity and heating energy, the underlying consumption, and related CO2 emissions.
- For municipal buildings with separate data, annual electricity and heating consumption must be shown in relation to usable area.
- Heating energy consumption must be weather-normalized using a recognized technical procedure.
- The first report was required for calendar year 2022 by 31.12.2023; later reports cover three consecutive calendar years beginning with 2023 and are due by 31 December of the following year.

Sources:
- https://voris.wolterskluwer-online.de/browse/document/d959b1ac-0d30-3ad4-bfcf-9814feb2fa45
- https://www.klimaschutz-niedersachsen.de/zielgruppen/kommunen/Kommunales-Energiemanagement/KEM_Energiebericht.php

Exact legal requirements must still be tracked per target state/region, because this project may serve communities beyond Niedersachsen.

## Public Vs Internal Reports
- Public reports hide site-level details by default.
- Guest/Public users receive aggregated or summarized report data unless a report section or data item is explicitly marked public.
- Public report publication needs visibility controls, with the safe default being "hide detail from public."
- Public reports may summarize details and omit sensitive internal analysis.
- Internal reports should support detailed property-level analysis and consultant notes.
- A released report version must remain stable after publication.

## Future AI Support
AI may later assist with anomaly analysis and saving suggestions. Early versions keep the consultant in the loop.

## Later Reporting Feature Candidates
Based on comparable products and Kom.EMS guidance:
- Budget tracking.
- Rate/tariff tracking.
- Project and measure tracking with expected and actual savings.
- Scheduled report distribution.

SMARD and ENTSO-E market/grid data are future optimization/context sources and should stay out of v1 reports.

## V3 Roadmap Candidates
- Reconciliation of meter readings with supplier invoices.
- Reconciliation of invoices with supply contracts.

These features are part of the long-term product vision for municipal energy controlling, but excluded from the first frontend demo and not required for core v1 unless a pilot customer makes them mandatory.
- Word export or separate editable HTML draft export.
