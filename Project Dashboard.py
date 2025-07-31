# 🌍 GLOBAL TEMPERATURE STORY DASHBOARD 
import streamlit as st
import pandas as pd
import altair as alt

# ─── Page Config ────────────────────────────────────
st.set_page_config(
    page_title="Global Temperature Change",
    page_icon="🌍",
    layout="wide"
)

# ─── Hero Section ─────────────────────────
st.markdown(
    """
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
        <p>An interactive exploration of global temperature trends.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    """
    <div class='description'>
        Explore how <strong>temperature changes over decades</strong> using interactive visualizations. 
        Hover over charts, filter by countries, or analyze warming gases individually.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ─── Sidebar Navigation ────────────────────────────
st.sidebar.title("Navigation")
st.sidebar.caption("""
🔑 Use keyboard ↑↓ or type to search options. 
Use this menu to switch between sections of the dashboard:
- **Home**: Overview of global temperature trends
- **Explore Trends**: Yearly patterns, variability, and status comparisons
- **Warming Gases**: Contributions by greenhouse gases and sources
- **Placeholder**: This is a placeholder page.
- **Chat Assistant**: Ask questions like "Which country warmed fastest in 1998?"

🌓 **Note**: This dashboard is best viewed in **dark mode** for optimal readability and contrast.
""")
page = st.sidebar.radio(
    "Go to:",
    ["Home", "Explore Trends", "Warming Gases", "Placeholder", "Chat Assistant"],  
    index=0
)

# ─── Data Load and Prep ─────────────────
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

    # Add DevStatus 
    developed_iso3 = ["USA", "CAN", "GBR", "DEU", "FRA", "JPN", "AUS", "NZL", "NOR", "SWE", "CHE"]
    df_long["DevStatus"] = df_long["ISO3"].apply(lambda x: "Developed" if x in developed_iso3 else "Developing")

    return df_long

df_long = load_data()

# ─── Warming Gases Page ───────
@st.cache_data
def prepare_gas_data(df2, dev_year_range, chart_country):
    # Filter the DataFrame based on the selected year range
    df2_filtered = df2[
        (df2["Year"] >= dev_year_range[0]) &
        (df2["Year"] <= dev_year_range[1])
    ].copy()

    # Function to get gas data for a specific entity
    def gas_data(entity):
        name = "World" if entity == "All" else entity
        return df2_filtered[df2_filtered["Entity"] == name].drop(columns=["Code"]).copy()

    # Define a mapping for gases and their sources
    gas_mapping = {
        "nitrous oxide": {
            "fossil fuels": "N2O_FF&I",
            "default": "N2O_AgLU"
        },
        "methane": {
            "fossil fuels": "CH4_FF&I",
            "default": "CH4_AgLU"
        },
        "fossil fuels": "CO2_FF&I",
        "default": "CO2_AgLU"
    }

    # Shorten column names using the mapping
    gas_cols = [c for c in df2_filtered.columns if c.startswith("Change in")]
    shortened_columns = {}

    for col in gas_cols:
        for gas, sources in gas_mapping.items():
            if gas in col:
                if isinstance(sources, dict):
                    for source, new_name in sources.items():
                        if source in col:
                            shortened_columns[col] = new_name
                            break
                else:
                    shortened_columns[col] = sources
                break
        else:
            shortened_columns[col] = "CO2_AgLU"  # Default case

    # Get the gas data and rename columns
    gas_df = gas_data(chart_country).rename(columns=shortened_columns)

    # Melt the DataFrame for visualization
    gas_long = gas_df.melt(
        id_vars="Year",
        value_vars=list(shortened_columns.values()),
        var_name="series",
        value_name="Temp Change"
    )

    # Add a legend mapping for better readability
    label_map = {
        "CO2_FF&I": "CO₂ (Fossil Fuels & Industry)",
        "CO2_AgLU": "CO₂ (Agriculture & Land Use)",
        "CH4_FF&I": "CH₄ (Fossil Fuels & Industry)",
        "CH4_AgLU": "CH₄ (Agriculture & Land Use)",
        "N2O_FF&I": "N₂O (Fossil Fuels & Industry)",
        "N2O_AgLU": "N₂O (Agriculture & Land Use)"
    }
    gas_long["Legend"] = gas_long["series"].map(label_map)

    return gas_long 
    
# ─── Sidebar Filters ───────────────
if page not in ["Home", "Chat Assistant"]:
    st.sidebar.header("🔍 Filters")
    countries = ["All"] + sorted(df_long["Country"].unique())
    years = sorted(df_long["Year"].unique())  # Keep years available if needed

    selected_country = st.sidebar.selectbox("Country", countries)
    selected_year = st.sidebar.selectbox("Year", years)  # Optional: keep if you want to filter by year

    # Filter the DataFrame based on selected country and year
    filtered = df_long.copy()
    
    if selected_country != "All":
        filtered = filtered[filtered["Country"] == selected_country]

# ─── Home Page ───────────────────────────── 
if page == "Home":
    st.write("""
    ### About This Dashboard
    Over the past century, the Earth's surface temperature has experienced significant changes due to various natural and anthropogenic factors. This dashboard explores key global temperature trends, anomalies, and projections to provide insights into the ongoing climate challenges.

    **How Gases Affect Temperature**  
    Greenhouse gases, like carbon dioxide (CO2), methane (CH4), and water vapor, trap heat in the Earth's atmosphere. This natural process, called the greenhouse effect, maintains the Earth's habitable temperature. However, excessive emissions from human activities, including burning fossil fuels and deforestation, amplify this effect, leading to global warming and climate changes.

    Explore the visualizations to understand the impacts of these changes and potential mitigation strategies.
    """)
    
# ─── Explore Trends Page Tabs ─────────────────────────────
if page == "Explore Trends":
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Year-over-Year", "🌡️ Scatter Plot", "🔻 Variability", "🌍 Country Status"])

    # Combined Line and Scatter Plot
    with tab1:
        st.subheader("📈 Historical Year-over-Year Temperature Changes (1961–2004)")
        
        # Interaction Description
        st.write("""
        **Explore the interactive visualization below!** 

        - **Hover** over the data points in both the line and scatter plots to see detailed information about the **Year**, **Temperature Change (°C)**, and **Country**.
        - **Select** specific countries in the scatter plot to highlight their temperature trends. The line chart will update to show the year-over-year changes for the selected country.
        - **Analyze** the relationship between year-over-year changes (line) and overall temperature trends (scatter points) to identify patterns and anomalies.
        - Use **zoom and pan** features to focus on specific time periods for a more detailed examination.
        - To return to viewing all countries, simply **deselect** any highlighted points in the scatter plot.

        Enjoy exploring the temperature trends!
        """)

        if selected_country == "All":
            st.write("Viewing data for a sample of countries. You can select a specific country to see detailed Year-over-Year changes.")
            sample_countries = df_long["Country"].unique()[:10]  # Limit to a sample of 10 countries
            yoy_data = df_long[df_long["Country"].isin(sample_countries)].copy()
            yoy_data["YoY_Change"] = yoy_data["TempChange"].diff()

            # Create the unified line chart for the sample countries
            line = alt.Chart(yoy_data).mark_line(point=True).encode(
                x=alt.X("Year:O"),
                y=alt.Y("YoY_Change:Q", title="Change from Previous Year (°C)"),
                color="Country:N",  # Differentiate lines by country
                tooltip=["Year", "Country", "YoY_Change"]
            ).properties(
                width=800,
                height=450,
                title="Year-over-Year Temperature Change – Sample of Countries"
            )
        else:
            yoy_data = df_long[df_long["Country"] == selected_country].copy()
            yoy_data["YoY_Change"] = yoy_data["TempChange"].diff()

            # Create the line chart for the selected country
            line = alt.Chart(yoy_data).mark_line(point=True).encode(
                x=alt.X("Year:O"),
                y=alt.Y("YoY_Change:Q", title="Change from Previous Year (°C)"),
                color=alt.value("#f45b69"),
                tooltip=["Year", "YoY_Change"]
            ).properties(
                width=800,
                height=450,
                title=f"Year-over-Year Temperature Change – {selected_country}"
            )

        # Create the scatter plot
        alt.data_transformers.disable_max_rows()
        sel_country = alt.selection_point(fields=["Country"], empty="all")

        if selected_country == "All":
            scatter_data = df_long[df_long["Country"].isin(sample_countries)]
        else:
            scatter_data = df_long[df_long["Country"] == selected_country]

        scatter = alt.Chart(scatter_data).mark_circle(size=60).encode(
            x=alt.X("Year:O", title="Year"),
            y=alt.Y("TempChange:Q", title="Temperature Change (°C)"),
            color=alt.Color("TempChange:Q", scale=alt.Scale(scheme="plasma", domainMid=0)),
            opacity=alt.condition(sel_country, alt.value(1), alt.value(0.15)),
            tooltip=["Country", "Year", "TempChange"]
        ).add

    # 🔻 Variability Analysis
    with tab3:
        st.subheader("🔻 Countries with Decreasing Temperature Variability")
        st.info(
            """
            This chart compares the **standard deviation of temperature change** before and after 1993.
            A **negative delta** indicates more stable climate conditions.
            """
        )

        early = df_long[df_long["Year"] <= 1992].groupby("Country")["TempChange"].std().reset_index(name="Std_Early")
        late = df_long[df_long["Year"] >= 1993].groupby("Country")["TempChange"].std().reset_index(name="Std_Late")
        std_comp = early.merge(late, on="Country")
        std_comp["Delta_Std"] = std_comp["Std_Late"] - std_comp["Std_Early"]
        decreasing = std_comp[std_comp["Delta_Std"] < 0].sort_values("Delta_Std")

        bar = alt.Chart(decreasing).mark_bar().encode(
            x=alt.X("Delta_Std:Q", title="∆ Std Dev (1993–2024 − 1961–1992)"),
            y=alt.Y("Country:N", sort="-x"),
            color=alt.Color("Delta_Std:Q", scale=alt.Scale(scheme="viridis", domainMid=0)),
            tooltip=["Country", "Std_Early", "Std_Late", "Delta_Std"]
        ).properties(
            height=500,
            width=750,
            title="Top Countries with Decreasing Yearly Temperature Variability"
        )

        st.altair_chart(bar, use_container_width=True)

    # 🌍 Developed vs Developing Comparison
    with tab4:
        st.subheader("🌍 Developed vs Developing: Temperature Comparison")
        
        st.write(
            """
            Developed countries, often referred to as "high-income" nations, typically have advanced technological infrastructure,
            high standards of living, and robust economies. Examples include the United States, Germany, and Japan.

            Developing countries face challenges like limited access to education, healthcare, and infrastructure.
            Examples include India, Nigeria, and Bangladesh.
            """
        )
        dev_sel = alt.selection_multi(fields=["DevStatus"], bind="legend")

        dev_avg = df_long.groupby(["Year", "DevStatus"])["TempChange"].mean().reset_index()

        line_chart = alt.Chart(dev_avg).mark_line(point=True).encode(
            x=alt.X("Year:O"),
            y=alt.Y("TempChange:Q", title="Avg Temp Change (°C)"),
            color=alt.Color("DevStatus:N", scale=alt.Scale(domain=["Developed", "Developing"], range=["#2ca02c", "#ff7f0e"])),
            opacity=alt.condition(dev_sel, alt.value(1.0), alt.value(0.15)),
            tooltip=["Year", "DevStatus", "TempChange"]
        ).add_params(dev_sel).properties(
            title="Average Temp Change by Economic Status",
            width=750,
            height=400
        )

        st.altair_chart(line_chart, use_container_width=True)

        df_long["YearGroup"] = (df_long["Year"] // 5) * 5
        dev_bar = df_long.groupby(["YearGroup", "DevStatus"])["TempChange"].mean().reset_index()

        bar_chart = alt.Chart(dev_bar).mark_bar().encode(
            x=alt.X("YearGroup:O", title="5-Year Group"),
            y=alt.Y("TempChange:Q", title="Avg Temp Change (°C)"),
            color=alt.Color("DevStatus:N", scale=alt.Scale(domain=["Developed", "Developing"], range=["#2ca02c", "#ff7f0e"])),
            opacity=alt.condition(dev_sel, alt.value(1.0), alt.value(0.25)),
            tooltip=["YearGroup", "DevStatus", "TempChange"]
        ).add_params(dev_sel).properties(
            title="5-Year Avg Temp Change by Development Status",
            width=750,
            height=400
        )

        st.altair_chart(bar_chart, use_container_width=True)

# ─── Warming Gases Page ─────────────────────────────────────
if page == "Warming Gases":
    st.subheader("🔥 Warming Contributions by Gas and Source")
    st.info("""
    This area chart shows **the warming impact of major greenhouse gases and emission sources over time**.
    Click the legend to highlight or filter different contributors.
    """)

    # Set a default year range and country
    dev_year_range = (1961, 2004)  # You can add a sidebar slider later if needed
    chart_country = selected_country if 'selected_country' in locals() else "All"

    # Load gas data
    gas_long = prepare_gas_data(df_long, dev_year_range, chart_country)

    # Interactive selection logic
    selection = alt.selection_point(fields=['series'])
    condition = alt.condition(selection, 'series:N', alt.ColorValue('lightgray'))

    # Area chart showing contribution by gas
    area = alt.Chart(gas_long).mark_area(opacity=0.7).encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Temp Change:Q", title="Temperature Change (°C)"),
        color=condition,
        order="series:N",
        tooltip=['Year:O', 'Legend:N', 'Temp Change:Q']
    ).add_params(selection).properties(
        width=900,
        height=500,
        title="Warming Contributions by Gas Type and Emission Source"
    )

    # Explanation and chart rendering
    st.markdown("""
    #### How do different gases and sources contribute to global warming?
    This area chart visualizes how different greenhouse gases contribute to global warming over time.
    
    - The leading gases are carbon dioxide (CO₂), methane (CH₄), and nitrous oxide (N₂O).
    - The main sources are fossil fuels and industry (FF&I), and agriculture and land use (AgLU).
    - You can interact with the chart legend to isolate specific gases or sources.
    """)

    st.markdown("""
    - The most prevalent contributor to global warming is **carbon dioxide** from **fossil fuels and industry**.  
    - Solutions include transitioning to renewable energy, electrification of transportation, and adopting energy-efficient technologies.
    """)

    st.altair_chart(area, use_container_width=True)

# ─── Roydan to add Content ───────────────────────────────────
if page == "Placeholder":
    st.title("Placeholder Page")
    st.write("This is a placeholder page. You can add content here later.")

# ─── Chat Assistant Page ────────────────────────────────
if page == "Chat Assistant":
    st.subheader("🧠 ClimateBot Assistant")
    st.markdown("""
    Ask **ClimateBot** about:
    - 📈 Temperature trends over time
    - 🌡️ Country-level comparisons
    - 🔻 Variability and climate stability

    For example:
    - “Which country had the highest temp change in 1998?”
    - “What does decreased variability mean?”
    - “Compare developing vs developed warming patterns”
    """)

    # Set up chat interface
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hi, I'm ClimateBot! Ask me about global temperatures 🌍"}
        ]

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask your question here...")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Hard-coded Q&A for demonstration
        response = ""
        q = prompt.lower()

        if "highest temp" in q and "country" in q:
            response = "The country with the highest recorded temperature change in 1998 was likely a high-latitude nation like Russia or Canada, but exact values depend on the dataset."
        elif "variability" in q:
            response = (
                "Variability refers to how much temperatures fluctuate year to year. "
                "Less variability means more climate stability, which can affect ecosystems and planning."
            )
        elif "developed" in q and "developing" in q:
            response = (
                "Developed countries often show earlier increases due to industrialization. "
                "Developing countries are now experiencing steeper rises due to economic growth and emissions."
            )
        else:
            response = "Great question! Try asking about a specific year, country, or trend type. I'm still learning! 🤖"

        st.chat_message("assistant").markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# ─── Footer ────────────────────────────────────────────────
st.markdown("---")
st.write(
    """
    <div style="text-align: center; font-size: 15px;" role="contentinfo" aria-label="Footer information">
        🌐 Created by <strong>Harrison, Paula, and Roydan</strong> • Advocates for climate transparency and data science  
        <br/>
        Built with ❤️ using <a href="https://streamlit.io" target="_blank">Streamlit</a> and <a href="https://altair-viz.github.io" target="_blank">Altair</a>
    </div>
    """,
    unsafe_allow_html=True
)
