# Emisat: Innovative NOx Emission Reporting

## 💎 Idea

Emisat addresses the challenges posed by the EU's Corporate Sustainability Reporting Directive (CSRD) by providing cheap, fast, and scalable NOx emission reporting for specific locations. Our innovative approach bridges the gap between costly on-site measurements and imprecise satellite data, offering an accurate and accessible solution for companies transitioning to proactive environmental management.

## 🛰️ EU Space Technologies

We leverage:
- Sentinel-5P NRTI NO2 data
- Global Forecast System wind data
- State-of-the-art physical modeling based on scientific research

Our approach allows for:
- High-resolution NOx emission estimates
- Improved spatial granularity
- Pinpointing specific emission sources
- Tracking pollution impact on nearby communities

## ⛑️ Addressing Challenges

Emisat directly addresses emissions and carbon footprint reporting by:
- Providing precise NOx emission reporting
- Using European space data from Copernicus (Sentinel-5P)
- Enabling effective emission tracking and management
- Supporting CSRD compliance
- Contributing to climate change mitigation efforts

## 💰 Business Plan

**Funding Needed**: €500,000

**Use of Funds**:
- Software Development: €200,000
- Operational Expenses: €150,000
- Marketing and Sales: €100,000
- Working Capital: €50,000

**Revenue Streams**:
1. SaaS Platform (€500/customer/month)
2. Consultancy Services (€10,000/project)

**Financial Projections**:
- Year 1: Revenue €163,000 | Net Loss €197,000
- Year 2: Revenue €324,000 | Net Loss €96,000
- Year 3: Revenue €792,000 | Net Profit €312,000

**Break-even**: Achieved in Year 3

**Customer Acquisition**: 
- Estimated CAC: €2,000
- Strategy: Start local, expand regionally and internationally

## 🛠️ Services

1. Software as a Service (SaaS):
   - API-based emission data processing
   - Comprehensive emission reports
   - Subscription-based pricing

2. Consultancy services:
   - Expert partnerships for emission mitigation and compensation

**Target Clients**:
- Heavy industry
- CSRD reporting consultancy companies

## 🗺️ Roadmap

1. Improve accuracy with potential ML integration
2. Expand to methane and CO2 estimation
3. Pursue European certification for CSRD compliance
4. Recruit an atmospheric scientist
5. Expand to new markets:
   - Livestock farmers
   - Governmental agencies

## 🤼 Team

- **Cédric Baron**: Geo-data scientist & ML engineer
- **Valeriy Litkovskyy**: Full-stack software developer
- **Antonio Luca**: Mechanical engineer with automation focus
- **Alice Giacomelli**: Banking and business support expert
- **Davide Bencivenga**: Industrial engineer with generative AI focus
- **Alberto Ambrosini**: Economics and management professional

## Appendix: Physical Modeling

### High-Level Overview

Our model combines Copernicus NOx measurements with wind data to identify and quantify pollution sources. The process works as follows:

1. **Data Collection**: We start with a raster of NO2 concentrations from satellite observations and corresponding wind vector data (speed and direction) for each pixel.

2. **Flux Calculation**: By multiplying the NO2 concentration with the wind vector, we calculate a flux map showing the movement of NO2 across the area.

3. **Divergence Analysis**: The core of our method lies in calculating the divergence of this flux. Divergence measures the net outflow of NO2 from each pixel. A positive divergence indicates a source, as more NO2 is flowing out than in.

4. **Source Identification**: To identify and quantify emissions from specific sources like power plants, we analyze the divergence patterns. Strong positive divergence peaks often correspond to point sources.

5. **Emission Quantification**: We use an iterative peak fitting algorithm to quantify emissions from these peaks.

### Technical Details

Our model calculates NOx flux using the following equation:

```
F = L*V*w

Where:
F = NOx flux
L = NOx/NO2 ratio
V = NO2 tropospheric column
w = wind fields
```

Emissions are calculated as:

```
E = D + S = ∇(L*V*w) + L*V/τ

Where:
E = Emissions
D = Divergence of flux
S = Sinks
τ = Time constant for NOx degradation
```

Key features:
- Point source localization accuracy: < 2km
- Emissions uncertainty: 42-65%
- Detection limit: 0.03-0.11 kg/s
- Cloud data fraction threshold: 30%

For more details on our methodology, please contact our team.
