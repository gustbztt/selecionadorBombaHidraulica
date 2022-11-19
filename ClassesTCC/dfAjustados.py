import sys
from enum import Enum

import numpy
import pandas as pd

from curvas.CurvaBomba import GetCurvaBomba
from dfAjustados.constants import (
    lista_caminho_hm,
    lista_caminho_hm_ajustado,
    lista_caminho_NPSH,
    lista_caminho_NPSH_ajustado,
    lista_caminho_potencia,
    lista_caminho_potencia_ajustado,
)


class DataOptions(Enum):
    HM = "Hm"
    NPSH = "NPSH"
    POTENCIA = "Potencia"


class AjustaDados:
    lista_nomes: list
    lista_nomes_ajustados: list

    def set_lista_dados_by_type(self, data_type):
        if data_type == DataOptions.HM:
            self.lista_nomes = lista_caminho_hm
            self.lista_nomes_ajustados = lista_caminho_hm_ajustado

        elif data_type == DataOptions.NPSH:
            self.lista_nomes = lista_caminho_NPSH
            self.lista_nomes_ajustados = lista_caminho_NPSH_ajustado

        elif data_type == DataOptions.POTENCIA:
            self.lista_nomes = lista_caminho_potencia
            self.lista_nomes_ajustados = lista_caminho_potencia_ajustado

    def __init__(self, data_type: DataOptions):
        self.set_lista_dados_by_type(data_type=data_type)
        self.data_type = data_type.value

    def get_lista_setada(self):
        numpy.set_printoptions(threshold=sys.maxsize)

        # guarda os nomes dos arquivos que estão na pasta
        curvas = []
        for i in range(0, len(self.lista_nomes)):
            # vai criar uma lista de objetos (bombas)
            #  da classe (GetCurvaBomba(arquivo, grau))
            curvas.append(GetCurvaBomba(self.lista_nomes[i], 3))

        bombas = []
        for i, nome in zip(curvas, self.lista_nomes_ajustados):
            bomba = GetCurvaBomba.ajustarDadosBomba(i)
            bomba = pd.DataFrame(bomba)
            bomba = bomba.T
            bomba.columns = ["R_sq", self.data_type, "Q"]
            del bomba["R_sq"]
            values_list = bomba.iloc[0][self.data_type]
            Q = bomba.iloc[0]["Q"]
            bomba = pd.DataFrame(
                list(zip(Q, values_list)), columns=["Q", self.data_type]
            )
            bombas.append(bomba)
            bomba.to_csv(nome, index=False)


hm = AjustaDados(DataOptions.HM)
NPSH = AjustaDados(DataOptions.NPSH)
POTENCIA = AjustaDados(DataOptions.POTENCIA)
hm.get_lista_setada()
NPSH.get_lista_setada()
POTENCIA.get_lista_setada()
