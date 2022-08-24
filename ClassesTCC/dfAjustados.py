import sys

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


def ajustaDadosHm():
    numpy.set_printoptions(threshold=sys.maxsize)
    # guarda os nomes dos arquivos que estão na pasta
    curvasHm = []
    for i in range(0, len(listaCaminhoHm)):
        # vai criar uma lista de objetos (bombas)
        #  da classe (GetCurvaBomba(arquivo, grau))
        curvasHm.append(GetCurvaBomba(listaCaminhoHm[i], 3))

    bombas = []
    for i, nome in zip(curvasHm, listaCaminhoHmAjustado):
        bomba = GetCurvaBomba.ajustarHmBomba(i)
        bomba = pd.DataFrame(bomba)
        bomba = bomba.T
        bomba.columns = ["R_sq", "Hm", "Q"]
        del bomba["R_sq"]
        Hm = bomba.iloc[0]["Hm"]
        Q = bomba.iloc[0]["Q"]
        bomba = pd.DataFrame(list(zip(Q, Hm)), columns=["Q", "Hm"])
        bombas.append(bomba)
        bomba.to_csv(nome, index=False)


def ajustaDadosNPSH():
    numpy.set_printoptions(threshold=sys.maxsize)
    # guarda os nomes dos arquivos que estão na pasta
    curvasNPSH = []
    for i in range(0, len(listaCaminhoNPSH)):
        # vai criar uma lista de objetos (bombas)
        #  da classe (GetCurvaBomba(arquivo, grau))
        curvasNPSH.append(GetCurvaBomba(listaCaminhoNPSH[i], 3))

    bombas = []
    for i, nome in zip(curvasNPSH, listaCaminhoNPSHAjustado):
        bomba = GetCurvaBomba.ajustarNPSHBomba(i)
        bomba = pd.DataFrame(bomba)
        bomba = bomba.T
        bomba.columns = ["R_sq", "NPSH", "Q"]
        del bomba["R_sq"]
        NPSH = bomba.iloc[0]["NPSH"]
        Q = bomba.iloc[0]["Q"]
        bomba = pd.DataFrame(list(zip(Q, NPSH)), columns=["Q", "NPSH"])
        bombas.append(bomba)
        bomba.to_csv(nome, index=False)


def ajustaDadosPotencia():
    numpy.set_printoptions(threshold=sys.maxsize)
    # guarda os nomes dos arquivos que estão na pasta
    curvasPotencia = []
    for i in range(0, len(listaCaminhoPotencia)):
        # vai criar uma lista de objetos (bombas)
        #  da classe (GetCurvaBomba(arquivo, grau))
        curvasPotencia.append(GetCurvaBomba(listaCaminhoPotencia[i], 3))

    bombas = []
    for i, nome in zip(curvasPotencia, listaCaminhoPotenciaAjustado):
        bomba = GetCurvaBomba.ajustarPotenciaBomba(i)
        bomba = pd.DataFrame(bomba)
        bomba = bomba.T
        bomba.columns = ["R_sq", "Potencia", "Q"]
        del bomba["R_sq"]
        Potencia = bomba.iloc[0]["Potencia"]
        Q = bomba.iloc[0]["Q"]
        bomba = pd.DataFrame(list(zip(Q, Potencia)), columns=["Q", "Potencia"])
        bombas.append(bomba)
        bomba.to_csv(nome, index=False)


# sugestão: mover "Hm", "Potencia" e "NPSH" para o arg. da função
ajustaDadosHm()
ajustaDadosPotencia()
ajustaDadosNPSH()
