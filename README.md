# DataVisionX

DataVisionX is a Streamlit web app for quick, interactive data analytics. Upload a CSV or Excel file and explore it through a modern dark-themed interface, with no code required.

## Features

- **Upload & Overview** – load a CSV/Excel file and get instant row/column counts, missing-value checks and summary statistics.
- **Visual Explorer** – build interactive Plotly charts (including 3D scatter/line, animated histograms and area charts) by picking your own axes and colour groups.
- **Time Series** – choose a date and value column, resample by frequency, and view rolling averages with interactive Altair charts.
- **Smart Insights** – automatic findings on missing values, outliers, correlations, duplicates and high-cardinality columns, with downloadable results.
- **Report & Export** – preview the cleaned dataset and download it as CSV.

## Tech stack

Python, Streamlit, pandas, NumPy, Plotly, Altair, Seaborn, Matplotlib.

## How to run

1. Install Python 3.10 or newer.
2. (Recommended) create and activate a virtual environment:

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS / Linux:
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install streamlit pandas numpy plotly altair seaborn matplotlib openpyxl xlrd
   ```

4. Start the app from the project folder:

   ```bash
   streamlit run Home.py
   ```

5. Open the link Streamlit prints (usually http://localhost:8501) and start from the **Upload & Overview** page.

## Project structure

```
Home.py        # landing page / entry point
theme.py       # shared theme and styling
pages/         # Upload_and_Overview, Visual_Explorer, Time_Series,
               # Smart_Insights, Report_and_Export
```

## Contact

Questions or feedback? Reach out via the contact form on the app's Home page.
