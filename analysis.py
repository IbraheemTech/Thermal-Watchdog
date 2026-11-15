"""
Bahawalpur Climate Trend Analysis
Data: NASA MERRA-2 2m air temperature (monthly, 2002-2026)
Region: 71.3E, 29.1N, 72E, 29.7N
"""

import pandas as pd
from scipy.stats import linregress
from pathlib import Path

MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Column name in Giovanni export
TIME_COL = 'time'
TEMP_COL = 'mean_M2TMNXSLV_5_12_4_T2M'
CSV_NAME = 'giovani_bahawalpur_temp.csv'


def load_and_prepare(csv_path="data.csv"):
    """
    Load Giovanni CSV, clean it, convert Kelvin to Celsius,
    and add year/month columns.
    """
    if csv_path is None:
        csv_path = Path(__file__).parent / CSV_NAME
    else:
        csv_path = Path(csv_path)

    # Giovanni exports have 8 header rows before the data
    df = pd.read_csv(csv_path, skiprows=8)
    df.columns = df.columns.str.strip()

    # Parse datetime and numeric temperature
    df['datetime'] = pd.to_datetime(df[TIME_COL], errors='coerce')
    df[TEMP_COL] = pd.to_numeric(df[TEMP_COL], errors='coerce')
    df = df.dropna(subset=['datetime', TEMP_COL]).copy()

    # Extract year and month
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month

    # Kelvin -> Celsius (mean ~300K, so always subtract)
    df['temp_c'] = df[TEMP_COL] - 273.15

    # Elapsed years (for regression on full series)
    df = df.sort_values('datetime').copy()
    df['years_elapsed'] = (
        df['datetime'] - df['datetime'].min()
    ).dt.total_seconds() / (365.2425 * 24 * 60 * 60)

    return df


def compute_overall_trend(df):
    """Linear regression on the full monthly series (all months mixed)."""
    res = linregress(df['years_elapsed'], df['temp_c'])
    return {
        'slope_per_year': res.slope,
        'slope_per_decade': res.slope * 10,
        'p_value': res.pvalue,
        'r_squared': res.rvalue ** 2,
        'significant': bool(res.pvalue < 0.05),
        'direction': 'Increasing' if res.slope > 0 else ('Decreasing' if res.slope < 0 else 'No change')
    }


def compute_monthly_trends(df):
    """
    For each calendar month, regress temperature against year.
    Returns a DataFrame with slope (°C/decade), p-value, significance.
    """
    results = []
    for m in range(1, 13):
        sub = df[df['month'] == m]
        if len(sub) < 3:
            continue
        res = linregress(sub['year'], sub['temp_c'])
        results.append({
            'Month': MONTH_NAMES[m - 1],
            'Month_Num': m,
            'Rate_per_decade': round(res.slope * 10, 3),
            'p_value': round(res.pvalue, 4),
            'Significant': bool(res.pvalue < 0.05),
            'R_squared': round(res.rvalue ** 2, 4),
            'N_years': len(sub)
        })
    return pd.DataFrame(results)


def compute_annual_means(df):
    """Annual average temperature (complete years only, exclude 2026)."""
    annual = (
        df[df['year'] < 2026]
        .groupby('year')['temp_c']
        .mean()
        .reset_index()
    )
    return annual


def project_temperature(df, month_num, target_year):
    """
    Simple linear extrapolation for a given month.
    Returns projected temperature (°C) and baseline (first year mean).
    """
    sub = df[df['month'] == month_num]
    res = linregress(sub['year'], sub['temp_c'])
    baseline_year = int(sub['year'].min())
    baseline_temp = sub[sub['year'] == baseline_year]['temp_c'].mean()
    projected = res.intercept + res.slope * target_year
    return {
        'target_year': target_year,
        'projected_temp': round(projected, 2),
        'baseline_year': baseline_year,
        'baseline_temp': round(baseline_temp, 2),
        'change_from_baseline': round(projected - baseline_temp, 2)
    }


if __name__ == "__main__":
    # Quick self-test when running: python climate_analysis.py
    df = load_and_prepare()
    print("Columns:", df.columns.tolist())
    print("Rows:", len(df))
    print("\nOverall trend:", compute_overall_trend(df))
    print("\nMonthly trends:")
    print(compute_monthly_trends(df).to_string(index=False))