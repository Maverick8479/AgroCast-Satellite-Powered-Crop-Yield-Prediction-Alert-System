import rasterio
import matplotlib.pyplot as plt

with rasterio.open("data/raw/NDVI.tif") as src:
    ndvi = src.read(1)
    plt.imshow(ndvi, cmap='RdYlGn')
    plt.colorbar(label="NDVI")
    plt.title("NDVI Raster")
    plt.show()