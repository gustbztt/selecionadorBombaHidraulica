import sqlite3
from glob import glob

import pandas as pd

"""
esse arquivo tem a função de armazenar constantes que serão usadas
posteriormente no código.
"""


# folder_path é o caminho onde estão armazenados os dados desejados

folder_path = "C:\\Users\\Avell 1513\\Desktop\\TCC I\\"

# nome das pastas finais
hm_folder = "Gráficos das bombasHm_teste"
NPSH_folder = "Gráficos das bombasNPSH_teste"
potencia_folder = "Gráficos das bombasPotencia_teste"
lista_caminho_hm = []  # type: list[str]
lista_caminho_NPSH = []  # type: list[str]
lista_caminho_potencia = []  # type: list[str]


# utilizar uma única função (esperar aux. de branch)
caminho_hm = glob(folder_path + hm_folder + "\\*.csv")
for i in caminho_hm:
    arquivo = i.replace("\\", "/")
    lista_caminho_hm.append(arquivo)

caminho_NPSH = glob(folder_path + NPSH_folder + "\\*.csv")
for i in caminho_NPSH:
    arquivo = i.replace("\\", "/")
    lista_caminho_NPSH.append(arquivo)

caminho_potencia = glob(folder_path + potencia_folder + "\\*.csv")
for i in caminho_potencia:
    arquivo = i.replace("\\", "/")
    lista_caminho_potencia.append(arquivo)

lista_caminho_hm_ajustado = []  # type: list[str]
for i in lista_caminho_hm:
    a = i.replace(hm_folder, "hmsAjustados")
    lista_caminho_hm_ajustado.append(a)

lista_caminho_NPSH_ajustado = []  # type: list[str]
for i in lista_caminho_NPSH:
    a = i.replace(NPSH_folder, "NPSHsAjustados")
    lista_caminho_NPSH_ajustado.append(a)

lista_caminho_potencia_ajustado = []  # type: list[str]
for i in lista_caminho_potencia:
    a = i.replace(potencia_folder, "PotenciasAjustados")
    lista_caminho_potencia_ajustado.append(a)

lista_caminho_hm.sort()
lista_caminho_hm_ajustado.sort()
lista_caminho_NPSH.sort()
lista_caminho_NPSH_ajustado.sort()
lista_caminho_potencia.sort()
lista_caminho_potencia_ajustado.sort()

con = sqlite3.connect("G:\\Scripts_Python\\bombas.db")
dfHm = pd.read_sql_query(
    "SELECT * from bombasHm",
    con,
)
dfNPSH = pd.read_sql_query("SELECT * from bombasNPSH", con)
dfPotencia = pd.read_sql_query("SELECT * from bombasPotencia", con)

df_hm = dfHm.drop(0, axis=0)
df_hm.columns = ["nome_bomba", "Q", "Hm"]

df_NPSH = dfNPSH.drop(0, axis=0)
df_NPSH.columns = ["nome_bomba", "Q", "NPSH"]

df_potencia = dfPotencia.drop(0, axis=0)
df_potencia.columns = ["nome_bomba", "Q", "Potencia"]


def to_numeric(dataframe, column):
    # transforma a coluna com virgula de separador decimal em float
    dataframe.loc[:, column] = (dataframe[column].astype(
        str).str.replace(",", ".").astype(float))

    return dataframe


to_numeric(df_hm, "Q")
to_numeric(df_hm, "Hm")
to_numeric(df_NPSH, "Q")
to_numeric(df_NPSH, "NPSH")
to_numeric(df_potencia, "Q")
to_numeric(df_potencia, "Potencia")


# Load the excel file and save it to a variable
tabPerdas = pd.read_excel(
    "C:/Users/Avell 1513/Desktop/TCC I/TabelaPerdaDeCarga.xlsx")

# Save the variable to a constant
TAB_PERDAS = tabPerdas
