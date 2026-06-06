# Research: Similar Products And Feature Deltas

## Research Questions
- Which features do existing municipal energy management products provide?
- Which features are common in building automation and energy platforms?
- Which gaps or differentiators does this project have?
- Which standards and external APIs matter for Germany and the EU?

## Comparable Municipal Energy Management Products

### LiMBO
LiMBO is directly relevant because the Harsefeld 2023 report was generated with it. Its public material positions it as web-based municipal energy management for monitoring, evaluating, and optimizing municipal properties.

Observed feature set:
- municipal property overview;
- energy reports for past calendar years when enough data exists;
- electricity, heat, water, and energy production;
- RLM and iMSys data integration;
- manual meter reading support with QR code/mobile web workflows;
- heat-data weather correction;
- Strom-Waerme-Diagramm comparison of properties;
- energy reports "at the push of a button";
- automatic data retrieval from metering operators.

Sources:
- https://limbo.energy/funktionen-von-limbo/
- https://limbo.energy/hallokommune/
- https://limbo.energy/wp-content/uploads/LiMBO-Produktkatalog-digital.pdf

Delta for this product:
- add actuator control, not only monitoring/reporting;
- add schedule and simple automation management;
- add explicit energy-consultant workflow for anomalies, estimates, findings, and release;
- add public/guest report portal;
- make REST API and integration security a first-class product requirement.

### INM Management
INM Management is municipal energy-controlling software for properties.

Observed feature set:
- electricity, heat, gas, and water consumption management;
- municipal building/property management;
- equipment and renovation-state data;
- monthly, yearly, and building reports;
- automatic weather correction;
- benchmarking with limit and target values;
- configurable guidelines;
- anomalies and saving-potential hints;
- report archive and PDF/Word availability;
- maintained standard heating values, conversion factors, and weather-correction data.

Source:
- https://management.klimastrategie.de/index

Delta for this product:
- add operational control and automation across buildings;
- add public report release workflow;
- add v1 REST API and external data ingestion/control contracts;
- make consultant review an explicit role and workflow.

### Kom.EMS
Kom.EMS is not a normal SaaS competitor; it is a municipal energy-management system/process framework and knowledge portal. It provides guidance, minimum requirements, and examples for energy-management software and energy reports.

Observed relevance:
- energy-management software should simplify energy controlling and automate workflows;
- energy controlling includes early detection of consumption anomalies;
- it includes reconciliation of meter readings with supplier invoices;
- it includes reconciliation of supplier invoices with supply contracts;
- Kom.EMS provides minimum software and report content guidance.

Source:
- https://www.komems.de/EnergyManagement/software/

Delta for this product:
- use Kom.EMS as requirements validation and checklist material;
- add invoice/contract reconciliation as a future feature candidate;
- keep the product simpler and more operational for v1, but leave room for Kom.EMS-aligned maturity.

Approved product decision:
- Kom.EMS is used as a requirements validation and maturity checklist.
- The v1 demo should align with visible Kom.EMS-style municipal energy-management concepts: monitoring, portfolio views, reports, anomalies, CSV/API ingest, and weather normalization.
- Production v1 should adopt Kom.EMS-aligned basics where they support monitoring and reporting correctness.
- Invoice reconciliation and supply-contract reconciliation remain future roadmap candidates.

## Building Automation And Energy Platforms

### aedifion.io
aedifion.io is relevant for technical building monitoring and open interfaces.

Observed feature set:
- edge-device and MQTT-based connection to local building plants;
- cloud data hub for building/plant/district data;
- RESTful HTTP API for platform functionality;
- MQTT API for streaming data into and out of the platform;
- alarms and live datapoint subscriptions;
- VDI 6041 and ISO 50001 orientation in product material.

Sources:
- https://docs.aedifion.io/en/products/io/
- https://docs.aedifion.io/en/products/io/apis/
- https://docs.aedifion.io/en/products/io/features/

Delta for this product:
- use the edge/MQTT/API pattern as architecture inspiration;
- combine technical monitoring with municipal legal reporting and consultant workflows;
- do not require full technical-monitoring depth for the first frontend demo.

### Siemens Desigo CC
Desigo CC is a large building-management platform.

Observed feature set:
- HVAC, lighting, fire safety, security, and other OT systems in one platform;
- scheduling, occupancy, and trending for energy optimization;
- energy and power reporting;
- calculated and virtual meters;
- power quality monitoring;
- lighting control, blinds, and sensors;
- third-party system integration.

Source:
- https://www.siemens.com/global/en/products/buildings/automation/desigo/building-management/desigo-cc.html

Delta for this product:
- the municipal product should not compete as a full BMS;
- it should integrate with or sit above BMS products;
- control UI must respect local BMS capabilities and safety boundaries.

### Schneider EcoStruxure Building Operation
EcoStruxure Building Operation is a BMS platform for integrated building control.

Observed feature set:
- HVAC, lighting, power, microgrids, renewables, security, fire, and WAGES data;
- mobile-friendly single control center;
- open integration with Schneider and third-party systems;
- metered energy, EV charging, and renewable energy source support.

Source:
- https://www.se.com/ww/en/work/products/product-launch/building-management-system/

Delta for this product:
- model building-control integrations as adapters instead of replacing BMS systems;
- provide municipal portfolio/reporting and public accountability features above local control systems.

### EnergyCAP
EnergyCAP is strong in utility bill management and energy reporting.

Observed feature set:
- utility bill auditing and validation;
- account, meter, vendor, building, and organizational hierarchy;
- facility benchmarking;
- weather data correlation and weather-normalized EUI;
- reports, charts, dashboards, scheduled distribution;
- budgets, rates, tariffs, chargebacks, accounting export;
- project tracking for energy/cost savings;
- REST API for organization energy data.

Sources:
- https://www.energycap.com/utility-bill-energy-management-software/features/
- https://developer.energycap.com/api-getting-started/getting-started/index.html

Delta for this product:
- add Germany/EU municipal report requirements;
- add actor control and automation;
- consider bill validation, budgets, tariffs, and project tracking as later roadmap items.

## Differentiation Hypothesis
The strongest product direction is a municipal-first layer that combines:
- legal/public energy reporting;
- portfolio monitoring;
- role-specific WebUI;
- consultant-in-the-loop recommendations;
- anomaly workflow;
- public report publication;
- practical building-control integration;
- REST-first API plus future MQTT/edge integration.

Most existing municipal products appear stronger at monitoring and reporting than control. Most BMS products appear stronger at control than public municipal reporting. The intended product can sit between those categories.
