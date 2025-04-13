import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np
import pandas as pd
import os
from shapely.geometry import box

# Paths
raster_path = "data/raw/NDVI.tif"
shapefile_path = "data/raw/districts.geojson"  # or .shp if you use shapefile
output_path = "data/processed/ndvi_by_district.csv"

# Load district boundaries
gdf = gpd.read_file(shapefile_path)

# Open NDVI raster
with rasterio.open(raster_path) as src:
    print("NDVI CRS:", src.crs)
    print("GeoJSON CRS:", gdf.crs)

    # Align CRS
    if gdf.crs != src.crs:
        gdf = gdf.to_crs(src.crs)

    # Filter only overlapping districts
    ndvi_bounds = box(*src.bounds)
    gdf = gdf[gdf.intersects(ndvi_bounds)]
    print(f"Processing {len(gdf)} districts overlapping with NDVI raster.")

    ndvi_stats = []

    for idx, row in gdf.iterrows():
        geometry = [row['geometry']]
        district_name = row['DISTRICT'] if 'DISTRICT' in row else f'District_{idx}'

        try:
            out_image, _ = mask(src, geometry, crop=True)
            out_image = out_image.astype('float32')

            # Flatten and filter valid NDVI range
            ndvi_values = out_image.flatten()
            ndvi_values = ndvi_values[(ndvi_values >= -1.0) & (ndvi_values <= 1.0)]

            if ndvi_values.size > 0:
                mean_ndvi = round(float(np.mean(ndvi_values)), 4)
                print(f"{district_name}: Mean NDVI = {mean_ndvi}")
                ndvi_stats.append({'district': district_name, 'mean_ndvi': mean_ndvi})
            else:
                print(f"{district_name}: No valid NDVI pixels")
        except Exception as e:
            print(f"Error for {district_name}: {e}")

# Save the results
os.makedirs(os.path.dirname(output_path), exist_ok=True)
ndvi_df = pd.DataFrame(ndvi_stats)
ndvi_df.to_csv(output_path, index=False)
print(f"\n✅ Saved NDVI extraction to {output_path}")
