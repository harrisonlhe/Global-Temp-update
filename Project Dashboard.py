# 🌍 GLOBAL TEMPERATURE STORY DASHBOARD — NASA Style + YoY + Overview
import streamlit as st
import pandas as pd
import altair as alt

# ─── Page Config ────────────────────────────────────────────
st.set_page_config(
    page_title="Temperature Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ─── Hero Section ───────────────────────────────────────────
st.markdown(
    """
    <style>
        .hero {
            background-image: url('https://www.nasa.gov/sites/default/files/thumbnails/image/earth.jpg'); 
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
        <h1>🌍 Temperature Dashboard 🌡️</h1>
        <p>An interactive exploration of monthly and yearly global temperature trends.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    """
    <div class='description'>
        Explore how <strong>temperature changes over decades</strong> using interactive visualizations. 
        Hover over charts, filter by countries, or analyze seasonal patterns individually.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ─── Sidebar Navigation ─────────────────────────────────────
st.sidebar.title("Navigation")
st.sidebar.caption("🔑 Use keyboard ↑↓ or type to search options.")
page = st.sidebar.radio(
    "Go to:",
    ["Home", "Scatter Plot (Global Trends)", "Year-over-Year Trend", "Monthly Analysis"],
    index=0
)

# ─── Data Load and Prep ─────────────────────────────────────
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

# ─── Sidebar Filters ────────────────────────────────────────
if page != "Home":
    st.sidebar.header("🔍 Filters")
    countries = ["All"] + sorted(df_long["Country"].unique())
    years     = ["All"] + sorted(df_long["Year"].unique())

    selected_country = st.sidebar.selectbox("Country", countries)
    selected_year    = st.sidebar.selectbox("Year", years)

    filtered = df_long.copy()
    if selected_country != "All":
        filtered = filtered[filtered["Country"] == selected_country]
    if selected_year != "All":
        filtered = filtered[filtered["Year"] == selected_year]

# ─── Home Page ──────────────────────────────────────────────
if page == "Home":
    st.write("""
    ### About This Dashboard
    Over the past century, the Earth's surface temperature has experienced significant changes due to various natural and anthropogenic factors. This dashboard explores key global temperature trends, anomalies, and projections to provide insights into the ongoing climate challenges.

    **How Gases Affect Temperature**  
    Greenhouse gases, like carbon dioxide (CO2), methane (CH4), and water vapor, trap heat in the Earth's atmosphere. This natural process, called the greenhouse effect, maintains the Earth's habitable temperature. However, excessive emissions from human activities, including burning fossil fuels and deforestation, amplify this effect, leading to global warming and climate changes.

    Explore the visualizations to understand the impacts of these changes and potential mitigation strategies.
    """)

# ─── Scatter Plot Page ──────────────────────────────────────
elif page == "Scatter Plot (Global Trends)":
    st.markdown("### 🌡️ Temperature Changes by Year (Scatter Plot)")
    st.info("""
    This scatter plot shows temperature deviations from baseline values for selected countries over time.
    - **Purple = cooler**, **yellow = warmer** (colorblind-friendly).
    - Click a country to highlight trends; hover to view details.
    """)

    alt.data_transformers.disable_max_rows()
    sel_country = alt.selection_point(fields=["Country"], empty="all")

    if selected_country == "All":
        sample_countries = df_long["Country"].unique()[:10]
        scatter_data = df_long[df_long["Country"].isin(sample_countries)]
    else:
        scatter_data = filtered

    scatter = (
        alt.Chart(scatter_data)
        .mark_circle(size=60)
        .encode(
            x=alt.X("Year:O"),
            y=alt.Y("TempChange:Q", title="Temperature Change (°C)"),
            color=alt.Color("TempChange:Q", scale=alt.Scale(scheme="plasma", domainMid=0)),
            opacity=alt.condition(sel_country, alt.value(1), alt.value(0.15)),
            tooltip=[
                alt.Tooltip("Country:N", title="Country"),
                alt.Tooltip("Year:O", title="Year"),
                alt.Tooltip("TempChange:Q", title="Temperature Change (°C)")
            ]
        )
        .transform_filter(sel_country)
        .properties(
            height=400,
            width=750,
            title=f"Temperature Change Over Time – {selected_country if selected_country != 'All' else 'Sample of Countries'}"
        )
    )

    st.altair_chart(scatter, use_container_width=True)

    st.markdown("### 🔻 Countries with Decreasing Temperature Variability")
    st.info("""
    This bar chart compares the **standard deviation of temperature change** before and after 1993.
    A **negative delta** means a country has become more stable in its yearly climate variation.
    """)

    early = (
        df_long[df_long["Year"] <= 1992]
        .groupby("Country")["TempChange"].std()
        .reset_index(name="Std_Early")
    )
    late = (
        df_long[df_long["Year"] >= 1993]
        .groupby("Country")["TempChange"].std()
        .reset_index(name="Std_Late")
    )
    std_comp = early.merge(late, on="Country")
    std_comp["Delta_Std"] = std_comp["Std_Late"] - std_comp["Std_Early"]
    decreasing = std_comp[std_comp["Delta_Std"] < 0].sort_values("Delta_Std")

    bar = (
        alt.Chart(decreasing)
        .mark_bar()
        .encode(
            x=alt.X("Delta_Std:Q", title="Δ Std Dev (1993–2024 − 1961–1992)"),
            y=alt.Y("Country:N", sort="-x"),
            color=alt.Color("Delta_Std:Q", scale=alt.Scale(scheme="plasma", domainMid=0)),
            tooltip=[
                alt.Tooltip("Country:N", title="Country"),
                alt.Tooltip("Std_Early:Q", title="Std Dev (1961–1992)"),
                alt.Tooltip("Std_Late:Q", title="Std Dev (1993–2024)"),
                alt.Tooltip("Delta_Std:Q", title="Δ Std Dev")
            ]
        )
        .add_params(sel_country)
        .properties(
            height=500,
            width=750,
            title="Countries with Decreasing Temperature Variability"
        )
    )

    st.altair_chart(bar, use_container_width=True)

# ─── Year-over-Year Trend Page ─────────────────────────────
elif page == "Year-over-Year Trend":
    st.subheader("📈 Year-over-Year Change in Temperature")
    st.info("""
    This line chart shows how much **temperature change fluctuates year-over-year** for a selected country.
    - Helps detect acceleration or deceleration in warming.
    """)

    if selected_country == "All":
        st.warning("Please select a specific country to view Year-over-Year changes.")
    else:
        yoy_data = df_long[df_long["Country"] == selected_country].copy()
        yoy_data["YoY_Change"] = yoy_data["TempChange"].diff()

        line = alt.Chart(yoy_data).mark_line(point=True).encode(
            x=alt.X("Year:O"),
            y=alt.Y("YoY_Change:Q", title="Change from Previous Year (°C)"),
            color=alt.value("#f45b69"),
            tooltip=[
                alt.Tooltip("Year:O", title="Year"),
                alt.Tooltip("YoY_Change:Q", title="Year-over-Year Change (°C)", format=".3f")
            ]
        ).properties(
            width=800,
            height=450,
            title=f"Year-over-Year Temperature Change – {selected_country}"
        )

        st.altair_chart(line, use_container_width=True)

# ─── Monthly Analysis Page ─────────────────────────────────
elif page == "Monthly Analysis":
    st.subheader("📅 Monthly Average Temperature Change")
    st.info("""
    This placeholder line chart illustrates how monthly averages may look.
    Use it to explore **seasonal climate patterns** over the years.
    (Real monthly data can be substituted here.)
    """)

    df_monthly = pd.DataFrame({
        'Month_named': ['January', 'February', 'March'],
        'Monthly Average Temperature Change (°C)': [0.2, 0.3, 0.4],
        'Year': [2001, 2002, 2003],
    })

    monthly_line = alt.Chart(df_monthly).mark_line().encode(
        x=alt.X("Month_named:N", title="Month"),
        y=alt.Y("Monthly Average Temperature Change (°C):Q", title="Temperature Change (°C)"),
        color=alt.Color("Year:N", scale=alt.Scale(scheme="viridis"), legend=alt.Legend(title="Year")),
        tooltip=[
            alt.Tooltip("Year:O", title="Year"),
            alt.Tooltip("Monthly Average Temperature Change (°C):Q", title="Avg Temp Change (°C)")
        ]
    ).properties(
        width=800,
        height=500,
        title="Seasonal Average Temperature Change"
    )

    st.altair_chart(monthly_line, use_container_width=True)

# ─── Footer ────────────────────────────────────────────────
st.markdown("---")
st.write(
    """
    <div style="text-align: center;" role="contentinfo" aria-label="Footer">
        Brought to you by <strong>NASA-inspired Data Exploration Team</strong>. 
        <a href="https://www.nasa.gov/" target="_blank">Visit NASA</a> for official climate data.
    </div>
    """,
    unsafe_allow_html=True
)
