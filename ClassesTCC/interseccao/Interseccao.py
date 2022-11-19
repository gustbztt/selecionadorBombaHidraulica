import sqlite3
import sys

sys.path.insert(
    0,
    "G:\\Scripts_Python\\selecionadorBombaHidraulica\\ClassesTCC\\curvas",
)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from CurvaSistema import CurvaSistema

con = sqlite3.connect("G:\\Scripts_Python\\bombas.db")
dfHm = pd.read_sql_query(
    "SELECT * from bombasHm",
    con,
)
dfNPSH = pd.read_sql_query("SELECT * from bombasNPSH", con)
dfPotencia = pd.read_sql_query("SELECT * from bombasPotencia", con)


def skip_header(dataframe):
    dataframe = dataframe.iloc[1:, :]
    return dataframe


def to_numeric(dataframe, column):
    # transforma a coluna com virgula de separador decimal em float
    dataframe[column] = (
        dataframe[column].astype(str).str.replace(",", ".").astype(float)
    )
    df = dataframe
    return df


df_hm = skip_header(dfHm)
df_NPSH = skip_header(dfNPSH)
df_potencia = skip_header(dfPotencia)

to_numeric(df_hm, "Q")
to_numeric(df_hm, "Hm")
to_numeric(df_NPSH, "Q")
to_numeric(df_NPSH, "NPSH")
to_numeric(df_potencia, "Q")
to_numeric(df_potencia, "Potencia")


class GetInterseccoes:
    def __init__(self, df_sistema, NPSHd, df_hm, df_NPSH, df_potencia):
        self.df_sistema = df_sistema
        self.NPSHd = NPSHd
        self.df_hm = df_hm
        self.df_NPSH = df_NPSH
        self.df_potencia = df_potencia

    def get_ponto_funcionamento(self):

        tmp = pd.merge(
            self.df_hm, self.df_sistema, on="Q", suffixes=("", "_system")
        ).assign(
            is_equal=lambda x: np.abs(x["Hm"] - x["Hm_system"]) < 0.1
        )  # find a threshold that suits your requirements

        self.temp = tmp[tmp["is_equal"]]

        return self.temp

    def get_potencia_efetiva(self):

        self.potencia_efetiva = pd.merge(self.temp, df_potencia, on=["nome_bomba", "Q"])
        self.potencia_efetiva = self.potencia_efetiva.groupby("nome_bomba").mean()

        return self.potencia_efetiva

    def get_eficiencia(self):

        gamma = 9790.38

        self.potencia_efetiva["eficiencia"] = (
            gamma * self.potencia_efetiva["Q"] * self.potencia_efetiva["Hm"]
        ) / (self.potencia_efetiva["Potencia"] * 745.7)

        self.eficiencia = self.potencia_efetiva

        return self.eficiencia

    def get_vazao_maxima(self):
        tmp = pd.merge(self.df_NPSH, self.NPSHd, on="Q").assign(
            is_equal=lambda x: np.abs(x["NPSH"] - x["NPSHd"]) < 0.1
        )

        vazao_maxima = tmp[tmp["is_equal"]]
        vazao_maxima = vazao_maxima.groupby("nome_bomba").mean()

        return vazao_maxima
