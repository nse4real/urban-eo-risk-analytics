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
        "Index Sensitivity",
        "Spatial Evidence",
        "Drivers & Components",
        "Validation & Confidence",
        "Limitations",
    ],
)

city = st.sidebar.selectbox("City", ["London", "Lagos"])
st.sidebar.markdown("---")
st.sidebar.info("Tiers are relative within the selected city and time window.")

df = make_dummy_risk_table(city=city, seed=42 if city == "London" else 7)

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
    st.caption("Baseline weights: expansion 0.35, abruptness 0.25, exposure 0.20, infra 0.20")
    st.dataframe(
        df[
            [
                "admin_id",
                "admin_name",
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
elif page == "Index Sensitivity":
    st.subheader("Index Sensitivity")
    st.write(
        """
        This page tests how robust the priority ranking is to reasonable changes in component weights.
        It does not “optimise” weights. It makes assumptions explicit.
        """
    )

    st.markdown("### Adjust weights (must sum to 1.0)")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        w_expansion = st.slider("Expansion rate", 0.0, 1.0, 0.35, 0.05)
    with c2:
        w_abrupt = st.slider("Abruptness", 0.0, 1.0, 0.25, 0.05)
    with c3:
        w_exposure = st.slider("Exposure", 0.0, 1.0, 0.20, 0.05)
    with c4:
        w_infra = st.slider("Infrastructure constraint", 0.0, 1.0, 0.20, 0.05)

    total = w_expansion + w_abrupt + w_exposure + w_infra
    st.caption(f"Current sum: {total:.2f}")

    if total == 0:
        st.error("All weights are zero. Increase at least one weight.")
    else:
        # Normalise weights to sum to 1.0
        w_expansion_n = w_expansion / total
        w_abrupt_n = w_abrupt / total
        w_exposure_n = w_exposure / total
        w_infra_n = w_infra / total

        st.markdown("### Normalised weights used")
        st.write(
            {
                "expansion_rate": round(w_expansion_n, 3),
                "abruptness": round(w_abrupt_n, 3),
                "exposure": round(w_exposure_n, 3),
                "infra_constraint": round(w_infra_n, 3),
            }
        )

        # Recompute score and show rank changes
        df_sens = df.copy()
        df_sens["sensitivity_score"] = (
            df_sens["expansion_rate"] * w_expansion_n
            + df_sens["abruptness"] * w_abrupt_n
            + df_sens["exposure"] * w_exposure_n
            + df_sens["infra_constraint"] * w_infra_n
        )
        df_sens = df_sens.sort_values("sensitivity_score", ascending=False).reset_index(drop=True)
        df_sens["new_rank"] = df_sens.index + 1

        st.markdown("### Updated priority ranking")
        cols = ["admin_id", "admin_name", "new_rank", "sensitivity_score", "top_drivers", "confidence_flag"]
        st.dataframe(df_sens[cols], use_container_width=True)

        st.markdown("### What to look for")
        st.write(
            """
            - If the top-ranked units remain similar across plausible weight changes, prioritisation is robust.  
            - If rankings swing wildly, the index is sensitive and should be treated as a screening tool only.
            """
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