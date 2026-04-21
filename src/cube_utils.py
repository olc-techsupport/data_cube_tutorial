"""
cube_utils.py — Shared helper functions for the tribal data cube tutorial.

These utilities are used across multiple notebooks. They handle:
- Downloading and caching boundary data for Pine Ridge and SD Tribal Nations
- Fetching MODIS NDVI and gridMET climate data
- Common xarray operations used throughout the tutorial

All functions follow the tutorial's design principles:
- Real data only — no synthetic data
- Cache to data/ directory to avoid repeated downloads
- Clear error messages when data is unavailable
- Inline comments explaining what each step does
"""

from __future__ import annotations

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import requests

# ── Paths ─────────────────────────────────────────────────────────────────────
TUTORIAL_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR      = TUTORIAL_ROOT / "data"
CACHE_DIR     = DATA_DIR / "cache"

try:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
except FileExistsError:
    pass

# ── Pine Ridge bounding box ───────────────────────────────────────────────────
# (min_lon, min_lat, max_lon, max_lat) — WGS84
PINE_RIDGE_BBOX = (-103.5, 42.5, -101.5, 43.8)

# ORNL DAAC MODIS Web Service
ORNL_BASE     = "https://modis.ornl.gov/rst/api/v1"
MODIS_PRODUCT = "MOD13Q1"
MODIS_BAND    = "250m_16_days_NDVI"
NDVI_SCALE    = 0.0001
NDVI_FILL     = -3000

# gridMET OPeNDAP base
GRIDMET_BASE  = "https://thredds.northwestknowledge.net/thredds/dodsC/MET"


# ── Boundary data ──────────────────────────────────────────────────────────────

def load_pine_ridge_boundary():
    """
    Load the Pine Ridge Reservation boundary from Census TIGER AIANNH.

    Returns a GeoDataFrame with the Pine Ridge polygon in EPSG:4326.
    Downloads and caches on first call.
    """
    try:
        import geopandas as gpd
        from shapely.validation import make_valid
    except ImportError:
        raise ImportError("geopandas is required: conda install geopandas")

    cache_path = CACHE_DIR / "pine_ridge_boundary.geojson"

    if cache_path.exists():
        return gpd.read_file(cache_path)

    print("Downloading Census TIGER AIANNH boundaries...")
    url = "https://www2.census.gov/geo/tiger/TIGER2023/AIANNH/tl_2023_us_aiannh.zip"
    import zipfile, io, tempfile

    r = requests.get(url, timeout=300)
    r.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        with tempfile.TemporaryDirectory() as tmp:
            z.extractall(tmp)
            shp = next(Path(tmp).glob("*.shp"))
            all_aiannh = gpd.read_file(shp).to_crs("EPSG:4326")

    pine_ridge = all_aiannh[all_aiannh["NAME"] == "Pine Ridge"].copy()
    pine_ridge = pine_ridge.dissolve(as_index=False)
    pine_ridge["geometry"] = pine_ridge.geometry.apply(make_valid)
    pine_ridge.to_file(cache_path, driver="GeoJSON")

    print(f"Pine Ridge boundary saved to {cache_path.name}")
    return pine_ridge


def load_sd_tribal_boundaries():
    """
    Load boundaries for all 8 South Dakota Tribal Nations from Census TIGER.

    Returns a GeoDataFrame in EPSG:4326 with a 'common_name' column.
    Downloads and caches on first call.
    """
    try:
        import geopandas as gpd
        from shapely.validation import make_valid
    except ImportError:
        raise ImportError("geopandas is required: conda install geopandas")

    cache_path = CACHE_DIR / "sd_tribal_boundaries.geojson"

    SD_CENSUS_NAMES = [
        "Pine Ridge", "Rosebud", "Standing Rock",
        "Cheyenne River", "Lower Brule", "Crow Creek",
        "Lake Traverse", "Flandreau",
    ]
    COMMON_NAMES = {
        "Pine Ridge":     "Oglala Lakota",
        "Rosebud":        "Rosebud Sioux",
        "Standing Rock":  "Standing Rock Sioux",
        "Cheyenne River": "Cheyenne River Sioux",
        "Lower Brule":    "Lower Brule Sioux",
        "Crow Creek":     "Crow Creek Sioux",
        "Lake Traverse":  "Sisseton Wahpeton Oyate",
        "Flandreau":      "Flandreau Santee Sioux",
    }

    if cache_path.exists():
        return gpd.read_file(cache_path)

    print("Downloading Census TIGER AIANNH boundaries...")
    url = "https://www2.census.gov/geo/tiger/TIGER2023/AIANNH/tl_2023_us_aiannh.zip"
    import zipfile, io, tempfile

    r = requests.get(url, timeout=300)
    r.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        with tempfile.TemporaryDirectory() as tmp:
            z.extractall(tmp)
            shp = next(Path(tmp).glob("*.shp"))
            all_aiannh = gpd.read_file(shp).to_crs("EPSG:4326")

    sd = all_aiannh[all_aiannh["NAME"].isin(SD_CENSUS_NAMES)].copy()
    sd = sd.dissolve(by="NAME", as_index=False)
    sd["geometry"]    = sd.geometry.apply(make_valid)
    sd["common_name"] = sd["NAME"].map(COMMON_NAMES)
    sd.to_file(cache_path, driver="GeoJSON")

    print(f"SD Tribal boundaries saved to {cache_path.name}")
    return sd


# ── MODIS NDVI ────────────────────────────────────────────────────────────────

def fetch_ndvi_timeseries(
    lat: float,
    lon: float,
    start_year: int,
    end_year: int,
    site_name: str = "site",
) -> pd.DataFrame:
    """
    Fetch MODIS MOD13Q1 NDVI time series for a single point via ORNL DAAC.

    The ORNL DAAC API limits requests to 10 tiles (~160 days) per call.
    This function fetches one year at a time and concatenates the results.
    Results are cached to data/cache/.

    Parameters
    ----------
    lat, lon   : WGS84 coordinates of the point
    start_year : First year to fetch (MODIS available from 2000)
    end_year   : Last year to fetch
    site_name  : Name used for the cache file

    Returns
    -------
    DataFrame with columns: date, ndvi (scaled 0–1), pixel_count
    """
    cache_file = CACHE_DIR / f"ndvi_{site_name.replace(' ', '_').lower()}_{start_year}_{end_year}.csv"

    if cache_file.exists():
        df = pd.read_csv(cache_file, parse_dates=["date"])
        return df

    print(f"Downloading MODIS NDVI for {site_name} ({start_year}–{end_year})...")
    parts = []

    # MOD13Q1 has ~23 composites per year (365÷16), exceeding the 10-tile API limit.
    # Split each year into 3 chunks of ≤8 composites each:
    #   Chunk 1: days 001–113  (composites on days 1,17,33,49,65,81,97,113  = 8 tiles)
    #   Chunk 2: days 129–241  (composites on days 129,145,...,241          = 8 tiles)
    #   Chunk 3: days 257–353  (composites on days 257,273,...,353          = 7 tiles)
    YEAR_CHUNKS = [("001", "113"), ("129", "241"), ("257", "353")]

    import time as _time
    total_chunks = (end_year - start_year + 1) * len(YEAR_CHUNKS)
    chunk_num    = 0

    for year in range(start_year, end_year + 1):
        year_parts = 0
        for start_doy, end_doy in YEAR_CHUNKS:
            chunk_num += 1
            url = f"{ORNL_BASE}/{MODIS_PRODUCT}/subset"
            params = {
                "latitude":     lat,
                "longitude":    lon,
                "startDate":    f"A{year}{start_doy}",
                "endDate":      f"A{year}{end_doy}",
                "kmAboveBelow": 2,
                "kmLeftRight":  2,
            }
            try:
                r = requests.get(url, params=params,
                                 headers={"Accept": "application/json"},
                                 timeout=30)
                r.raise_for_status()
                data = r.json()

                for subset in data.get("subset", []):
                    if subset.get("band") != MODIS_BAND:
                        continue
                    raw_vals = [
                        v for v in subset.get("data", [])
                        if v is not None and v > NDVI_FILL
                    ]
                    if not raw_vals:
                        continue
                    cal_date = subset.get("calendar_date", "")
                    try:
                        date = pd.to_datetime(cal_date)
                    except Exception:
                        continue
                    parts.append({
                        "date":        date,
                        "ndvi":        round(float(np.mean(raw_vals)) * NDVI_SCALE, 4),
                        "pixel_count": len(raw_vals),
                    })
                    year_parts += 1
            except Exception as e:
                warnings.warn(
                    f"NDVI fetch failed for {year} chunk {start_doy}-{end_doy}: {e}",
                    UserWarning,
                )
                _time.sleep(0.3)
        print(f"  {year}: {year_parts} obs  [{chunk_num}/{total_chunks} chunks]", flush=True)

    if not parts:
        raise RuntimeError(
            f"No MODIS NDVI data retrieved for {site_name}. "
            "Check network access to modis.ornl.gov"
        )

    df = pd.DataFrame(parts).sort_values("date").reset_index(drop=True)
    df.to_csv(cache_file, index=False)
    print(f"  Cached {len(df)} observations → {cache_file.name}")
    return df


# ── gridMET climate data ───────────────────────────────────────────────────────

def fetch_gridmet_point(
    lat: float,
    lon: float,
    variable: str,
    start_year: int,
    end_year: int,
    site_name: str = "site",
) -> pd.DataFrame:
    """
    Fetch gridMET daily climate data for a single point via OPeNDAP.

    Parameters
    ----------
    lat, lon   : WGS84 coordinates
    variable   : gridMET variable name, e.g. 'tmmx' (max temp), 'pr' (precip),
                 'rmax' (max RH), 'vs' (wind speed), 'erc' (energy release component)
    start_year : First year to fetch (gridMET available from 1979)
    end_year   : Last year to fetch
    site_name  : Name used for the cache file

    Returns
    -------
    DataFrame with columns: date, {variable}

    gridMET variable reference
    --------------------------
    tmmx  — Maximum temperature (K)
    tmmn  — Minimum temperature (K)
    pr    — Precipitation (mm)
    rmax  — Maximum relative humidity (%)
    rmin  — Minimum relative humidity (%)
    vs    — Wind speed (m/s)
    erc   — Energy release component (dimensionless)
    bi    — Burning index (dimensionless)
    """
    try:
        import xarray as xr
    except ImportError:
        raise ImportError("xarray is required: conda install xarray")

    cache_file = CACHE_DIR / (
        f"gridmet_{variable}_{site_name.replace(' ', '_').lower()}"
        f"_{start_year}_{end_year}.csv"
    )

    if cache_file.exists():
        return pd.read_csv(cache_file, parse_dates=["date"])

    print(f"Downloading gridMET {variable} for {site_name} ({start_year}–{end_year})...")

    url = f"{GRIDMET_BASE}/{variable}/{variable}_{start_year}.nc"
    # gridMET OPeNDAP URL pattern
    url = (
        f"http://thredds.northwestknowledge.net:8080/thredds/dodsC/"
        f"MET/{variable}/{variable}_{start_year}.nc"
    )

    parts = []
    for year in range(start_year, end_year + 1):
        year_url = (
            f"http://thredds.northwestknowledge.net:8080/thredds/dodsC/"
            f"MET/{variable}/{variable}_{year}.nc"
        )
        try:
            ds = xr.open_dataset(year_url, engine="netcdf4")
            # gridMET uses 0–360 longitude convention
            ds_point = ds.sel(lon=lon % 360, lat=lat, method="nearest")
            var_name  = [v for v in ds_point.data_vars][0]
            series    = ds_point[var_name].to_series().reset_index()
            series    = series.rename(columns={var_name: variable, "day": "date"})
            series["date"] = pd.to_datetime(series["date"])
            parts.append(series[["date", variable]])
            ds.close()
        except Exception as e:
            warnings.warn(f"gridMET {variable} fetch failed for {year}: {e}", UserWarning)

    if not parts:
        raise RuntimeError(
            f"No gridMET {variable} data retrieved for {site_name}."
        )

    df = pd.concat(parts, ignore_index=True).sort_values("date").reset_index(drop=True)
    df.to_csv(cache_file, index=False)
    print(f"  Cached {len(df)} daily observations → {cache_file.name}")
    return df


# ── xarray helpers ────────────────────────────────────────────────────────────

def timeseries_to_dataarray(
    df: pd.DataFrame,
    date_col: str = "date",
    value_col: str = "ndvi",
    name: str | None = None,
    attrs: dict | None = None,
) -> "xr.DataArray":
    """
    Convert a time series DataFrame to a labeled xarray DataArray.

    This is the first step in building a data cube — taking tabular data
    and adding dimensional labels.

    Parameters
    ----------
    df        : DataFrame with date and value columns
    date_col  : Name of the date column
    value_col : Name of the value column
    name      : Name for the DataArray (used in Dataset)
    attrs     : Metadata attributes to attach to the DataArray

    Returns
    -------
    xr.DataArray with 'time' dimension
    """
    try:
        import xarray as xr
    except ImportError:
        raise ImportError("xarray is required: conda install xarray")

    da = xr.DataArray(
        data   = df[value_col].values,
        coords = {"time": df[date_col].values},
        dims   = ["time"],
        name   = name or value_col,
        attrs  = attrs or {},
    )
    return da


def compute_growing_season_mean(
    da: "xr.DataArray",
    months: list[int] | None = None,
) -> "xr.DataArray":
    """
    Compute annual growing season mean for a time series DataArray.

    Parameters
    ----------
    da     : DataArray with a 'time' dimension
    months : List of month integers to include in growing season.
             Default: [5, 6, 7, 8, 9] (May–September, Great Plains growing season)

    Returns
    -------
    DataArray with annual growing season means, indexed by year
    """
    if months is None:
        months = [5, 6, 7, 8, 9]

    gs = da.sel(time=da["time"].dt.month.isin(months))
    annual = gs.groupby("time.year").mean()
    return annual


def compute_anomaly(da: "xr.DataArray") -> "xr.DataArray":
    """
    Compute anomaly (departure from long-term mean) for a DataArray.

    Parameters
    ----------
    da : DataArray (any temporal resolution)

    Returns
    -------
    DataArray of same shape with values as departures from mean
    """
    return da - da.mean()

