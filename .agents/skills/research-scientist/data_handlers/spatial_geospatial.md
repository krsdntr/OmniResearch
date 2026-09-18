# Data Handler 2: Spatial & Geospatial Data

Format Scope: Raster (`.tif`, `.tiff`, `.nc` NetCDF, `.h5` HDF5, `.grib`), Vector (`.shp`, `.geojson`, `.gpkg`, `.kml`).

---

## 1. Coordinate Reference System (CRS) Hygiene
- **Rule**: Never combine or distance-measure geospatial layers without verifying CRS alignment.
  - Geographic CRS: WGS84 (`EPSG:4326`) for latitude/longitude coordinates.
  - Projected CRS: UTM zones or regional equal-area projections (e.g. Albers Equal Area) when computing surface areas, buffers, or distances in meters.

---

## 2. Spatial Autocorrelation & Econometrics
- Tobler's First Law: Nearby things are more related than distant things.
- **Diagnostic**: Global and Local Moran's $I$ for spatial clustering.
- **Spatial Models**:
  - Spatial Autoregressive (SAR) / Spatial Lag Model: $Y = \rho W Y + X\beta + \epsilon$.
  - Spatial Error Model (SEM): $Y = X\beta + u, \quad u = \lambda W u + \epsilon$.
- Tools: Python (`geopandas`, `pysal`, `esda`, `spreg`, `rasterio`, `xarray`), R (`sf`, `terra`, `spatialreg`).
