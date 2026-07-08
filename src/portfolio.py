import numpy as np
import pandas as pd

def generate_portfolio(n_policies=10000, seed=7911):
    """
    Generates a life insurance portfolio of individual life insurance polices with
    issue age, gender, policy duration, and attained age. This function returns a dataframe
    that will be used as a foundation for a mortality experience study.
    """
    np.random.seed(seed)

    portfolio = pd.DataFrame({
        "policy_id": np.arange(1, n_policies + 1),
        "issue_age": np.random.randint(20, 71, n_policies),
        "gender": np.random.choice(
            ["Male", "Female"],
            n_policies,
            p=[0.52, 0.48]
        ),
        "policy_duration": np.random.randint(1, 31, n_policies)
    })

    portfolio["attained_age"] = (
        portfolio["issue_age"] +
        portfolio["policy_duration"]
    )

    return portfolio