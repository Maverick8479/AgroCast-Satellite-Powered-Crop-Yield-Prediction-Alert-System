# AgroCast-Satellite-Powered-Crop-Yield-Prediction-Alert-System
**AgroCast** is an end-to-end AI solution that forecasts crop yields at a district level using satellite vegetation data (NDVI), historical crop production, and climate data. It also flags potential low-yield zones by triggering early alerts based on statistical thresholds. Insights are presented through an interactive Power BI dashboard for actionable decision-making.

---
## 🧰 Tech Stack

| Layer              | Tools Used                                  |
|-------------------|----------------------------------------------|
| **Data Sources**   | Google Earth Engine (NDVI), Crop Yield Datasets |
| **Geo Processing** | Rasterio, Geopandas, Shapefiles              |
| **Modeling**       | Python, XGBoost, Scikit-learn                |        |
| **Visualization**  | Power BI (cards, maps, slicers, line charts) |

---

## 📦 Folder Structure

```
AgroCast/
├── data/
│   ├── raw/                # Raw shapefiles, CSVs, NDVI rasters
│   ├── processed/          # Cleaned CSVs with yield, NDVI, alerts
├── models/                # Saved ML models (optional)
├── scripts/               # Python scripts for data prep & modeling
├── outputs/               # Final alert reports & plots
├── dashboard/             # Power BI .pbix file
```

---

## 🔄 Workflow

### 1. NDVI Extraction
- Download NDVI GeoTIFF using Google Earth Engine
- Use `rasterio` + `geopandas` to mask NDVI by district shapes
- Save average NDVI per district to CSV

### 2. Merge Datasets
- Combine NDVI, crop yield, temperature, and production into one dataset
- Compute `Yield = Production / Area` if not present

### 3. Model Training
- Train an `XGBoostRegressor` to predict yield
- Evaluate using RMSE and R² Score

### 4. Alert Generation
- Trigger alert if `Yield_Predicted < mean - 0.5 * std_dev`
- Add `Alert` column to output CSV

### 5. Visualization
- Load final dataset into Power BI
- Add:
  - KPI cards (Avg Yield, NDVI, Alerts)
  - Line chart (Yield over Years)
  - Filled map (District Alert Zones)
  - Data table with slicers (Crop, Year, District, Alert)

