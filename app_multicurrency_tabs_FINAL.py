
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="COT Dashboard", layout="wide")
st.title("📈 Multi-Currency COT Net Positioning Dashboard")

def load_data(file):
    return pd.read_csv(file, parse_dates=["Date"])

def draw_chart(df, title):
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    start_date, end_date = st.slider(
        f"Select date range for {title}",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )

    mask = (df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))
    filtered_df = df.loc[mask]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Institutional Net"],
                             mode="lines", name="Institutional Net", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=filtered_df["Date"], y=filtered_df["Retail Net"],
                             mode="lines", name="Retail Net", line=dict(color="orange")))

    fig.update_layout(title=title,
                      xaxis_title="Date", yaxis_title="Net Contracts",
                      legend_title="Participant Type", height=500)

    st.plotly_chart(fig, use_container_width=True)

# Final and complete currency files (mapped to the actual uploaded cleaned full versions)
currencies = [
    ("USD Index", "usd_cot_cleaned.csv"),
    ("Euro FX", "eur_cot_cleaned_FULL.csv"),
    ("British Pound", "gbp_cot_cleaned_FULL.csv"),
    ("Japanese Yen", "jpy_cot_cleaned_FULL.csv"),
    ("Swiss Franc", "chf_cot_cleaned_FULL.csv"),
    ("Canadian Dollar", "cad_cot_cleaned_FULL.csv"),
    ("Australian Dollar", "australian_dollar_cot_cleaned_v2.csv"),
    ("New Zealand Dollar", "nzd_cot_cleaned_FULL.csv"),
    ("Mexican Peso", "mxn_cot_cleaned_FULL.csv")
]

tabs = st.tabs([name for name, _ in currencies])

for i, (name, file) in enumerate(currencies):
    with tabs[i]:
        df = load_data(file)
        draw_chart(df, name)
