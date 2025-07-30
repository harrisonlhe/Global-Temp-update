# 🌍 GLOBAL TEMPERATURE STORY DASHBOARD 
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Global Temperature Dashboard", page_icon="🌍", layout="wide")

# ─── Load Data ───────────────────────────────────────────
@st.cache_data

def load_data():
    df = pd.read_csv("Indicator_3_1_Climate_Indicators_Annual_Mean_Global_Surface_Temperature_577579683071085080.csv")
    year_cols = [c for c in df.columns if c.isdigit()]
    df_long = df.melt(
        id_vars=["Country", "ISO2", "ISO3", "Indicator", "Unit"],
        value_vars=year_cols,
        var_name="Year",
        value_name="TempChange"
    )
    df_long["Year"] = df_long["Year"].astype(int)
    df_long.sort_values(["Country", "Year"], inplace=True)
    return df_long

df_long = load_data()

# Add Economic Status
dev_map = {
    "United States": "Developed", "Germany": "Developed", "Japan": "Developed",
    "India": "Developing", "Nigeria": "Developing", "Bangladesh": "Developing"
    # Add more country mappings as needed
}
df_long["DevStatus"] = df_long["Country"].map(dev_map)
df_long["DevStatus"].fillna("Other", inplace=True)

# ─── Hero Section ─────────────────────────────────────────
st.markdown("""
<style>
    .hero {
        background-image: url('https://github.com/PReece11/Global-Temp/blob/main/ChatGPT%20Image%20Jul%2030,%202025,%2011_22_32%20AM.png?raw=true');
        background-size: cover;
        padding: 100px 0;
        margin-bottom: 20px;
        color: white;
        text-align: center;
    }
    .description {
        text-align: center;
        line-height: 1.6;
        font-size: 18px;
    }
</style>
<div class="hero" role="region" aria-label="Header with Earth image and dashboard title">
    <h1>🌍 Global Temperature Change 🌡️</h1>
    <p>An interactive exploration of monthly and yearly global temperature trends.</p>
</div>
""", unsafe_allow_html=True)

st.write("""
<div class='description'>
Explore how <strong>temperature changes over decades</strong> using interactive visualizations.
Hover over charts, filter by countries, or analyze seasonal patterns individually.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── Tabs ────────────────────────────────────────────────
tab_yoy, tab_scatter, tab_bar, tab_dev = st.tabs([
    "📈 Year-over-Year Trends", "📊 Global Scatter Plot", "🔻 Temperature Variability", "🌐 Economic Status"
])

# ─── TAB 1: Year-over-Year Trend ─────────────────────────
with tab_yoy:
    st.subheader("📈 Year-over-Year Change and Country Trend")

    countries = sorted(df_long["Country"].unique())
    selected_country = st.selectbox("Select a Country", countries)
    country_data = df_long[df_long["Country"] == selected_country].copy()
    country_data["YoY_Change"] = country_data["TempChange"].diff()

    line = alt.Chart(country_data).mark_line(point=True).encode(
        x=alt.X("Year:O"),
        y=alt.Y("YoY_Change:Q", title="Year-over-Year Temp Change (°C)"),
        color=alt.value("#f45b69"),
        tooltip=["Year", "YoY_Change"]
    ).properties(width=750, height=300, title=f"YoY Change – {selected_country}")

    scatter = alt.Chart(country_data).mark_circle(size=60).encode(
        x=alt.X("Year:O"),
        y=alt.Y("TempChange:Q", title="Temperature Change (°C)"),
        color=alt.Color("TempChange:Q", scale=alt.Scale(scheme="plasma"), legend=None),
        tooltip=["Year", "TempChange"]
    ).properties(width=750, height=300, title=f"Annual Temp Change – {selected_country}")

    st.altair_chart(alt.vconcat(line, scatter), use_container_width=True)

# ─── TAB 2: Scatter Plot ─────────────────────────────────
with tab_scatter:
    st.subheader("🌡️ Global Temperature Changes by Year")
    sel_country = alt.selection_point(fields=["Country"], empty="all")
    sample_countries = df_long["Country"].unique()[:10]
    scatter_data = df_long[df_long["Country"].isin(sample_countries)]

    scatter = alt.Chart(scatter_data).mark_circle(size=60).encode(
        x=alt.X("Year:O"),
        y=alt.Y("TempChange:Q"),
        color=alt.Color("TempChange:Q", scale=alt.Scale(scheme="plasma")),
        opacity=alt.condition(sel_country, alt.value(1), alt.value(0.15)),
        tooltip=["Country", "Year", "TempChange"]
    ).add_params(sel_country).properties(width=800, height=500)

    st.altair_chart(scatter, use_container_width=True)

# ─── TAB 3: Decreasing Temperature Variability ───────────
with tab_bar:
    st.subheader("🔻 Countries with Decreasing Temperature Variability")

    early = df_long[df_long["Year"] <= 1992].groupby("Country")["TempChange"].std().reset_index(name="Std_Early")
    late = df_long[df_long["Year"] >= 1993].groupby("Country")["TempChange"].std().reset_index(name="Std_Late")
    std_comp = early.merge(late, on="Country")
    std_comp["Delta_Std"] = std_comp["Std_Late"] - std_comp["Std_Early"]
    decreasing = std_comp[std_comp["Delta_Std"] < 0].sort_values("Delta_Std")

    bar = alt.Chart(decreasing).mark_bar().encode(
        x=alt.X("Delta_Std:Q", title="Δ Std Dev (1993–2024 − 1961–1992)"),
        y=alt.Y("Country:N", sort="-x"),
        color=alt.Color("Delta_Std:Q", scale=alt.Scale(scheme="viridis")),
        tooltip=["Country", "Std_Early", "Std_Late", "Delta_Std"]
    ).properties(width=800, height=500)

    st.altair_chart(bar, use_container_width=True)

# ─── TAB 4: Economic Status ──────────────────────────────
with tab_dev:
    st.subheader("🌐 Developed vs Developing Countries")
    st.markdown("""
    Developed countries, often referred to as "high-income" nations, typically have advanced technological infrastructure,
    high standards of living, and strong economies. Examples include the United States, Germany, and Japan.

    In contrast, developing countries, or "low to middle-income" nations, often face challenges such as lower economic growth,
    limited access to education and healthcare, and higher levels of poverty. Examples include India, Nigeria, and Bangladesh.
    """)

    filtered_dev = df_long[df_long["DevStatus"].isin(["Developed", "Developing"])].copy()
    dev_avg = filtered_dev.groupby(["Year", "DevStatus"])["TempChange"].mean().reset_index()
    dev_sel = alt.selection_multi(fields=["DevStatus"], bind="legend")

    line_chart = alt.Chart(dev_avg).mark_line(point=True).encode(
        x=alt.X("Year:O"),
        y=alt.Y("TempChange:Q", title="Avg Temp Change (°C)"),
        color=alt.Color("DevStatus:N", scale=alt.Scale(domain=["Developed", "Developing"], range=["#2ca02c", "#ff7f0e"])),
        opacity=alt.condition(dev_sel, alt.value(1.0), alt.value(0.15)),
        tooltip=["Year", "DevStatus", "TempChange"]
    ).add_params(dev_sel).properties(width=750, height=400, title="Annual Avg Temp Change")

    st.altair_chart(line_chart, use_container_width=True)

    filtered_dev["YearGroup"] = (filtered_dev["Year"] // 5) * 5
    dev_bar = filtered_dev.groupby(["YearGroup", "DevStatus"])["TempChange"].mean().reset_index()

    bar_chart = alt.Chart(dev_bar).mark_bar().encode(
        x=alt.X("YearGroup:O", title="5-Year Group"),
        y=alt.Y("TempChange:Q"),
        color=alt.Color("DevStatus:N", scale=alt.Scale(domain=["Developed", "Developing"], range=["#2ca02c", "#ff7f0e"])),
        opacity=alt.condition(dev_sel, alt.value(1.0), alt.value(0.25)),
        tooltip=["YearGroup", "DevStatus", "TempChange"]
    ).add_params(dev_sel).properties(width=750, height=400, title="5-Year Avg Temp Change by Development Status")

    st.altair_chart(bar_chart, use_container_width=True)

# ─── Footer ───────────────────────────────────────────────
st.markdown("---")
st.write("""
<div style="text-align: center;" role="contentinfo">
    Brought to you by <strong>Harrison, Paula, and Roydan </strong>.
    Advocates for climate change.
</div>
""", unsafe_allow_html=True)
