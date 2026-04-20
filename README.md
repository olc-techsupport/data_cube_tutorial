# Building Geospatial Data Cubes for Earth Data Science
### A Tutorial for Tribal College Students and Faculty
**Author:** Lilly Jones, PhD, Daear Consulting, LLC  
**Primary Focus:** Pine Ridge (Oglala Lakota)  
**Level:** Beginner  
**License:** AGPL-3.0 license

## What Is a Data Cube?
When scientists study the environment, they collect data across three dimensions
simultaneously: **space** (where), **time** (when), and **variable** (what).
A data cube is a data structure that holds all three dimensions together so you
can ask questions like:

> *"What was the vegetation condition at Pine Ridge in August 2012 compared to
> August 2022? How does that change compare to the drought record?"*

A spreadsheet can't answer that question. A data cube can.

This tutorial teaches you to build and query geospatial data cubes in Python
using real satellite and climate data centered on Pine Ridge and South Dakota
Tribal lands.

## Why Pine Ridge?
Pine Ridge is home to the Oglala Lakota Nation and is one of the largest
reservations in the United States by land area. The land is primarily mixed-grass prairie,
badlands, ponderosa pine hills, shaped by climate, fire, drought, and the
management decisions of the people who steward it.

Understanding environmental change on these lands through data science is not
just a technical exercise. It is a contribution to Tribal sovereignty, land
management capacity, and the long-term health of the community.

## Data Sovereignty
Before you start, read `docs/data_sovereignty.md`.
The data in this tutorial comes from public federal sources including NASA satellites,
NOAA weather stations, Census boundaries. That data describes Indigenous lands.
The frameworks that govern responsible use of that data including OCAP®, CARE, FAIR,
and IEEE 2890-2025 are introduced in the data sovereignty document and
referenced throughout the tutorial.

## Tutorial Structure
| Notebook | Topic | What you will build |
|---|---|---|
| 00 | Orientation | Understanding the data cube concept |
| 01 | Arrays and Dimensions | From numpy to xarray: adding meaning to numbers |
| 02 | Your First Data Cube | MODIS NDVI cube over Pine Ridge |
| 03 | Time Slicing | Querying across years, seasons, and events |
| 04 | Multi-Variable Cube | Adding temperature and precipitation |
| 05 | Spatial Operations | Clip, mask, and reproject with rioxarray |
| 06 | Analysis Patterns | Anomalies, trends, and composites |
| 07 | Open Data Cube Intro | What ODC adds and when to use it |
| 08 | Your Own Question | Build a cube for something you care about |

## Quick Start
```bash
# Clone the repository
git clone https://github.com/daearconsulting/tribal_datacube_tutorial
cd tribal_datacube_tutorial

# Create and activate the environment
conda env create -f environment.yml
conda activate tribal-datacube

# Launch JupyterLab
jupyter lab notebooks/
```

Start with `00_orientation.ipynb`.

## Data
All data is downloaded at runtime from public sources. Nothing is committed
to this repository. See `data/README.md` for the full data inventory and
citation information.

**Sources used in this tutorial:**
- MODIS MOD13Q1 NDVI (250m, 16-day): NASA/ORNL DAAC
- gridMET daily climate (4km): University of Idaho Climatology Lab
- Census TIGER AIANNH boundaries: US Census Bureau

## For Instructors
Each notebook is self-contained and includes:
- A conceptual introduction (no code required)
- Step-by-step code cells with detailed comments
- Discussion questions for the classroom
- A "Going Further" section pointing to more advanced resources

Recommended sequence: notebooks 00–06 in order, then 07 as an optional
advanced session, then 08 as a capstone project.

Estimated time: 2–3 hours per notebook for a classroom session, or self-paced.

## Acknowledgments
This work is part of a broader effort to build
earth data science capacity at Tribal colleges and universities.

Data governance frameworks referenced: OCAP®, CARE Principles, FAIR Principles,
IEEE 2890-2025.
