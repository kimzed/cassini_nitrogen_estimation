# Cassini Nitrogen Estimation

NOx emission estimation from Sentinel-5P satellite data using divergence-based physical modeling.

## Overview

A Cassini Hackathon project that estimates nitrogen oxide (NOx) emissions for specific locations by combining Sentinel-5P NO2 tropospheric column data with Global Forecast System wind fields. The approach uses flux divergence analysis to identify and quantify pollution point sources, achieving sub-2km source localization accuracy.

## Tech Stack

- **Satellite Data:** Sentinel-5P NRTI NO2 (Copernicus)
- **Wind Data:** Global Forecast System
- **Processing:** Python, NumPy
- **Visualization:** Matplotlib

## Method

1. **Data Collection** — Retrieve NO2 concentration rasters and wind vector data from satellite observations
2. **Flux Calculation** — Multiply NO2 concentration by wind vectors to produce a flux map of NO2 movement
3. **Divergence Analysis** — Calculate flux divergence to identify net NO2 outflow per pixel (positive divergence = emission source)
4. **Source Identification** — Detect emission peaks corresponding to point sources (e.g., power plants)
5. **Emission Quantification** — Iterative peak fitting algorithm to estimate emission rates

### Core Equations

```
Flux:       F = L * V * w
Emissions:  E = div(L * V * w) + L * V / tau
```

Where `L` = NOx/NO2 ratio, `V` = NO2 tropospheric column, `w` = wind fields, `tau` = NOx degradation time constant.

### Performance

- Point source localization: < 2km accuracy
- Emissions uncertainty: 42–65%
- Detection limit: 0.03–0.11 kg/s
- Cloud data fraction threshold: 30%

## Context

Built during the **Cassini Hackathon** by a team of 6. The project targets CSRD compliance for industrial NOx reporting, combining Copernicus satellite infrastructure with physics-based emission modeling.

## Team

- Cedric Baron — Geo-data scientist & ML engineer
- Valeriy Litkovskyy — Full-stack developer
- Antonio Luca — Mechanical engineer
- Alice Giacomelli — Business development
- Davide Bencivenga — Industrial engineer
- Alberto Ambrosini — Economics & management
