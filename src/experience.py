import numpy as np
import pandas as pd

def simulate_deaths(portfolio: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    portfolio = portfolio.copy()

    np.random.seed(seed)

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