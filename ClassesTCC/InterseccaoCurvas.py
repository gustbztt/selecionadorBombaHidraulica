import sqlite3
import sys

import numpy as np
import pandas as pd

from curvas.CurvaSistema import CurvaSistema

con = sqlite3.connect("G:\\Scripts_Python\\bombas.db")
dfHm = pd.read_sql_query("SELECT * from bombasHm", con)
dfHm = dfHm[1:]
dfNPSH = pd.read_sql_query("SELECT * from bombasNPSH", con)
dfNPSH = dfNPSH[1:]
dfPotencia = pd.read_sql_query("SELECT * from bombasPotencia", con)
dfPotencia = dfPotencia[1:]


# salva as informações do sistema
curva1 = CurvaSistema(40, 2, 28, 0.0507, 46.8, "Aço carbono novo")
# seta a rugosidade
curva1.setRugosidade("Rugosidade Absoluta")
# obtem os dados da curva [Hm] do sistema
hmSistema = curva1.hmSistema()
NPSHd = curva1.NPSHd()


"""class IndexFuncionamento:
    def __init__(self, dfSistema, NPSHd, dfHm, dfNPSH, dfPotencia):
        self.dfSistema = dfSistema
        self.NPSHd = NPSHd
        self.dfHm = dfHm
        self.dfNPSH = dfNPSH
        self.dfPotencia = dfPotencia
"""

names = dfHm["nome_bomba"].unique()
for name in names:
    dfTeste = dfHm.loc[dfHm["nome_bomba"] == name, :]
