import sys
from enum import Enum

import numpy
import pandas as pd

from curvas.CurvaBomba import GetCurvaBomba
from dfAjustados.constants import (
    listaCaminhoHm,
    listaCaminhoHmAjustado,
    listaCaminhoNPSH,
    listaCaminhoNPSHAjustado,
    listaCaminhoPotencia,
    listaCaminhoPotenciaAjustado,
)


class DataOptions(Enum):
    HM = "HM"
    NPSH = "NPSH"
    POTENCIA = "POTENCIA"


class AjustaDados:
    lista_nomes: list
    lista_nomes_ajustados: list

    def set_lista_dados_by_type(self, data_type):
        if data_type == DataOptions.HM:
            self.lista_nomes = listaCaminhoHm
            self.lista_nomes_ajustados = listaCaminhoHmAjustado

        elif data_type == DataOptions.NPSH:
            self.lista_nomes = listaCaminhoNPSH
            self.lista_nomes_ajustados = listaCaminhoNPSHAjustado

        elif data_type == DataOptions.POTENCIA:
            self.lista_nomes = listaCaminhoPotencia
            self.lista_nomes_ajustados = listaCaminhoPotenciaAjustado

    def __init__(self, data_type: DataOptions):
        self.set_lista_dados_by_type(data_type=data_type)

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
            if self.lista_nomes_ajustados == listaCaminhoHmAjustado:
                bomba = GetCurvaBomba.ajustarHmBomba(i)

            elif self.lista_nomes_ajustados == listaCaminhoNPSHAjustado:
                bomba = GetCurvaBomba.ajustarNPSHBomba(i)

            elif self.lista_nomes_ajustados == listaCaminhoPotenciaAjustado:
                bomba = GetCurvaBomba.ajustarPotenciaBomba(i)

            bomba = pd.DataFrame(bomba)
            bomba = bomba.T

            if self.lista_nomes_ajustados == listaCaminhoHmAjustado:
                bomba.columns = ["R_sq", "Hm", "Q"]
                del bomba["R_sq"]
                Hm = bomba.iloc[0]["Hm"]
                Q = bomba.iloc[0]["Q"]
                bomba = pd.DataFrame(list(zip(Q, Hm)), columns=["Q", "Hm"])

            elif self.lista_nomes_ajustados == listaCaminhoNPSHAjustado:
                bomba.columns = ["R_sq", "NPSH", "Q"]
                del bomba["R_sq"]
                NPSH = bomba.iloc[0]["NPSH"]
                Q = bomba.iloc[0]["Q"]
                bomba = pd.DataFrame(list(zip(Q, NPSH)), columns=["Q", "NPSH"])

            elif self.lista_nomes_ajustados == listaCaminhoPotenciaAjustado:
                bomba.columns = ["R_sq", "Potencia", "Q"]
                del bomba["R_sq"]
                Potencia = bomba.iloc[0]["Potencia"]
                Q = bomba.iloc[0]["Q"]
                bomba = pd.DataFrame(list(zip(Q, Potencia)), columns=["Q", "Potencia"])

            bombas.append(bomba)
            bomba.to_csv(nome, index=False)


hm = AjustaDados(DataOptions.HM)
NPSH = AjustaDados(DataOptions.NPSH)
POTENCIA = AjustaDados(DataOptions.POTENCIA)
hm.get_lista_setada()
NPSH.get_lista_setada()
POTENCIA.get_lista_setada()
