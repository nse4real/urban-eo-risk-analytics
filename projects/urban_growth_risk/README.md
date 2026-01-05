# Urban Expansion & Informality Detection

## Executive summary
Rapid urban growth becomes risky when it is fast, spatially concentrated, and misaligned with infrastructure and service capacity.  
This project develops an Urban Growth Risk Index to help planning and policy teams prioritise areas where recent expansion may be creating downstream pressure.

## Decision context
**Intended users**
- Urban planners
- Policy and infrastructure teams

**Decisions supported**
- Prioritisation of inspections and reviews
- Targeting of planning and infrastructure assessments

**Consequences of inaction**
- Infrastructure stress
- Increased flood exposure
- Reactive rather than anticipatory planning

## What problem this actually solves
Land-cover maps show where growth occurred, but not which growth patterns create risk.  
This project focuses on growth **speed, abruptness, exposure, and infrastructure context**, not classification detail alone.

## Urban Growth Risk Index
### What the index represents
A composite indicator of where recent urban growth patterns are most likely to create planning or service-delivery pressure.

### Components
- Built-up expansion rate  
- Temporal abruptness of change  
- Population or building exposure  
- Proximity to roads and drainage proxies  

### Interpretation
Higher scores indicate priority for further investigation, not enforcement.

### Non-uses
- Not a legal determination
- Not a prediction of future growth

## Data sources
- Satellite imagery
- Population or building proxies
- Infrastructure layers

Known constraints and gaps are documented explicitly.

## Method overview
- Supervised classification
- Time-series change detection
- Aggregation to administrative units
- Composite index construction

## Validation and confidence
- Stratified sampling
- Component-level uncertainty discussion
- Confidence flags for outputs

## Limitations and non-claims
- Resolution trade-offs
- Proxy uncertainty
- Governance assumptions

## Connection to flood risk
Urban growth patterns identified here inform flood exposure analysis in Project 2.