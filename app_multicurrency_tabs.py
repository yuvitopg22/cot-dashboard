
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

# Define currency data
currencies = [
    ("USD Index", "usd_cot_cleaned.csv"),
    ("Euro FX", "euro_fx_cot_cleaned.csv"),
    ("British Pound", "british_pound_sterling_cot_cleaned.csv"),
    ("Japanese Yen", "japanese_yen_cot_cleaned.csv"),
    ("Swiss Franc", "swiss_franc_cot_cleaned.csv"),
    ("Canadian Dollar", "canadian_dollar_cot_cleaned.csv"),
    ("Australian Dollar", "australian_dollar_cot_cleaned.csv"),
    ("New Zealand Dollar", "new_zealand_dollar_cot_cleaned.csv"),
    ("Mexican Peso", "mexican_peso_cot_cleaned.csv")
]

tabs = st.tabs([name for name, _ in currencies])

for i, (name, file) in enumerate(currencies):
    with tabs[i]:
        df = load_data(file)
        draw_chart(df, name)
