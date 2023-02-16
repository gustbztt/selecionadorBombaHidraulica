import pandas as pd
from curvas.CurvaSistema import CurvaSistema
from dfAjustados.constants import df_hm, df_NPSH, df_potencia
from interseccao.Interseccao import GetInterseccoes
from interseccao.interpolation_curve import CurveIntersection
import numpy as np
import math
from dfAjustados.constants import TAB_PERDAS
import matplotlib.pyplot as plt

dict_succao = {'diametroSuccao': '50', 'perdaSuccao': '-1,5', 'comprimentoTotalSuccao': '2', 'entradaNormal': '0', 'entradaDeBorda': '1', 'curva90RaioLongo': '0', 'curva90RaioMedio': '0', 'curva90RaioCurto': '0', 'curva45': '0',
               'curva90rd1': '0', 'registroGavetaAberto': '1', 'registroGloboAberto': '0', 'registroAnguloAberto': '0', 'TePassagemDireta': '0', 'TeSaidaLado': '0', 'TeSaidaBilateral': '0', 'valvulaPeCrivo': '0', 'valvulaRetencaoLeve': '0', 'valvulaRetencaoPesado': '0', 'saidaCanalizacao': '0', 'curva_90_rd_1_5': '0'}
dict_recalque = {'diametroRecalque': '50', 'perdaRecalque': '27', 'comprimentoTotal': '32', 'entradaNormal': '0', 'entradaDeBorda': '0', 'curva90RaioLongo': '3', 'curva90RaioMedio': '0', 'curva90RaioCurto': '0', 'curva45': '0', 'curva90rd1': '0',
                 'registroGavetaAberto': '1', 'registroGloboAberto': '0', 'registroAnguloAberto': '0', 'TePassagemDireta': '1', 'TeSaidaLado': '1', 'TeSaidaBilateral': '0', 'valvulaPeCrivo': '0', 'valvulaRetencaoLeve': '1', 'valvulaRetencaoPesado': '0', 'saidaCanalizacao': '0', 'curva_90_rd_1_5': '0'}


# from .constants import Q, V, rho, mi, g, gamma
step = 0.000001
Q = np.arange(step, 0.0555556, step)
V = np.zeros(len(Q))
g = 9.81


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
        perda_carga_localizada,
        rugosidade
    ):
        self.temperatura_agua = temperatura_agua
        self.altura_inicial = altura_inicial
        self.altura_final = altura_final
        self.diametro_cano = diametro_cano
        self.material = material
        self.comprimento_total = comprimento_total
        self.perda_carga_localizada = perda_carga_localizada
        self.rugosidade = rugosidade

    def run(self):
        # self.set_rugosidade(rugosidade)
        self.set_densidade()
        self.set_viscosidade()

        return (self.hmSistema(), self.NPSHd())

    def set_viscosidade(self):

        z = 273.15 / (self.temperatura_agua + 273.15)
        mi_zero = 0.001788
        x = -1.704 - (5.306 * z) + (7.003 * z**2) + math.log(mi_zero)

        self.mi = math.exp(x)

    def set_densidade(self):

        self.rho = 1000 - 0.0178 * (self.temperatura_agua - 4) ** 1.7

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
            + (fator_de_atrito * self.perda_carga_localizada * V**2)
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

        return (fator_de_atrito * self.perda_carga_localizada * V**2) / (self.diametro_cano * 2 * g)

    def hmSistema(self):
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
        pv = 2340
        lista_NPSHd = []
        for i in range(len(Q)):
            NPSHd = (P1 - pv) / self.gamma - \
                self.calcula_NPSH(i) - self.altura_final
            lista_NPSHd.append(NPSHd)
        NPSHd_sistema = {"Q": Q, "NPSHd": lista_NPSHd}
        df_NPSH_disponivel = pd.DataFrame(NPSHd_sistema)

        return df_NPSH_disponivel


def calcula_perda_succao(dic):
    df = pd.DataFrame(dic, index=[0])
    df = df.T
    df = df.rename(columns={0: "quantidade"})

    df_perdas = pd.DataFrame(TAB_PERDAS)
    df_perdas = df_perdas.T
    diametro = dic.get("diametroSuccao")

    df_perdas = df_perdas.merge(df, left_index=True, right_index=True)

    # assuming your dataframe is named df
    new_column_names = {i: j for i, j in enumerate(
        [13, 19, 25, 32, 38, 50, 63, 75, 100, 125, 200, 250, 300])}
    df_perdas = df_perdas.rename(columns=new_column_names)
    diametro = float(diametro)
    df_perdas = df_perdas[[diametro, "quantidade"]]
    df_perdas["quantidade"] = df_perdas["quantidade"].astype("float")
    pd.to_numeric(df_perdas[diametro], downcast="float")

    df_perdas["Perda de carga"] = df_perdas["quantidade"] * \
        df_perdas[diametro]
    perda_carga = df_perdas["Perda de carga"].sum()

    return perda_carga


def calcula_perda_recalque(dic):
    df = pd.DataFrame(dic, index=[0])
    df = df.T
    df = df.rename(columns={0: "quantidade"})

    df_perdas = pd.DataFrame(TAB_PERDAS)
    df_perdas = df_perdas.T
    diametro = dic.get("diametroRecalque")

    df_perdas = df_perdas.merge(df, left_index=True, right_index=True)

    # assuming your dataframe is named df
    new_column_names = {i: j for i, j in enumerate(
        [13, 19, 25, 32, 38, 50, 63, 75, 100, 125, 200, 250, 300])}
    df_perdas = df_perdas.rename(columns=new_column_names)
    diametro = float(diametro)
    df_perdas = df_perdas[[diametro, "quantidade"]]
    df_perdas["quantidade"] = df_perdas["quantidade"].astype("float")
    pd.to_numeric(df_perdas[diametro], downcast="float")

    df_perdas["Perda de carga"] = df_perdas["quantidade"] * \
        df_perdas[diametro]
    perda_carga = df_perdas["Perda de carga"].sum()

    return perda_carga


d1 = 50/1000
d2 = 50/1000
temperatura = 20
altura_reservatorio = 0
altura_bomba = -1.5
altura_reservatorio_recalque = 27
material = "PVC"
comprimento_tub_succao = 2
comprimento_tub_recalque = 32
rugosidade = 0.05
perda_localizada_succao = 1.9
perda_localizada_recalque = 12.5

Succao = CurvaSistema(temperatura, altura_reservatorio,
                      altura_bomba, d1, material, comprimento_tub_succao, perda_localizada_succao, rugosidade)
Recalque = CurvaSistema(temperatura, 0, altura_reservatorio_recalque,
                        d2, material, comprimento_tub_recalque, perda_localizada_recalque, rugosidade)

hm_succao, NPSHd = Succao.run()
hm_recalque, _,  = Recalque.run()


hm_sistema = pd.merge(hm_succao, hm_recalque, on='Q')
hm_sistema['Hm'] = hm_sistema['Hm_x'] + hm_sistema['Hm_y']
hm_sistema = hm_sistema[['Q', 'Hm']]

print(hm_succao)

Q_values = hm_sistema['Q']*3600
Hm_values = hm_sistema['Hm']

path = 'C:\\Users\\Avell 1513\\Desktop\\TCC I\\figuras\\graph_invisible.png'


# Set the axis limits
plt.xlim(0, 40)
plt.ylim(25, 70)

plt.tick_params(labelcolor='none', top=False,
                bottom=False, left=False, right=False)

# Plot the data with a solid color line
plt.plot(Q_values, Hm_values, color='blue')

# Save the plot with a transparent background
plt.savefig(path, transparent=True)
