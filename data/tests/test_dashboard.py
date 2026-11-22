"""Tests for the published Retail EDA Streamlit dashboard and its source CSV.
Run from project root: python -m pytest -v tests/
"""
from pathlib import Path
import ast
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "retail_customer_sales_dataset.csv"
APP = ROOT / "app.py"

@pytest.fixture(scope="module")
def raw():
    return pd.read_csv(CSV)

@pytest.fixture(scope="module")
def prepared(raw):
    df = raw.copy()
    for col in ["Sales", "Profit", "Discount", "Age", "Income", "Quantity"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Region"] = df["Region"].astype("string").str.strip().str.title()
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce", format="mixed")
    return df

def test_csv_exists_and_has_rows(raw):
    assert CSV.is_file()
    assert len(raw) > 0

def test_required_dashboard_columns(raw):
    required = {"Sales", "Profit", "Discount", "Age", "Income", "Quantity", "Region", "Order_Date"}
    assert required.issubset(raw.columns)

def test_dashboard_row_count(prepared):
    assert len(prepared) == 7084

def test_dashboard_missing_cell_metric(prepared):
    assert int(prepared.isna().sum().sum()) == 1179

def test_duplicate_count_matches_pandas_logic(prepared):
    assert int(prepared.duplicated().sum()) == 64

def test_missing_audit_percentages(prepared):
    pct = prepared.isna().mean().mul(100)
    assert pct.between(0, 100).all()
    assert int(prepared["Age"].isna().sum()) == 142

def test_numeric_distribution_inputs(prepared):
    for col in ["Sales", "Profit", "Age", "Income", "Discount"]:
        assert pd.api.types.is_numeric_dtype(prepared[col])
        assert prepared[col].notna().any()

def test_region_group_totals(prepared):
    grouped = prepared.groupby("Region", dropna=False).agg(
        Transactions=("Sales", "size"), Revenue=("Sales", "sum"), Profit=("Profit", "sum")
    )
    assert int(grouped.Transactions.sum()) == len(prepared)
    assert grouped.Revenue.sum() == pytest.approx(prepared.Sales.sum())
    assert grouped.Profit.sum() == pytest.approx(prepared.Profit.sum())

def test_known_raw_data_quality_issues(prepared):
    assert (prepared["Age"] < 0).any()
    assert (prepared["Age"] > 110).any()
    assert ((prepared["Discount"] < 0) | (prepared["Discount"] > 1)).any()
    assert {"Nort", "Sth"}.issubset(set(prepared["Region"].dropna()))

def test_app_is_valid_python_and_has_expected_sections():
    source = APP.read_text(encoding="utf-8")
    ast.parse(source)
    for label in ["Data quality and exploratory profiling", "Missing-value audit", "Numerical distributions", "Descriptive statistics", "Business segmentation"]:
        assert label in source

def test_dashboard_dependency_file():
    deps = (ROOT / "requirements.txt").read_text(encoding="utf-8").lower()
    for dep in ["streamlit", "pandas", "numpy", "matplotlib"]:
        assert dep in deps
