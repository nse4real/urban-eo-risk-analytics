from __future__ import annotations

import streamlit as st

from projects.urban_growth_risk.src.dummy_data import make_dummy_risk_table


st.set_page_config(page_title="Urban Growth Risk", layout="wide")

st.title("Urban Growth Risk Index")
st.caption("Scaffold view using dummy data. EO-derived features will replace placeholders.")

st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to",
    options=[
        "Overview",
        "Priority Table",
        "Spatial Evidence",
        "Drivers & Components",
        "Validation & Confidence",
        "Limitations",
    ],
)

city = st.sidebar.selectbox("City", ["London", "Lagos"])
st.sidebar.markdown("---")
st.sidebar.info("Tiers are relative within the selected city and time window.")

df = make_dummy_risk_table(seed=42 if city == "London" else 7, n=15)

if page == "Overview":
    st.subheader("What this tool is for")
    st.write(
        """
        This project prioritises administrative areas where recent urban growth patterns may be creating
        planning, infrastructure, or service-delivery pressure. Outputs are designed for triage, not enforcement.
        """
    )
    st.subheader("How to read the results")
    st.write(
        """
        Start with the Priority Table to see ranked areas, then inspect drivers and evidence.
        Confidence flags are placeholders until validation is wired in.
        """
    )

elif page == "Priority Table":
    st.subheader(f"Priority Table: {city}")
    st.write("Ranked administrative units with component breakdown and relative risk tiering.")
    st.dataframe(
        df[
            [
                "admin_unit",
                "risk_tier",
                "composite_score",
                "expansion_rate",
                "abruptness",
                "exposure",
                "infra_constraint",
                "confidence_flag",
                "top_drivers",
            ]
        ],
        use_container_width=True,
    )

elif page == "Spatial Evidence":
    st.subheader("Spatial Evidence")
    st.write("Placeholder. This page will show admin-unit choropleths and change evidence maps.")

elif page == "Drivers & Components":
    st.subheader("Drivers & Components")
    st.write("Placeholder. This page will explain what pushed scores up or down per unit.")

elif page == "Validation & Confidence":
    st.subheader("Validation & Confidence")
    st.write("Placeholder. This page will show sampling design, confusion matrices, and confidence notes.")

elif page == "Limitations":
    st.subheader("Limitations")
    st.write(
        """
        - This is a decision-support index, not a legal determination of informality.
        - Tiers are relative within a city and time window.
        - Proxies and EO-derived signals carry uncertainty that must be interpreted with local context.
        """
    )