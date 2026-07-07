import numpy as np
import pandas as pd

def assign_mortality_multiplier(portfolio, young = .9, middle = 1, old = 1.15):
    multiplier = np.ones(len(portfolio))

    multiplier *= np.where(
        portfolio["attained_age"] < 50,
        young,
        np.where(
            portfolio["attained_age"] >= 75,old,middle,
        )
    )
    multiplier *= np.where(
        portfolio["policy_duration"] <= 5,
        0.85,
        1,
    )
    noise = np.random.normal(
        loc=1.0,
        scale=0.05,
        size=len(portfolio)
    )

    multiplier *= noise

    multiplier = np.clip(
        multiplier,
        0.70,
        1.30
    )
    portfolio["mortality_multiplier"] = multiplier
    return portfolio
    

def simulate_deaths(portfolio: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    portfolio = portfolio.copy()

    np.random.seed(seed)

    portfolio["actual_qx"] = (
        portfolio["qx"] *
        portfolio["mortality_multiplier"]
    )

    portfolio["death"] = np.random.binomial(
        n=1,
        p=portfolio["qx"]
    )

    portfolio["expected_deaths"] = portfolio["qx"]

    return portfolio


def summarize_experience(portfolio: pd.DataFrame) -> pd.DataFrame:
    experience = (
        portfolio
        .groupby("attained_age")
        .agg(
            exposure=("policy_id", "count"),
            expected_deaths=("expected_deaths", "sum"),
            actual_deaths=("death", "sum")
        )
        .reset_index()
    )
    experience["expected_rate"] = (
        experience["expected_deaths"] /
        experience["exposure"]
    )

    experience["actual_rate"] = (
        experience["actual_deaths"] /
        experience["exposure"]
    )

    experience["AE"] = (
        experience["actual_deaths"] /
        experience["expected_deaths"]
    )

    return experience

def summarize_by_age_band(portfolio: pd.DataFrame, bins = None, labels = None) -> pd.DataFrame:
    portfolio = portfolio.copy()
    if bins is None:
        bins = [20, 30, 40, 50, 60, 70, 80, 90, 101]
    if labels is None:
        labels = [
            "20–29",
            "30–39",
            "40–49",
            "50–59",
            "60–69",
            "70–79",
            "80–89",
            "90–100"
        ]

    age_band = pd.cut(
        portfolio["attained_age"],
        bins=bins,
        labels=labels,
        right=False
    )


    band_experience = (
        portfolio
        .groupby(age_band)
        .agg(
            exposure=("policy_id", "count"),
            expected_deaths=("expected_deaths", "sum"),
            actual_deaths=("death", "sum")
        )
    )

    band_experience["AE"] = (
        band_experience["actual_deaths"] /
        band_experience["expected_deaths"]
    )

    return band_experience

def calculate_overall_ae(experience):
    overall_AE = (
        experience["actual_deaths"].sum() /
        experience["expected_deaths"].sum()
    )
    return overall_AE