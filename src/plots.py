import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Visualization functions for the mortality experience study.

Provides plotting functions for comparing expected and actualt mortality experience.
"""




def plot_expected_vs_actual(experience):
    """
    Plot expected and observed deaths by attained age.
    """
    plt.figure(figsize=(10, 6))

    plt.plot(
        experience["attained_age"],
        experience["expected_deaths"],
        label="Expected Deaths"
    )

    plt.plot(
        experience["attained_age"],
        experience["actual_deaths"],
        label="Actual Deaths"
    )

    plt.xlabel("Attained Age")
    plt.ylabel("Deaths")
    plt.title("Expected vs. Actual Deaths by Attained Age")

    plt.legend()

    plt.grid(alpha=0.3)

    plt.show()


def plot_ae_by_age(experience):
    """
    Displays the ratio of actual to expected deaths for each attained age with
    a reference line at 1.0 indicating expected mortality experience (a perfect prediction).
    """
    plt.figure(figsize=(10,6))

    plt.plot(
        experience["attained_age"],
        experience["AE"],
        marker="o"
    )

    plt.axhline(
        y=1.0,
        linestyle="--",
        label="Expected"
    )

    plt.xlabel("Attained Age")
    plt.ylabel("Actual / Expected")

    plt.title("Mortality A/E by Attained Age")

    plt.legend()

    plt.grid(alpha=0.3)

    plt.show()

def plot_ae_by_age_band(band_experience):
    """
    Plot the Actual-to-Expected mortality ratio by age band to reduce random variation and
    be more interpretable.
    """
    plt.figure(figsize=(9,5))

    plt.bar(
        band_experience.index.astype(str),
        band_experience["AE"]
    )

    plt.axhline(
        1.0,
        linestyle="--",
        label="Expected"
    )

    plt.ylabel("Actual / Expected")
    plt.xlabel("Age Band")
    plt.title("Mortality A/E by Age Band")

    plt.legend()

    plt.show()
