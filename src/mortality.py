import numpy as np
import pandas as pd

def load_ssa_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    life_table_f = pd.read_excel("../data/raw/PerLifeTables_F_Hist_TR2023.xlsx", skiprows = 4)
    life_table_m = pd.read_excel("../data/raw/PerLifeTables_M_Hist_TR2023.xlsx",skiprows = 4)
    return life_table_f,life_table_m
    
def prepare_life_table(life_table: pd.DataFrame,
                       year:int = 2020
                     ) -> pd.DataFrame:
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
    
    portfolio = portfolio.merge(
        life_table,
        on=["gender", "attained_age"],
        how="left"
        )
    portfolio["expected_deaths"] = portfolio["qx"]
    return portfolio