from __future__ import annotations

import numpy as np
import pandas as pd

from projects.urban_growth_risk.src.boundaries import load_admin_units_stub


def make_dummy_risk_table(city: str, seed: int = 42) -> pd.DataFrame:
    """
    Create a dummy admin-unit risk table with plausible component structure.
    This scaffolds the decision artifact before EO features are wired in.
    """
    rng = np.random.default_rng(seed)

    admins = load_admin_units_stub(city)
    n = len(admins)

    # Component scores in [0, 1]
    expansion_rate = rng.uniform(0.15, 0.95, size=n)
    abruptness = rng.uniform(0.10, 0.90, size=n)
    exposure = rng.uniform(0.05, 0.95, size=n)
    infra_constraint = rng.uniform(0.05, 0.95, size=n)

    df = pd.DataFrame(
        {
            "admin_id": admins["admin_id"],
            "admin_name": admins["admin_name"],
            "expansion_rate": expansion_rate,
            "abruptness": abruptness,
            "exposure": exposure,
            "infra_constraint": infra_constraint,
        }
    )

    # Composite score using explicit weights (transparent, not optimised)
    weights = {
        "expansion_rate": 0.35,
        "abruptness": 0.25,
        "exposure": 0.20,
        "infra_constraint": 0.20,
    }
    df["composite_score"] = (
        df["expansion_rate"] * weights["expansion_rate"]
        + df["abruptness"] * weights["abruptness"]
        + df["exposure"] * weights["exposure"]
        + df["infra_constraint"] * weights["infra_constraint"]
    )

    # Relative tiers within the current run (triage, not absolutes)
    df = df.sort_values("composite_score", ascending=False).reset_index(drop=True)

    # Tier cutoffs: top 20% high, next 30% medium, rest low
    n_high = max(1, int(np.ceil(0.20 * n)))
    n_medium = max(1, int(np.ceil(0.30 * n)))

    tiers = (["High"] * n_high) + (["Medium"] * n_medium) + (["Low"] * (n - n_high - n_medium))
    df["risk_tier"] = tiers

    # Simple confidence flag proxy (placeholder until validation exists)
    df["confidence_flag"] = pd.cut(
        df["composite_score"],
        bins=[
            -np.inf,
            df["composite_score"].quantile(0.33),
            df["composite_score"].quantile(0.66),
            np.inf,
        ],
        labels=["Low", "Medium", "High"],
        include_lowest=True,
    ).astype(str)

    # Human-readable drivers: top 2 components for each unit
    component_cols = ["expansion_rate", "abruptness", "exposure", "infra_constraint"]
    driver_names = {
        "expansion_rate": "Rapid built-up growth",
        "abruptness": "Sudden change",
        "exposure": "High exposure",
        "infra_constraint": "Infrastructure constraint",
    }

    drivers = []
    for _, row in df.iterrows():
        top2 = row[component_cols].sort_values(ascending=False).index[:2].tolist()
        drivers.append(", ".join(driver_names[c] for c in top2))
    df["top_drivers"] = drivers

    return df