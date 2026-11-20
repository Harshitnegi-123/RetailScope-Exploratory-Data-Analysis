import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
st.set_page_config(page_title="Retail EDA & Data Quality",layout="wide")
st.title("Retail EDA & Data Quality")
st.caption("Harshit Negi | Roll: 2026m01410006 | Data Analyst Mini Project 1")
@st.cache_data
def load():
    df=pd.read_csv(Path(__file__).parent / "retail_customer_sales_dataset.csv")
    for col in ["Sales","Profit","Discount","Age","Income","Quantity"]:
        df[col]=pd.to_numeric(df[col],errors="coerce")
    df["Region"]=df["Region"].astype("string").str.strip().str.title()
    df["Order_Date"]=pd.to_datetime(df["Order_Date"],errors="coerce",format="mixed")
    return df
df=load()
st.subheader("Data quality and exploratory profiling")
a,b,c=st.columns(3)
a.metric("Raw records",len(df));b.metric("Duplicate rows",int(df.duplicated().sum()));c.metric("Missing cells",int(df.isna().sum().sum()))
st.markdown("#### Missing-value audit")
audit=pd.DataFrame({"Missing":df.isna().sum(),"Missing %":(df.isna().mean()*100).round(2)})
st.dataframe(audit, use_container_width=True)
st.markdown("#### Numerical distributions")
metric=st.selectbox("Variable",["Sales","Profit","Age","Income","Discount"])
fig,ax=plt.subplots(figsize=(9,4));ax.hist(df[metric].dropna(),bins=35);ax.set(xlabel=metric,ylabel="Transactions",title=f"Distribution of {metric}");st.pyplot(fig)
st.markdown("#### Descriptive statistics")
st.dataframe(df[["Sales","Profit","Age","Income","Discount","Quantity"]].describe(),use_container_width=True)
st.markdown("#### Business segmentation")
st.dataframe(df.groupby("Region",dropna=False).agg(Transactions=("Sales","size"),Revenue=("Sales","sum"),Profit=("Profit","sum")).round(2),use_container_width=True)
st.info("Exploration uses raw data. See the submitted EDA notebook for cleaning decisions, feature engineering and the full audit.")
