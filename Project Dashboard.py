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

st.title("🌍 Global Temperature Story  🌡️")

# Display the local image from GitHub
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.image(
    "https://raw.githubusercontent.com/PReece11/Global-Temp/main/pexels-arthousestudio-4310289.jpg",
    caption="Image from Pexels (Credit: Arthousestudio)",
    width=600
)
st.markdown("</div>", unsafe_allow_html=True)

# Display the global temperature animation
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/3/33/Global_temperature_anomalies_-_1880-present.gif",
    caption="Global Temperature Anomalies Since 1880 (Credit: NASA)",
    use_container_width=True
)

st.write("""
### About This Dashboard
Over the past century, the Earth's surface temperature has experienced significant changes due to various natural and anthropogenic factors. This dashboard explores key global temperature trends, anomalies, and projections to provide insights into the ongoing climate challenges.

**How Gases Affect Temperature**
Greenhouse gases, like carbon dioxide (CO2), methane (CH4), and water vapor, trap heat in the Earth's atmosphere. This natural process, called the greenhouse effect, maintains the Earth's habitable temperature. However, excessive emissions from human activities, including burning fossil fuels and deforestation, amplify this effect, leading to global warming and climate changes.

Explore the visualizations to understand the impacts of these changes and potential mitigation strategies.
""")

# ─── 📊 CHARTS TAB — SCATTER VISUALIZATION ─────────────────
with tab_charts:
    st.subheader("Temperature Change Forecast (Simulation)")
    st.markdown("""
    This scatterplot represents **simulated temperature change outcomes** for selected countries across different years.
    
    Just like election models forecast a range of results, this visualization shows how likely warming trends distribute under historical and scenario-based simulations.

    **Legend:**
    - 🔴 Higher than 1.5°C change = Significant warming (Red)
    - 🔵 Below 0.5°C = Milder warming (Blue)
    - ⚪ All others = Moderate range (Gray)

    This approach increases **interpretability**, aligns with **ADA guidelines**, and ensures screen reader users understand the trend categories.
    """)

    # Sample 100 countries if large
    sample_df = filtered_chart.copy()
    sample_grouped = (
        sample_df.groupby("Country")["TempChange"]
        .mean()
        .reset_index()
        .rename(columns={"TempChange": "Avg_Change"})
    )
    if len(sample_grouped) > 100:
        sample_grouped = sample_grouped.sample(100, random_state=42)

    scatter = (
        alt.Chart(sample_grouped)
        .mark_circle(size=100)
        .encode(
            x=alt.X("Avg_Change:Q", title="Average Simulated Temp Change (°C)", scale=alt.Scale(zero=False)),
            y=alt.Y("Country:N", sort="-x", title=None),
            color=alt.condition(
                "datum.Avg_Change > 1.5", alt.value("#d62728"),  # red
                alt.condition("datum.Avg_Change < 0.5", alt.value("#1f77b4"), alt.value("#999999"))
            ),
            tooltip=["Country:N", "Avg_Change:Q"]
        )
        .properties(
            width=800,
            height=600,
            title="Distribution of Simulated Country-Level Temperature Change"
        )
    )
    st.altair_chart(scatter, use_container_width=True)
