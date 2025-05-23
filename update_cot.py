
import pandas as pd
import requests
import io
from datetime import datetime

# Define each currency's unique "Market and Exchange Names" used in COT data
# These must match exactly what appears in the CFTC raw files
contracts = {
    "eur": "EURO FX - CHICAGO MERCANTILE EXCHANGE",
    "gbp": "BRITISH POUND STERLING - CHICAGO MERCANTILE EXCHANGE",
    "jpy": "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE",
    "chf": "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE",
    "cad": "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
    "aud": "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
    "nzd": "NEW ZEALAND DOLLAR - CHICAGO MERCANTILE EXCHANGE",
    "mxn": "MEXICAN PESO - CHICAGO MERCANTILE EXCHANGE",
    "usd": "U.S. DOLLAR INDEX - ICE FUTURES U.S."
}

# COT long format URL
cot_url = "https://www.cftc.gov/files/dea/history/fut_fin_txt_2024.zip"  # Use current year (update annually or automate)
output_files = []

# Download and read the zipped long format file
r = requests.get(cot_url)
r.raise_for_status()

# Save and unzip in memory
import zipfile
from io import BytesIO

with zipfile.ZipFile(BytesIO(r.content)) as z:
    for name in z.namelist():
        if name.endswith(".txt"):
            with z.open(name) as f:
                df_raw = pd.read_csv(f)
                break

# Standardize columns
df_raw.columns = [c.strip() for c in df_raw.columns]

# Clean and export each currency
for code, label in contracts.items():
   df = df_raw[df_raw["Market_and_Exchange_Name"] == label].copy()
    df["Report_Date_as_YYYY-MM-DD"] = pd.to_datetime(df["Report_Date_as_YYYY-MM-DD"])

    df_cleaned = pd.DataFrame({
        "Date": df["Report_Date_as_YYYY-MM-DD"],
        "Institutional Net": df["Asset Manager/Institutional Longs"] - df["Asset Manager/Institutional Shorts"],
        "Retail Net": df["Nonreportable Positions Longs"] - df["Nonreportable Positions Shorts"]
    })

    df_cleaned = df_cleaned.sort_values("Date")
    file_path = f"{code}_cot_cleaned_FULL.csv"
    df_cleaned.to_csv(file_path, index=False)
    output_files.append(file_path)

print("Updated files:", output_files)
