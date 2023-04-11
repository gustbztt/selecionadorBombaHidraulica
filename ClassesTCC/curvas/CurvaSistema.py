import math
from dfAjustados.constants import TAB_PERDAS
import numpy as np
import pandas as pd

# from .constants import Q, V, rho, mi, g, gamma
step = 0.000003
Q = np.arange(step, 0.2, step)
V = np.zeros(len(Q))
g = 9.81


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

        df_rugosidade = pd.read_excel(
            "C:\\Users\\Avell 1513\\Desktop\\TCC I\\TabelaRugosidade.xlsx",
            sheet_name="Planilha1",
        )

        self.df_rugosidade = df_rugosidade.set_index("Material")


class CurvaSistema:

    """
    temperatura_agua: int
    altura_inicial: float
    altura_final: float
    diametro_cano: int
    material: str

    armazena os dados necessários para o cálculo da curva do sistema
    """

    def __init__(
        self,
        temperatura_agua,
        altura_inicial,
        altura_final,
        diametro_cano,
        material,
        comprimento_total,
    ):
        self.temperatura_agua = temperatura_agua
        self.altura_inicial = altura_inicial
        self.altura_final = altura_final
        self.diametro_cano = diametro_cano
        self.material = material
        self.comprimento_total = comprimento_total
        self.planilhas = Planilhas()

    def run_succao(self, rugosidade, dict_succao):
        self.set_rugosidade(rugosidade)
        self.set_densidade()
        self.set_viscosidade()
        self.set_pv()
        self.calcula_perda_succao(dict_succao)
        return self.NPSHd(), self.hm_sistema(), self.rho

    def run_recalque(self, rugosidade, dict_recalque):
        self.set_rugosidade(rugosidade)
        self.set_densidade()
        self.set_viscosidade()
        self.set_pv()
        self.calcula_perda_recalque(dict_recalque)
        return self.hm_sistema()

    def set_rugosidade(self, nivel_conservadorismo):
        # define a rugosidade do sistema a partir da planilha salva em Planilhas()
        self.rugosidade = self.planilhas.df_rugosidade.loc[
            self.material, nivel_conservadorismo
        ]

    def set_viscosidade(self):

        z = 273.15 / (self.temperatura_agua + 273.15)
        mi_zero = 0.001788
        x = -1.704 - (5.306 * z) + (7.003 * z**2) + math.log(mi_zero)

        self.mi = math.exp(x)

    def set_densidade(self):

        self.rho = 1000 - 0.0178 * (self.temperatura_agua - 4) ** 1.7

    def set_pv(self):
        A = 8.07131
        B = 1730.63
        C = 233.426
        exp = A - (B/(C+self.temperatura_agua))
        self.Pv = (10**exp)*133.322

    def calcula_perda_succao(self, dic):
        df = pd.DataFrame(dic, index=[0])
        df = df.T
        df = df.rename(columns={0: "quantidade"})

        df_perdas = pd.DataFrame(TAB_PERDAS)
        df_perdas = df_perdas.T
        diametro = dic.get("diametroSuccao")

        df_perdas = df_perdas.merge(df, left_index=True, right_index=True)

        # assuming your dataframe is named df
        new_column_names = {i: j for i, j in enumerate(
            [13, 19, 25, 32, 38, 50, 63, 75, 100, 125, 150, 200, 250, 300])}
        df_perdas = df_perdas.rename(columns=new_column_names)
        diametro = float(diametro)
        df_perdas = df_perdas[[diametro, "quantidade"]]
        df_perdas["quantidade"] = df_perdas["quantidade"].astype("float")
        pd.to_numeric(df_perdas[diametro], downcast="float")

        df_perdas["Perda de carga"] = df_perdas["quantidade"] * \
            df_perdas[diametro]
        self.perda_carga = df_perdas["Perda de carga"].sum()

        return self.perda_carga

    def calcula_perda_recalque(self, dic):
        df = pd.DataFrame(dic, index=[0])
        df = df.T
        df = df.rename(columns={0: "quantidade"})

        df_perdas = pd.DataFrame(TAB_PERDAS)
        df_perdas = df_perdas.T
        diametro = dic.get("diametroRecalque")

        df_perdas = df_perdas.merge(df, left_index=True, right_index=True)

        # assuming your dataframe is named df
        new_column_names = {i: j for i, j in enumerate(
            [13, 19, 25, 32, 38, 50, 63, 75, 100, 125, 150, 200, 250, 300])}
        df_perdas = df_perdas.rename(columns=new_column_names)
        diametro = float(diametro)
        df_perdas = df_perdas[[diametro, "quantidade"]]
        df_perdas["quantidade"] = df_perdas["quantidade"].astype("float")
        pd.to_numeric(df_perdas[diametro], downcast="float")

        df_perdas["Perda de carga"] = df_perdas["quantidade"] * \
            df_perdas[diametro]
        self.perda_carga = df_perdas["Perda de carga"].sum()

        return self.perda_carga

    def calcula_hm(self, index):
        # retorna um valor único de Hm para uma determinada vazão
        V = 4 * Q[index] / (math.pi * self.diametro_cano**2)
        reynolds = self.rho * V * self.diametro_cano / self.mi
        fator_de_atrito = (
            1
            / (
                -1.8
                * math.log(
                    (6.9 / reynolds)
                    + ((self.rugosidade / self.diametro_cano) / 3.7) ** 1.11
                )
            )
        ) ** 2

        return (
            self.altura_final
            - self.altura_inicial
            + (fator_de_atrito * self.perda_carga * V**2)
            / (self.diametro_cano * 2 * g)
        )

    def calcula_NPSH(self, index):
        """
        retorna um valor único de Hm para uma determinada vazão
        """
        V = 4 * Q[index] / (math.pi * self.diametro_cano**2)
        reynolds = self.rho * V * self.diametro_cano / self.mi
        fator_de_atrito = (
            1
            / (
                -1.8
                * math.log(
                    (6.9 / reynolds)
                    + ((self.rugosidade / self.diametro_cano) / 3.7) ** 1.11
                )
            )
        ) ** 2

        return (fator_de_atrito * self.perda_carga * V**2) / (self.diametro_cano * 2 * g)

    def hm_sistema(self):
        """
        calcula a função de Hm para diversas vazões;
        para alterar o vetor vazão, é necessário alterar
        "Q" no início do código.
        Retorna um dataframe com os valores de Q e Hm.
        """
        listaHm = []

        for i in range(len(Q)):
            hm = self.calcula_hm(i)
            listaHm.append(hm)

        curva_sistema = {"Q": Q, "Hm": listaHm}
        df_curva_sistema = pd.DataFrame(curva_sistema)

        return df_curva_sistema

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
        P1 = (10330 - self.altura_inicial) * g / 0.9

        lista_NPSHd = []
        for i in range(len(Q)):
            NPSHd = (P1 - self.Pv) / self.gamma - \
                self.calcula_NPSH(i) - self.altura_final
            lista_NPSHd.append(NPSHd)
        NPSHd_sistema = {"Q": Q, "NPSHd": lista_NPSHd}
        df_NPSH_disponivel = pd.DataFrame(NPSHd_sistema)

        return df_NPSH_disponivel
