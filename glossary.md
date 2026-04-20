# Glossary
Terms used throughout this tutorial. Refer back here whenever you
encounter an unfamiliar concept.

## Data Cube Concepts
**Array**
A grid of numbers. In Python, numpy arrays are the foundation of all
scientific computing. A 2D array is like a spreadsheet. A 3D array adds
a third dimension, which could be for example, rows × columns × time.

**Dimension**
An axis of an array. A geospatial data cube typically has three dimensions:
latitude, longitude, and time. A multi-variable cube adds a fourth: variable.

**Coordinate**
The actual values along a dimension. If latitude is a dimension, the
coordinates might be `[43.0, 43.25, 43.5, ...]`. Coordinates make an array
meaningful because they tell you *where* and *when* each value belongs.

**xarray Dataset**
The core Python data structure for data cubes. An xarray Dataset holds one
or more named variables (like `ndvi`, `temperature`, `precipitation`), each
with shared dimensions (like `lat`, `lon`, `time`). Think of it as a
dictionary of labeled numpy arrays that all share coordinate systems.

**xarray DataArray**
A single labeled array within an xarray Dataset. If a Dataset is like a
spreadsheet workbook, a DataArray is like one sheet.

**Chunk**
A piece of a large array that fits in memory. When working with large data
cubes, Dask divides arrays into chunks that are processed one at a time.
This allows you to work with datasets larger than your computer's RAM.

**Zarr**
A storage format designed for chunked, compressed N-dimensional arrays.
Zarr files can be stored locally or in cloud storage (such as Cyverse) and
accessed efficiently in parallel.

**NetCDF**
Network Common Data Form: a widely used file format for scientific array
data, especially climate and weather data. Files end in `.nc`.

## Geospatial Concepts
**CRS: Coordinate Reference System**
The mathematical framework that defines how coordinates (like latitude and
longitude) map to locations on Earth. Different data sources often use
different CRS;  combining them requires reprojecting to a common CRS.
EPSG:4326 is the most common geographic CRS (latitude/longitude, WGS84).
EPSG:5070 is Albers Equal Area CONUS, good for area calculations in the US.

**EPSG Code**
A number that identifies a specific CRS. EPSG stands for European Petroleum
Survey Group, which maintains the registry. Common codes:
- EPSG:4326 = WGS84 geographic (latitude/longitude)
- EPSG:3857 = Web Mercator (used by Google Maps, OpenStreetMap)
- EPSG:5070 = Albers Equal Area CONUS (good for US area calculations)

**Bounding Box (bbox)**
A rectangle defined by minimum and maximum coordinates:
`(min_longitude, min_latitude, max_longitude, max_latitude)`.
Used to specify the spatial extent of a data request.

**Raster**
A grid of cells (pixels), each with a value. Satellite images are rasters.
Each pixel covers a specific area on the ground ex. for MODIS NDVI, each
pixel covers 250m × 250m.

**Vector**
Geospatial data stored as points, lines, or polygons with attributes.
The Pine Ridge boundary is a vector polygon. Census data is vector.
Rasters and vectors are the two fundamental data types in GIS.

**Spatial Resolution**
The size of one pixel in a raster dataset. MODIS NDVI is 250m resolution, meaning
each pixel covers 250 meters on the ground. Higher resolution = smaller
pixels = more detail, but also larger files.

**Temporal Resolution**
How frequently data is collected. MODIS MOD13Q1 is a 16-day composite —
one image every 16 days. gridMET is daily. PDSI is monthly.

**Reproject**
Change the CRS of a dataset so it aligns with other datasets. Required
when combining data from different sources.

**Clip/Mask**
Crop a raster to a specific geographic boundary. Clipping cuts the
bounding box; masking sets pixels outside the boundary to NaN.

## Remote Sensing Concepts
**NDVI: Normalized Difference Vegetation Index**
A measure of vegetation greenness derived from satellite imagery.
Calculated as `(NIR - Red) / (NIR + Red)` where NIR is near-infrared
reflectance and Red is visible red reflectance.
Values range from -1 to 1. Healthy vegetation is typically 0.3–0.8.
Bare soil or drought-stressed vegetation is typically 0.1–0.3.

**MODIS**
Moderate Resolution Imaging Spectroradiometer: a sensor on NASA's Terra
and Aqua satellites. Provides global coverage every 1–2 days at resolutions
of 250m to 1km. MOD13Q1 is the 16-day NDVI composite product.

**Composite**
A single image created by combining multiple images over a time period.
The MODIS 16-day composite takes the best-quality pixel from 16 days of
observations, reducing cloud contamination.

**Anomaly**
The difference between an observed value and the long-term average.
A positive NDVI anomaly means vegetation was greener than usual.
A negative anomaly means vegetation was less green than usual.
Anomalies reveal unusual events like droughts, fires, and floods.

## Climate Data Concepts
**gridMET**
A gridded daily surface meteorological dataset covering the continental US
at 4km resolution. Provides temperature, precipitation, humidity, wind,
and fire weather indices. Developed by the University of Idaho.

**OPeNDAP**
Open-source Project for a Network Data Access Protocol: a protocol for
accessing scientific data over the internet. gridMET and MACAv2 are accessed
via OPeNDAP in this tutorial. You request only the data you need rather than
downloading entire files.

**PDSI: Palmer Drought Severity Index**
A measure of drought severity that integrates temperature, precipitation,
and soil moisture. Negative values indicate drought; -2 to -3 is moderate
drought; below -4 is extreme drought.

## Python Libraries
**numpy**
The foundation of scientific computing in Python. Provides fast N-dimensional
arrays. Most geospatial Python libraries are built on numpy.

**xarray**
Labeled N-dimensional arrays. Extends numpy with named dimensions,
coordinates, and attributes. The primary library for working with
climate and Earth science data cubes.

**rioxarray**
Extends xarray with geospatial capabilities such as CRS management, reprojection,
clipping, and raster I/O. The `rio` accessor on xarray objects.

**geopandas**
Extends pandas with geometry support for vector data. Used for working
with points, lines, and polygons (like Tribal boundaries).

**rasterio**
Low-level library for reading and writing raster files (GeoTIFF, NetCDF).
rioxarray uses rasterio under the hood.

**Open Data Cube (ODC)**
A platform for managing large collections of Earth observation data as
analysis-ready data cubes. Adds indexing, cataloging, and production-scale
access on top of xarray. Introduced in notebook 07.
