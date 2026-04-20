# Data
All data in this tutorial is downloaded at runtime from public sources.
Nothing is committed to this repository.

## Directory Structure
```
data/
├── cache/          # Downloaded data, created automatically on first run
└── README.md       # This file
```
The `cache/` directory is created automatically when you run the notebooks.
It is listed in `.gitignore` and should never be committed.

## Data Sources

### MODIS MOD13Q1 NDVI
- **What:** 16-day composite NDVI at 250m resolution
- **Source:** NASA ORNL DAAC MODIS Web Service
- **URL:** https://modis.ornl.gov/rst/api/v1/
- **No account required** for point time series queries
- **Citation:** Didan, K. (2021). MODIS/Terra Vegetation Indices 16-Day L3 Global 250m SIN Grid V061. NASA EOSDIS Land Processes DAAC. doi:10.5067/MODIS/MOD13Q1.061
- **Used in:** Notebooks 02–06

### gridMET Daily Surface Meteorology
- **What:** Daily 4km gridded temperature, precipitation, and fire weather variables
- **Source:** University of Idaho Climatology Lab via OPeNDAP
- **URL:** https://www.climatologylab.org/gridmet.html
- **No account required**
- **Citation:** Abatzoglou, J.T. (2013). Development of gridded surface meteorological data for ecological applications and modelling. International Journal of Climatology. doi:10.1002/joc.3413
- **Used in:** Notebooks 04–06

### Census TIGER AIANNH Boundaries
- **What:** American Indian/Alaska Native/Native Hawaiian Areas boundaries
- **Source:** US Census Bureau TIGER/Line Shapefiles (2023 vintage)
- **URL:** https://www.census.gov/cgi-bin/geo/shapefiles/index.php
- **No account required**
- **Citation:** US Census Bureau, TIGER/Line Shapefiles (2023).
- **Governance note:** Census-defined boundaries are for statistical purposes
  only. They do not represent legal jurisdiction or Tribal self-definition.
- **Used in:** Notebooks 02–08

## Data Governance
All data in this tutorial describes Indigenous lands and environments.
The frameworks that guide responsible use are:

- **OCAP®**: https://fnigc.ca/ocap-training/
- **CARE Principles**: https://www.gida-global.org/care
- **FAIR Principles**: https://www.go-fair.org/fair-principles/
- **IEEE 2890-2025**: https://standards.ieee.org/ieee/2890/10318/

See `docs/data_sovereignty.md` for full discussion.
