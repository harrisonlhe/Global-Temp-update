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
