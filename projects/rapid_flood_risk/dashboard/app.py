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
        "Method Comparison",
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

elif page == "Method Comparison":
    st.subheader("Method Comparison: Rapid vs Refined")
    st.write(
        """
        This compares two approaches under operational constraints:
        - **Rapid**: transparent weighted overlay (primary for 48–72 hour use)
        - **Refined**: ML-style comparator (secondary, to test consistency)
        The goal is not to claim ML is “better”. The goal is to identify where methods disagree.
        """
    )

    df_cmp = df.copy()

    # Ranking by each method
    df_cmp["rank_overlay"] = df_cmp["susceptibility_score"].rank(ascending=False, method="min").astype(int)
    df_cmp["rank_ml"] = df_cmp["ml_score"].rank(ascending=False, method="min").astype(int)

    df_cmp["rank_delta"] = (df_cmp["rank_overlay"] - df_cmp["rank_ml"]).abs()

    st.markdown("### Agreement check")
    top_k = st.slider("Top-K zones to compare", 3, min(10, len(df_cmp)), 5, 1)

    top_overlay = set(df_cmp.nsmallest(top_k, "rank_overlay")["zone"])
    top_ml = set(df_cmp.nsmallest(top_k, "rank_ml")["zone"])

    overlap = len(top_overlay.intersection(top_ml))
    st.write(
        {
            "top_k": top_k,
            "overlap_count": overlap,
            "overlap_fraction": round(overlap / top_k, 2),
        }
    )

    st.markdown("### Where methods disagree most")
    st.dataframe(
        df_cmp.sort_values("rank_delta", ascending=False)[
            ["zone", "susceptibility_score", "ml_score", "rank_overlay", "rank_ml", "rank_delta", "top_drivers", "confidence_flag"]
        ].head(10),
        use_container_width=True,
    )

    st.markdown("### Operational guidance")
    st.write(
        """
        **Use weighted overlay first when:**
        - You need a defendable answer fast
        - Stakeholders require interpretable drivers
        - Data is incomplete or noisy
        
        **Lean on the ML comparator when:**
        - You have time for feature QA and validation
        - You need to test whether overlay rankings are robust
        - You can explain model behaviour and uncertainty
        
        **Red flag zones:** high disagreement + high exposure.
        Those should be prioritised for manual review or additional evidence checks.
        """
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