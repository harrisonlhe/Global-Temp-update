# ───────────────────────────────────────────────────────────
#  🌍  GLOBAL TEMPERATURE STORY DASHBOARD  (Streamlit + Altair)
# ───────────────────────────────────────────────────────────
import pandas as pd
import altair as alt
import streamlit as st

# ─── Page Setup ─────────────────────────────────────────────────────
st.set_page_config(page_title="Temperature Dashboard", page_icon="🌍", layout="wide")
st.title("🌍 Temperature Change Visualizations 🌡️")

# ─── Scatter Plot: Temperature Change Over Time ─────────────────────
st.subheader("Scatter Plot: Temperature Change Over Time")
st.write("""
This scatter plot visualizes **temperature changes by year** for selected countries. 
Points are color-coded by the degree of temperature change (blue represents cooling, red represents warming), 
and opacity represents the highlighted selection.

**Interactive Features**:
- Hover over points to see specific country, year, and temperature changes.
- Click a country (if filtered) to isolate its specific annual trends.
""")

# Sample Data Filtering
if chart_country == "All":
    sample_countries = filtered_chart["Country"].unique()[:10]
    scatter_src = filtered_chart[filtered_chart["Country"].isin(sample_countries)]
else:
    scatter_src = filtered_chart

# Scatter Chart Creation
sel_country = alt.selection_point(fields=["Country"], bind="legend")

scatter = (
    alt.Chart(scatter_src)
    .mark_circle(size=60)
    .encode(
        x=alt.X("Year:O", axis=alt.Axis(labelAngle=0), title="Year"),
        y=alt.Y("TempChange:Q", title="Temperature Change (°C)"),
        color=alt.Color(
            "TempChange:Q",
            scale=alt.Scale(scheme="redblue", reverse=True, domainMid=0),
            legend=alt.Legend(title="Temp Change (°C)"),
        ),
        opacity=alt.condition(sel_country, alt.value(1), alt.value(0.15)),
        tooltip=["Country", "Year", "TempChange"]
    )
    .add_params(sel_country)
    .properties(
        width=750,
        height=400,
        title=f"Temperature Change Over Time – {chart_country if chart_country != 'All' else 'All Countries'}",
    )
)

# Render scatter plot
st.altair_chart(scatter, use_container_width=True)

# ─── Monthly Temperature Change Line Chart ──────────────────────────
st.subheader("Monthly Temperature Trends")
st.write("""
This line chart captures **monthly average temperature changes** over time.
The color gradient represents the **Yearly Average Temperature Change**, making it easier to identify warming or cooling trends.

**Interactive Features**:
- Hover over a specific month to view precise temperature change values.
- Click on a year in the legend to filter monthly trends for that year only.
""")

# Monthly Data Filtering
if chart_country == "All":
    df_monthly_filtered = filtered_chart_monthly[filtered_chart_monthly["Entity"] == "World"]
    name = "All"
else:
    df_monthly_filtered = filtered_chart_monthly[filtered_chart_monthly["Entity"] == chart_country]
    name = chart_country

# Calculate Yearly Averages
yearly_averages = (
    df_monthly_filtered.groupby(["Year", "Entity"])["Monthly Average Temperature Change (°C)"]
    .agg("mean")
    .reset_index()
    .rename(columns={"Monthly Average Temperature Change (°C)": "Yearly Average Temperature Change (°C)"})
)

# Merge Monthly Data with Yearly Averages
df_monthly_filtered = pd.merge(df_monthly_filtered, yearly_averages, on=["Year", "Entity"], how="left")

# Selection for Line Chart
sel_year = alt.selection_point(fields=["Year"], empty=True)

# Line Chart Creation
monthly_line = (
    alt.Chart(df_monthly_filtered)
    .mark_line()
    .encode(
        x=alt.X(
            "Month_named:N",
            sort=[
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"
            ],
            title="Month"
        ),
        y=alt.Y("Monthly Average Temperature Change (°C):Q", title="Monthly Avg Temp Change (°C)"),
        color=alt.Color(
            "Yearly Average Temperature Change (°C):Q",
            scale=alt.Scale(scheme="reds"),
            legend=alt.Legend(title="Yearly Avg Temp Change (°C)")
        ),
        opacity=alt.condition(sel_year, alt.value(1), alt.value(0.20)),
        tooltip=["Year", "Monthly Average Temperature Change (°C)", "Entity"]
    )
    .properties(
        width=750,
        height=400,
        title=f"Monthly Average Temperature Change – {name}",
    )
    .interactive()
    .add_params(sel_year)
)

# Render monthly line chart
st.altair_chart(monthly_line, use_container_width=True)
