# Test cases — Retail EDA & Data Quality

Tests verify CSV loading, expected columns, dashboard metrics, missing-value audit, duplicates after preprocessing, numeric inputs, region aggregations, known dirty-data examples, Python syntax, and dependencies.

From the project root run:

```powershell
python -m ensurepip --upgrade
python -m pip install -r requirements-dev.txt
python -m pytest -v tests/
```

The app intentionally explores raw data; tests for invalid age, discount, and region values confirm that anomalies are present, not that the dashboard cleans them.

The duplicate count of 64 refers to the dashboard's transformed DataFrame. A direct `pd.read_csv(...).duplicated()` count can differ (61) because formatting conversions may make additional records identical.

A full Streamlit browser smoke test is separate: `python -m streamlit run app.py` and inspect the dashboard manually.
