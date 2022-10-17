import sqlite3
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from curvas.CurvaSistema import CurvaSistema

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


# salva as informações do sistema
curva1 = CurvaSistema(50, 2, 50, 0.0507, 27, "Aço carbono novo")
# seta a rugosidade
curva1.setRugosidade("Rugosidade Absoluta")
curva1.setDensidade()
curva1.setViscosidade()
# obtem os dados da curva [Hm] do sistema
df_sistema = curva1.hmSistema()
NPSHd = curva1.NPSHd()


# Plot the curves
fig, ax = plt.subplots(figsize=(10, 6))
for name, sub_df in df_hm.groupby("nome_bomba"):
    ax.plot(sub_df["Q"], sub_df["Hm"], label=name)

ax.plot(df_sistema["Q"], df_sistema["Hm"], label="System", linestyle="--")
ax.set_xlabel("Q")
ax.set_ylabel("Hm")
ax.legend()
plt.show()


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
            is_equal=lambda x: np.abs(x["Hm"] - x["Hm_system"]) < 0.01
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
            gamma * potencia_efetiva["Q"] * potencia_efetiva["Hm"]
        ) / (potencia_efetiva["Potencia"] * 745.7)

        self.eficiencia = self.potencia_efetiva

        return self.eficiencia

    def get_vazao_maxima(self):
        tmp = pd.merge(self.df_NPSH, self.NPSHd, on="Q").assign(
            is_equal=lambda x: np.abs(x["NPSH"] - x["NPSHd"]) < 0.01
        )

        vazao_maxima = tmp[tmp["is_equal"]]
        vazao_maxima = vazao_maxima.groupby("nome_bomba").mean()

        return vazao_maxima


interseccoes = GetInterseccoes(df_sistema, NPSHd, df_hm, df_NPSH, df_potencia)
ponto_funcionamento = interseccoes.get_ponto_funcionamento()
potencia_efetiva = interseccoes.get_potencia_efetiva()
eficiencia = interseccoes.get_eficiencia()
vazao_maxima = interseccoes.get_vazao_maxima()
print(eficiencia)
