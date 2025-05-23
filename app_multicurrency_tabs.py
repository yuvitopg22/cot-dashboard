
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

# Define tabs
tabs = st.tabs("USD Index", "Euro FX", "British Pound", "Japanese Yen", "Swiss Franc", "Canadian Dollar", "Australian Dollar", "New Zealand Dollar", "Mexican Peso")


with tabs[0]:
    df = load_data("usd_cot_cleaned.csv")
    draw_chart(df, "USD Index")

with tabs[1]:
    df = load_data("euro_fx_cot_cleaned.csv")
    draw_chart(df, "Euro FX")

with tabs[2]:
    df = load_data("british_pound_sterling_cot_cleaned.csv")
    draw_chart(df, "British Pound")

with tabs[3]:
    df = load_data("japanese_yen_cot_cleaned.csv")
    draw_chart(df, "Japanese Yen")

with tabs[4]:
    df = load_data("swiss_franc_cot_cleaned.csv")
    draw_chart(df, "Swiss Franc")

with tabs[5]:
    df = load_data("canadian_dollar_cot_cleaned.csv")
    draw_chart(df, "Canadian Dollar")

with tabs[6]:
    df = load_data("australian_dollar_cot_cleaned.csv")
    draw_chart(df, "Australian Dollar")

with tabs[7]:
    df = load_data("new_zealand_dollar_cot_cleaned.csv")
    draw_chart(df, "New Zealand Dollar")

with tabs[8]:
    df = load_data("mexican_peso_cot_cleaned.csv")
    draw_chart(df, "Mexican Peso")
