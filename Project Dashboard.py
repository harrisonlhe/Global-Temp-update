import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(page_title="Climate Dashboard", page_icon="🌍", layout="wide")

# ─── Hero Section ───────────────────────────────────────────────
st.markdown("""
    <div style='
        background-image: url("https://raw.githubusercontent.com/PReece11/Global-Temp/main/pexels-arthousestudio-4310289.jpg");
        background-size: cover;
        padding: 80px 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
    '>
        <h1 style='font-size: 3em; font-weight: bold;'>🌍 Global Climate Dashboard</h1>
        <p style='font-size: 1.2em;'>Tracking Temperature Trends, GHG Impacts, and Global Forecasts</p>
    </div>
""", unsafe_allow_html=True)

# ─── Stats Bar ─────────────────────────────────────────────────
st.markdown("""
<div style='display: flex; justify-content: space-around; padding: 20px 0; font-size: 1.1em; font-weight: bold;'>
    <div style='color: #ff5733;'>🔥 Global Temp ↑ <br><span style='font-size:1.5em;'>+1.1°C</span></div>
    <div style='color: #33b5e5;'>🌊 Sea Level Rise <br><span style='font-size:1.5em;'>+100 mm</span></div>
    <div style='color: #2ecc71;'>🌿 CO₂ (ppm) <br><span style='font-size:1.5em;'>419.3</span></div>
</div>
""", unsafe_allow_html=True)

# ─── Education Panel ──────────────────────────────────────────
st.markdown("""
<div style="background-color: #f9f9f9; padding: 30px; border-radius: 10px;">
<h3>🔬 What is the Greenhouse Effect?</h3>
<p>
The greenhouse effect occurs when gases in Earth's atmosphere trap heat. This process makes Earth much warmer than it would be without an atmosphere. It's one of the things that makes Earth a comfortable place to live.
</p>
<ul>
    <li><strong>Natural GHGs:</strong> Water vapor, CO₂, CH₄</li>
    <li><strong>Human Activity:</strong> Fossil fuels and deforestation intensify this effect</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ─── Chart Description ────────────────────────────────────────
st.markdown("## 📈 Simulation of Temperature Outcomes")
st.markdown("This chart shows a range of possible outcomes modeled on recent data. It does **not** predict a single value, but rather simulates many plausible futures.")

# ─── Simulated Chart (placeholder) ────────────────────────────
df_example = pd.DataFrame({
    "Country": [f"Country {i}" for i in range(1, 101)],
    "Avg_Change": np.random.normal(loc=1.2, scale=0.5, size=100)
})

scatter = (
    alt.Chart(df_example)
    .mark_circle(size=100)
    .encode(
        x=alt.X("Avg_Change:Q", title="Simulated Avg Temp Change (°C)", scale=alt.Scale(zero=False)),
        y=alt.Y("Country:N", sort='-x', title=None),
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

# ─── Footer ─────────────────────────────────────────────────
st.markdown("""
---
<small>Data source: Simulated | Design inspired by <a href='https://science.nasa.gov/climate-change/' target='_blank'>NASA Climate Change</a>.</small>
""", unsafe_allow_html=True)
