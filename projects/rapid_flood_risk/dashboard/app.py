from __future__ import annotations

import streamlit as st

from projects.rapid_flood_risk.src.dummy_data import make_dummy_flood_priority_table


st.set_page_config(page_title="Rapid Flood Risk", layout="wide")

st.title("Rapid Flood Susceptibility & Impact Mapping")
st.caption("Scaffold view using dummy data. EO + climate features will replace placeholders.")

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

basin = st.sidebar.selectbox("Basin", ["Thames Catchment"])
st.sidebar.markdown("---")
st.sidebar.info("Outputs are designed for 48–72 hour operational use. Tiers are relative within the basin run.")

df = make_dummy_flood_priority_table(seed=24, n=12)

if page == "Overview":
    st.subheader("What this tool is for")
    st.write(
        """
        This project demonstrates how to produce defensible flood susceptibility and impact insights
        within a 48–72 hour operational window using open EO and climate-grade inputs.
        """
    )
    st.subheader("How to use it")
    st.write(
        """
        Start with the Priority Table to identify likely high-susceptibility zones, then inspect drivers and evidence.
        Confidence flags are placeholders until SAR validation is wired in.
        """
    )

elif page == "Priority Table":
    st.subheader(f"Priority Table: {basin}")
    st.dataframe(
        df[
            [
                "zone",
                "risk_tier",
                "susceptibility_score",
                "terrain",
                "rainfall",
                "wetness",
                "s1_flood_signal",
                "exposure",
                "confidence_flag",
                "top_drivers",
            ]
        ],
        use_container_width=True,
    )

elif page == "Spatial Evidence":
    st.subheader("Spatial Evidence")
    st.write("Placeholder. This page will show susceptibility tiers, flood extent, and impact overlays.")

elif page == "Drivers & Components":
    st.subheader("Drivers & Components")
    st.write("Placeholder. This page will explain what pushed zones into high tier.")

elif page == "Validation & Confidence":
    st.subheader("Validation & Confidence")
    st.write("Placeholder. This page will show checks against historical flood footprints and confidence qualifiers.")

elif page == "Limitations":
    st.subheader("Limitations")
    st.write(
        """
        - This workflow does not replace hydrodynamic modelling.
        - Outputs prioritise speed and interpretability within 48–72 hours.
        - Confidence depends heavily on SAR availability and quality.
        """
    )