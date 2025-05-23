
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="COT Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("usd_cot_cleaned.csv", parse_dates=["Date"])

df = load_data()

st.title("📈 COT Net Positioning: Institutional vs Retail (USD Index)")

# Date range selector
min_date, max_date = df["Date"].min(), df["Date"].max()
start_date, end_date = st.slider(
    "Select date range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

# Filter data
mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
filtered_df = df.loc[mask]

# Create line chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Institutional Net"],
                         mode="lines", name="Institutional Net", line=dict(color="blue")))
fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Retail Net"],
                         mode="lines", name="Retail Net", line=dict(color="orange")))

fig.update_layout(title="Net Positioning Over Time",
                  xaxis_title="Date", yaxis_title="Net Contracts",
                  legend_title="Participant Type", height=600)

st.plotly_chart(fig, use_container_width=True)

st.caption("Data Source: CFTC | Built with Streamlit & Plotly")
