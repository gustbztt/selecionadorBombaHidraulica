import math

import numpy as np
import pandas as pd

# from .constants import Q, V, rho, mi, g, gamma

Q = np.arange(0.000001, 0.0083, 0.000001)
V = np.zeros(len(Q))


g = 9.81
rho = 998
mi = 1.01 * 10**-3
gamma = rho * g


class Planilhas:

    """
    classe para trazer as planilhas desejadas ao programa.
    """

    def __init__(self):
        self.carrega_planilhas()

    def carrega_planilhas(self):

        """
        as planilhas desejadas são armazenadas nesta função
        """

        dfRugosidade = pd.read_excel(
            "C:\\Users\\Avell 1513\\Desktop\\TCC I\\TabelaRugosidade.xlsx",
            sheet_name="Planilha1",
        )

        dfPerdaDeCarga = pd.read_excel(
            "C:\\Users\\Avell 1513\\Desktop\\TCC I\\TabelaPerdaDeCarga.xlsx",
            sheet_name="Planilha1",
        )

        self.dfRugosidade = dfRugosidade.set_index("Material")
        self.dfPerdaDeCarga = dfPerdaDeCarga.set_index("diâmetro (mm)")


class CurvaSistema:

    """
    temperaturaAgua: int
    alturaInicial: float
    alturaFinal: float
    diametroCano: int
    Lv: float (perda do sistema)
    material: str

    armazena os dados necessários para o cálculo da curva do sistema
    """

    def __init__(
        self, temperaturaAgua, alturaInicial, alturaFinal, diametroCano, Lv, material
    ):
        self.temperaturaAgua = temperaturaAgua
        self.alturaInicial = alturaInicial
        self.alturaFinal = alturaFinal
        self.diametroCano = diametroCano
        self.Lv = Lv
        self.material = material
        self.planilhas = Planilhas()

    def setRugosidade(self, nivelConservadorismo):

        """
        define a rugosidade do sistema a partir da planilha salva em Planilhas()
        """
        self.rugosidade = self.planilhas.dfRugosidade.loc[
            self.material, nivelConservadorismo
        ]

    def setViscosidade(self):

        z = 273.15 / (self.temperaturaAgua + 273.15)
        mi_zero = 0.001788
        x = -1.704 - (5.306 * z) + (7.003 * z**2) + math.log(mi_zero)

        self.mi = math.exp(x)

    def setDensidade(self):

        self.rho = 1000 - 0.0178 * (self.temperaturaAgua - 4) ** 1.7

    def calculaHm(self, index):

        """
        retorna um valor único de Hm para uma determinada vazão
        """
        V = 4 * Q[index] / (math.pi * self.diametroCano**2)
        reynolds = self.rho * V * self.diametroCano / self.mi
        fatorDeAtrito = (
            1
            / (
                -1.8
                * math.log(
                    (6.9 / reynolds)
                    + ((self.rugosidade / self.diametroCano) / 3.7) ** 1.11
                )
            )
        ) ** 2
        return (
            self.alturaFinal
            - self.alturaInicial
            + (fatorDeAtrito * self.Lv * V**2) / (self.diametroCano * 2 * g)
        )

    def hmSistema(self):
        """
        calcula a função de Hm para diversas vazões;
        para alterar o vetor vazão, é necessário alterar
        "Q" no início do código.
        Retorna um dataframe com os valores de Q e Hm.
        """
        listaHm = []

        for i in range(len(Q)):
            hm = self.calculaHm(i)
            listaHm.append(hm)

        curvaSistema = {"Q": Q, "Hm": listaHm}
        dfCurvaSistema = pd.DataFrame(curvaSistema)

        return dfCurvaSistema

    def NPSHd(
        self,
    ):

        """calcula NPSHd para diversas vazões;
        para alterar o vator vazão, é necessário alterar
        "Q" no início do código.
        retorna um dataframe com os valores de Q e NPSHd.
        """
        # npshd = (p1-pv)/gamma + Hs - Hp12
        self.gamma = self.rho * g
        P1 = (10330 - self.alturaInicial) * g / 0.9
        pv = 2340
        listaNPSHd = []
        for i in range(len(Q)):
            NPSHd = (P1 - pv) / self.gamma - self.calculaHm(i) + self.alturaFinal
            listaNPSHd.append(NPSHd)
        NPSHdSistema = {"Q": Q, "NPSHd": listaNPSHd}
        dfNPSHdSistema = pd.DataFrame(NPSHdSistema)

        return dfNPSHdSistema


curva1 = CurvaSistema(40, 2, 28, 0.0507, 46.8, "Aço carbono novo")
curva1.setRugosidade("Rugosidade Absoluta")
curva1.setDensidade()
curva1.setViscosidade()
a = curva1.hmSistema()

print(a)
