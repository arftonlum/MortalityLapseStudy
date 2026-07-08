import numpy as np
import pandas as pd

"""
Functions for getting expected mortality rates.

Get life tables from ssa.gov, combine and polish them for usablility and add expected mortality
rates to the life insurance policy portfolio. 
"""

def load_ssa_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Get the life tables from ssa.gov and save male and female life tables as variables
    in the project.
    """
    life_table_f = pd.read_excel("../data/raw/PerLifeTables_F_Hist_TR2023.xlsx", skiprows = 4)
    life_table_m = pd.read_excel("../data/raw/PerLifeTables_M_Hist_TR2023.xlsx",skiprows = 4)
    return life_table_f,life_table_m
    
def prepare_life_table(life_table: pd.DataFrame,
                       year:int = 2020
                     ) -> pd.DataFrame:
    """
    Keep one year of life table data and rename columns for interpretibility and to line up with columns
    in the insurance policy portfolio.
    2020 is the default as that is the most recent available year on ssa.gov. 
    """
    life_table_year = life_table[life_table["Year"] == year].copy()

    life_table_year = life_table_year[["x", "q(x)"]]

    life_table_year = life_table_year.rename(columns={
        "x": "attained_age",
        "q(x)": "qx"
        })
    return life_table_year

def combine_life_tables(
        male_life_table: pd.DataFrame,
        female_life_table: pd.DataFrame
    ) -> pd.DataFrame:
    """
    Combine the male and female life tables into one life-table to be used for this study.
    """
    female_life_table = female_life_table.copy()
    male_life_table = male_life_table.copy()
    female_life_table["gender"] = "Female"
    male_life_table["gender"] = "Male"
    life_table = pd.concat(
        [female_life_table, male_life_table],
        ignore_index=True
        )
    return life_table

def merge_expected_mortality(
        portfolio: pd.DataFrame,
        life_table: pd.DataFrame
    ) -> pd.DataFrame:
    """
    Add expected mortality to the portfolio of insurance policies by combining the tables
    on age and gender.
    """
    portfolio = portfolio.merge(
        life_table,
        on=["gender", "attained_age"],
        how="left"
        )
    portfolio["expected_deaths"] = portfolio["qx"]
    return portfolio