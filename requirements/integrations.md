# Integration Requirements

## Integration Goals
The product must ingest energy data from municipal sites and external providers, and may control actors through local building systems or gateways.

## Initial Integration Types
- CSV import for historic readings.
- REST API for controlled reading ingestion.
- REST API for reading queries.
- REST API for actor control.
- REST API for device inventory, device telemetry, device maintenance state, and device warnings.
- Future edge gateway for remote objects.
- Building automation integrations.
- Weather and climate data for normalization and forecasts.
- Energy market and registry data where useful.

Approved v1/v2 decisions:
- V1 supports CSV import and API ingestion for readings.
- RLM/iMSys integrations are v2 production integration requirements, not v1/demo requirements, unless an easy metering-provider or EWE/LiMBO access path becomes available early.
- DWD weather data integration is required for v1 and should also be represented in the demo.
- Demo DWD/weather integration should be real if practical.
- If real DWD fetching is too much for the first frontend-only demo, use an API-shaped mock with the same interface.
- Demo deployment may set site weather location through Docker Compose configuration.
- Weather location is configured per site by Admin users in the full product.
- SMARD/ENTSO-E should stay out of v1 reports except as future optimization/context sources.
- The first target municipality does not currently run a BMS such as Desigo, EcoStruxure, or Niagara; the known existing system is EWE LiMBO for reporting.
- Loxone is a known building automation protocol/platform in the first real customer context and should be tracked for integration planning.

## Building And Device Protocol Candidates
Potential protocols and integration surfaces to research and validate:
- BACnet for building automation.
- Modbus for meters and industrial devices.
- KNX for lighting, shading, HVAC, and building automation.
- MQTT for gateway/cloud messaging.
- OPC UA for industrial or utility infrastructure.
- EEBus for energy-relevant appliances and smart energy communication.
- Smart Meter Gateway / CLS channel for Germany-specific secure metering/control scenarios.

## Device Integration Scope
- Device integrations should support both smart devices and legacy devices.
- Smart devices may provide telemetry, warnings, maintenance state, and controls through building automation, vendor APIs, gateways, or local protocols.
- Legacy devices may only be represented by manual metadata, imported/manual measurements, and manually maintained maintenance records.
- V1 device categories to model are heat pumps, PV systems, batteries, and ventilation systems.
- Device controls are represented as actor-backed controls in V1 and should integrate with the same permission, confirmation, and audit concepts as actor control.
- Device warnings and maintenance-due events should flow into the same warning/message infrastructure as sensor and consumption warnings.

## External Data Provider Candidates
Potential external data sources to research and validate:
- DWD weather and climate data.
- SMARD market data from Bundesnetzagentur.
- Marktstammdatenregister data for generation assets and energy market master data.
- ENTSO-E Transparency Platform for European electricity market data.
- Energy provider or metering operator APIs where available.

## Researched Integration Notes

### DWD Weather And Climate Data
DWD provides open weather and climate data through its Open Data Server. This is relevant for weather-normalized heat consumption, local weather context, and possibly solar/global-radiation context.

Implementation note:
- Prefer official DWD open data where feasible.
- A convenience API may be useful for frontend/backend prototyping, but production reporting should keep source attribution and data provenance clear.
- DWD integration is required for v1 and should be represented in the demo.
- Use real DWD data in the demo if practical.
- If real DWD fetching is not practical for the first frontend-only demo, provide an API-shaped mock behind the same interface.
- Demo deployment may set site weather location through Docker Compose configuration.
- In the full product, Admin users configure weather location per site.

Source:
- https://dwd.de/EN/ourservices/opendata/opendata.html

### SMARD
SMARD is the Bundesnetzagentur electricity market data platform. It provides market data for Germany and Europe. Downloaded market-data visual data is CC-BY 4.0 and should be attributed to "Bundesnetzagentur | SMARD.de".

Potential uses:
- context for electricity prices and market trends;
- dynamic-price context for future optimization;
- public contextual reporting, not core municipal meter data.
- SMARD should stay out of v1 reports except as future optimization/context.

Source:
- https://www.smard.de/en/datennutzung

### Marktstammdatenregister
The MaStR has documented web services and data downloads. The 2025-10-01 V25.2 documentation describes HTTPS-only access, API/web-service users, rate/availability considerations, test systems, and production/test/vorschau environments.

Potential uses:
- validate or enrich PV/generation-asset metadata;
- identify registered generation units relevant to municipal sites;
- future registry synchronization.

Sources:
- https://www.marktstammdatenregister.de/MaStRHilfe/files/webdienst/2025-10-01%20Dokumentation%20MaStR%20Webdienste%20V25.2.pdf
- https://marktstammdaten.api.bund.dev/

### ENTSO-E Transparency Platform
ENTSO-E's Transparency Platform publishes European electricity generation, load, transmission, and balancing data under EU transparency regulation.

Potential uses:
- EU-wide market and grid context;
- electricity price/load context for future optimization features;
- not a replacement for local municipal metering.
- ENTSO-E should stay out of v1 reports except as future optimization/context.

Source:
- https://www.entsoe.eu/data/transparency-platform/

### EEBus And Smart Meter Gateway Context
EEBus provides IP-based secure machine-to-machine communication for home/building energy use cases. Its SHIP security is described as aligned with the Smart Meter Gateway HAN interface in BSI TR-03109. EEBus also describes power-limitation use cases around the grid connection point and Germany's intelligent metering system.

Potential uses:
- future connection to energy-relevant appliances, wallboxes, heat pumps, and EMS systems;
- Germany-specific control scenarios around power limitation and Smart Meter Gateway context.

Source:
- https://www.eebus.org/solutions/

### Building Automation Platforms
Large BMS platforms such as Siemens Desigo CC and Schneider EcoStruxure already provide HVAC, lighting, metering, power, and control integration. This product should integrate with such systems instead of trying to replace them in v1.

Sources:
- https://www.siemens.com/global/en/products/buildings/automation/desigo/building-management/desigo-cc.html
- https://www.se.com/ww/en/work/products/product-launch/building-management-system/

## Open Integration Questions
- Which integrations are required for the first customer demo?
- Which integrations are required for v1 production?
- Will the product provide its own managed data endpoint for field devices?
- Should remote sites use a local gateway?
- How should local gateways authenticate?
- What offline buffering is required?
- Which building automation protocols are most common in the first target communities?
