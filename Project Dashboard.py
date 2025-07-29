# ───────────────────────────────────────────────────────────
#  🌍  GLOBAL TEMPERATURE STORY DASHBOARD  (Streamlit + Altair)
# ───────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import altair as alt

# ─── Page set‑up ────────────────────────────────────────────
st.set_page_config(page_title="Global Temperature Dashboard",
                   page_icon="🌍",
                   layout="wide")

st.title(":earth_africa: Global Temperature Story  :thermometer:")

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/3/33/Global_temperature_anomalies_-_1880-present.gif",
    caption="Global Temperature Anomalies Since 1880 (Credit: NASA)",
    use_column_width=True
)

st.write("""
### About This Dashboard
This dashboard explores key global temperature trends, anomalies, and projections to provide insights into climate change.

**How Gases Affect Temperature**
Greenhouse gases like CO2, CH4, and water vapor trap heat in the atmosphere. Human activity has intensified this effect, leading to global warming. Use the interactive tools to explore how these changes vary by country, year, and development status.
""")

# ─── Cached Data Load ───────────────────────────────────────
@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

df = load_csv("Indicator_3_1_Climate_Indicators_Annual_Mean_Global_Surface_Temperature_577579683071085080.csv")
df2 = load_csv("global-warming-by-gas-and-source.csv")
df_monthly = load_csv("df_monthly_long.csv")
df_contribution = load_csv("contributions-global-temp-change.csv")

# ─── Reshape and Prepare Data ───────────────────────────────
year_cols = [c for c in df.columns if c.isdigit()]
df_long = df.melt(
    id_vars=["Country", "ISO2", "ISO3", "Indicator", "Unit"],
    value_vars=year_cols,
    var_name="Year",
    value_name="TempChange"
)
df_long["Year"] = df_long["Year"].astype(int)

# Map development status
developed_iso3 = ["USA", "CAN", "GBR", "DEU", "FRA", "JPN",
                  "AUS", "NZL", "NOR", "SWE", "CHE"]
df_long["DevStatus"] = df_long["ISO3"].apply(
    lambda x: "Developed" if x in developed_iso3 else "Developing"
)

# Monthly formatting
df_monthly['Date'] = pd.to_datetime(df_monthly[['Year', 'Month']].assign(DAY=1))
df_monthly.rename(columns={'Mean_Temp':'Monthly Average Temperature Change (\u00b0C)'}, inplace=True)

# ─── Filters and Sidebar ────────────────────────────────────
data_long_list = list(df_long["Country"].unique())
data_contribution_list = list(df_contribution['Entity'].unique())
df_monthly_list = list(df_monthly["Entity"].unique())
df2_list = list(df2['Entity'].unique())

in_all = [x for x in data_long_list if x in data_contribution_list and x in df_monthly_list and x in df2_list]

all_countries = ["All"] + sorted(in_all)
year_min, year_max = int(df_long["Year"].min()), int(df_long["Year"].max())

with st.sidebar.expander("📊 Charts Filters", expanded=True):
    chart_country = st.selectbox("Country", all_countries, key="chart_country")

with st.sidebar.expander("🌐 Select Time Period", expanded=False):
    dev_year_range = st.slider("Year Range",
                               min_value=year_min,
                               max_value=year_max,
                               value=(year_min, year_max),
                               step=1,
                               key="dev_year_range")

# ─── Tabs ───────────────────────────────────────────────────
tabs = st.tabs(["\ud83d\udcca Charts", "\ud83c\udf10 Developed vs Developing", "\ud83d\udccb Data"])

# Placeholders for future code...
with tabs[0]:
    st.subheader("Coming soon: Country Trends and Global Gas Contributions")

with tabs[1]:
    st.subheader("Coming soon: Developed vs Developing Comparisons")

with tabs[2]:
    st.subheader("Raw Data Preview")
    st.dataframe(df_long.head(100))
    st.download_button(
        "Download Filtered Data",
        data=df_long.to_csv(index=False).encode('utf-8'),
        file_name="filtered_temperature_data.csv",
        mime="text/csv"
    )
