from __future__ import annotations

from pathlib import Path
import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[2] / "data"  # repo_root/data
BOUNDARY_DIR = DATA_DIR / "boundaries"


def list_expected_boundary_files() -> dict[str, Path]:
    """
    Defines where boundary files should live.
    We keep downloads out of code for now; this is just the contract.
    """
    return {
        "london_boroughs": BOUNDARY_DIR / "london_boroughs.geojson",
        "lagos_lgas": BOUNDARY_DIR / "lagos_lgas.geojson",
    }


def load_admin_units_stub(city: str) -> pd.DataFrame:
    city = city.strip().lower()

    if city == "london":
        units = [
            ("E09000007", "Camden"),
            ("E09000011", "Greenwich"),
            ("E09000012", "Hackney"),
            ("E09000014", "Haringey"),
            ("E09000019", "Islington"),
            ("E09000022", "Lambeth"),
            ("E09000023", "Lewisham"),
            ("E09000025", "Newham"),
            ("E09000028", "Southwark"),
            ("E09000030", "Tower Hamlets"),
            ("E09000031", "Waltham Forest"),
            ("E09000033", "Westminster"),
        ]
        return pd.DataFrame(units, columns=["admin_id", "admin_name"])

    if city == "lagos":
        units = [
            ("LGA01", "Ikeja"),
            ("LGA02", "Eti-Osa"),
            ("LGA03", "Surulere"),
            ("LGA04", "Alimosho"),
            ("LGA05", "Kosofe"),
            ("LGA06", "Mushin"),
            ("LGA07", "Shomolu"),
            ("LGA08", "Agege"),
            ("LGA09", "Apapa"),
            ("LGA10", "Ikorodu"),
        ]
        return pd.DataFrame(units, columns=["admin_id", "admin_name"])

    raise ValueError(f"Unsupported city: {city}")
