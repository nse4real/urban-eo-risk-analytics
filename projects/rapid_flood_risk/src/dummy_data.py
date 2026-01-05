from __future__ import annotations

import numpy as np
import pandas as pd


def make_dummy_flood_priority_table(seed: int = 24, n: int = 12) -> pd.DataFrame:
    """
    Dummy basin priority outputs to scaffold the 48–72 hour decision artifact.
    """
    rng = np.random.default_rng(seed)

    zones = [f"Zone {i:02d}" for i in range(1, n + 1)]

    # Components in [0, 1]
    terrain_susceptibility = rng.uniform(0.10, 0.95, size=n)   # DEM-derived
    rainfall_intensity = rng.uniform(0.05, 0.95, size=n)       # ERA5/GPM proxy
    surface_wetness = rng.uniform(0.05, 0.95, size=n)          # NDWI-like proxy
    observed_flood_signal = rng.uniform(0.05, 0.95, size=n)    # Sentinel-1 proxy
    exposure = rng.uniform(0.05, 0.95, size=n)                # population/assets proxy

    df = pd.DataFrame(
        {
            "zone": zones,
            "terrain": terrain_susceptibility,
            "rainfall": rainfall_intensity,
            "wetness": surface_wetness,
            "s1_flood_signal": observed_flood_signal,
            "exposure": exposure,
        }
    )

    # Weighted overlay style score (transparent, operational)
    weights = {
        "terrain": 0.30,
        "rainfall": 0.25,
        "wetness": 0.15,
        "s1_flood_signal": 0.20,
        "exposure": 0.10,
    }
    df["susceptibility_score"] = (
        df["terrain"] * weights["terrain"]
        + df["rainfall"] * weights["rainfall"]
        + df["wetness"] * weights["wetness"]
        + df["s1_flood_signal"] * weights["s1_flood_signal"]
        + df["exposure"] * weights["exposure"]
    )

    # ML comparator score (dummy): correlated with overlay score + noise
    noise = rng.normal(0, 0.08, size=n)
    df["ml_score"] = (0.75 * df["susceptibility_score"] + 0.25 * df["s1_flood_signal"] + noise).clip(0, 1)

    df = df.sort_values("susceptibility_score", ascending=False).reset_index(drop=True)

    # Tiers relative within basin run
    n_high = max(1, int(np.ceil(0.20 * n)))
    n_medium = max(1, int(np.ceil(0.30 * n)))
    tiers = (["High"] * n_high) + (["Medium"] * n_medium) + (["Low"] * (n - n_high - n_medium))
    df["risk_tier"] = tiers

    # Confidence placeholder: stronger S1 signal -> higher confidence
    df["confidence_flag"] = pd.cut(
        df["s1_flood_signal"],
        bins=[-np.inf, df["s1_flood_signal"].quantile(0.33), df["s1_flood_signal"].quantile(0.66), np.inf],
        labels=["Low", "Medium", "High"],
        include_lowest=True,
    ).astype(str)

    # Fast briefing note: top 2 drivers
    driver_names = {
        "terrain": "Terrain susceptibility",
        "rainfall": "High rainfall",
        "wetness": "High wetness",
        "s1_flood_signal": "Observed flood signal",
        "exposure": "High exposure",
    }
    component_cols = ["terrain", "rainfall", "wetness", "s1_flood_signal", "exposure"]

    drivers = []
    for _, row in df.iterrows():
        top2 = row[component_cols].sort_values(ascending=False).index[:2].tolist()
        drivers.append(", ".join(driver_names[c] for c in top2))
    df["top_drivers"] = drivers

    return df