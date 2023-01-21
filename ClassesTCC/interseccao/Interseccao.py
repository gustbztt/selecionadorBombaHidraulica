import sqlite3
import sys

sys.path.insert(
    0,
    "G:\\Scripts_Python\\selecionadorBombaHidraulica\\ClassesTCC\\curvas",
)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class GetInterseccoes:
    def __init__(self, df_sistema, NPSHd, df_hm, df_NPSH, df_potencia):
        self.df_sistema = df_sistema
        self.NPSHd = NPSHd
        self.df_hm = df_hm
        self.df_NPSH = df_NPSH
        self.df_potencia = df_potencia

    def run(self):
        self.get_ponto_funcionamento()
        self.get_potencia_efetiva()
        self.get_eficiencia()
        self.get_vazao_maxima()
        return self.check_cavitation()

    def get_ponto_funcionamento(self):

        # gets the Q where the Hm from the two datasets are the same
        tmp = pd.merge(self.df_hm, self.df_sistema, on="Q", suffixes=("", "_system"))
        tmp["is_equal"] = np.isclose(tmp["Hm"], tmp["Hm_system"], rtol=0.1, atol=0.01)
        self.temp = tmp[tmp["is_equal"]]
        return self.temp

    def get_potencia_efetiva(self):

        # merges the dfs to get potencia efetiva
        self.potencia_efetiva = pd.merge(
            self.temp, self.df_potencia, on=["nome_bomba", "Q"]
        )
        self.potencia_efetiva = self.potencia_efetiva.groupby(
            "nome_bomba", as_index=False
        ).mean()

        self.potencia_efetiva = self.potencia_efetiva.rename(
            columns={"Q": "Vazao_de_funcionamento"}
        )
        return self.potencia_efetiva

    def get_eficiencia(self):
        # calcs eficiencia and returns df w/ all previous columns

        gamma = 9790.38
        self.potencia_efetiva["eficiencia"] = (
            gamma
            * self.potencia_efetiva["Vazao_de_funcionamento"]
            * self.potencia_efetiva["Hm"]
        ) / (self.potencia_efetiva["Potencia"] * 745.7)

        self.eficiencia = self.potencia_efetiva

        return self.eficiencia

    def get_vazao_maxima(self):
        tmp = pd.merge(self.df_NPSH, self.NPSHd, on="Q")
        tmp["is_equal"] = np.isclose(tmp["NPSH"], tmp["NPSHd"], rtol=0.1, atol=0.01)
        self.vazao_maxima = tmp[tmp["is_equal"]]
        self.vazao_maxima = self.vazao_maxima.groupby(
            "nome_bomba", as_index=False
        ).mean()
        return self.vazao_maxima

    def check_cavitation(self):
        self.check_if_cavitates = pd.merge(
            self.vazao_maxima, self.eficiencia, on=["nome_bomba"]
        )

        self.check_if_cavitates = self.check_if_cavitates.rename(
            columns={
                "Q": "Vazao_maxima",
            }
        )

        self.check_if_cavitates = self.check_if_cavitates.query(
            "Vazao_maxima > Vazao_de_funcionamento"
        )

        self.working_pumps = self.check_if_cavitates[
            [
                "nome_bomba",
                "Vazao_de_funcionamento",
                "NPSH",
                "Vazao_maxima",
                "Hm",
                "Potencia",
                "eficiencia",
            ]
        ]

        self.working_pumps = self.working_pumps.sort_values(
            by=["eficiencia"], ascending=False
        )
        self.working_pumps = self.working_pumps.rename(
            columns={
                "nome_bomba": "Nome da bomba",
                "Vazao_de_funcionamento": "Vazão de funcionamento",
                "Vazao_maxima": "Vazão máxima",
                "Potencia": "Potência",
                "eficiencia": "Eficiência",
            }
        )

        self.working_pumps = self.working_pumps.query(
            "`Vazão de funcionamento` > 0 & Potência > 0 & Eficiência > 0 & NPSH > 0"
        )

        """self.output = self.working_pumps.to_string(
            formatters={"Eficiência": "{:,.2%}".format}
        )"""
        return self.working_pumps
