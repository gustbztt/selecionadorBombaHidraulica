import matplotlib.font_manager as fm
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from curvas.CurvaSistema import CurvaSistema
from dfAjustados.constants import TAB_PERDAS, df_hm, df_NPSH, df_potencia
from interseccao.interpolation_curve import CurveIntersection

dict_recalque = {
    'diametroRecalque': '63',
    'perdaRecalque': '55',
    'comprimentoTotal': '75',
    'entradaNormal': '0',
    'entradaDeBorda': '1',
    'curva90RaioLongo': '0',
    'curva90RaioMedio': '3',
    'curva90RaioCurto': '0',
    'curva45': '0',
    'curva90rd1': '0',
    'registroGavetaAberto': '0',
    'registroGloboAberto': '0',
    'registroAnguloAberto': '0',
    'TePassagemDireta': '0',
    'TeSaidaLado': '1',
    'TeSaidaBilateral': '0',
    'valvulaPeCrivo': '1',
    'valvulaRetencaoLeve': '0',
    'valvulaRetencaoPesado': '0',
    'saidaCanalizacao': '1',
    'curva_90_rd_1_5': '0'}

dict_succao = {
    'diametroSuccao': '75',
    'perdaSuccao': '5',
    'comprimentoTotalSuccao': '7',
    'entradaNormal': '1',
    'entradaDeBorda': '0',
    'curva90RaioLongo': '0',
    'curva90RaioMedio': '0',
    'curva90RaioCurto': '1',
    'curva45': '1',
    'curva90rd1': '0',
    'registroGavetaAberto': '1',
    'registroGloboAberto': '0',
    'registroAnguloAberto': '0',
    'TePassagemDireta': '0',
    'TeSaidaLado': '0',
    'TeSaidaBilateral': '0',
    'valvulaPeCrivo': '0',
    'valvulaRetencaoLeve': '0',
    'valvulaRetencaoPesado': '0',
    'saidaCanalizacao': '0',
    'curva_90_rd_1_5': '0'}


step = 0.000003
Q = np.arange(step, 0.2, step)
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
        rugosidade,
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

        return (fator_de_atrito * self.perda_carga_localizada * V**2) / (
            self.diametro_cano * 2 * g
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
    new_column_names = {
        i: j
        for i, j in enumerate(
            [13, 19, 25, 32, 38, 50, 63, 75, 100, 125, 150, 200, 250, 300]
        )
    }
    df_perdas = df_perdas.rename(columns=new_column_names)
    diametro = float(diametro)
    df_perdas = df_perdas[[diametro, "quantidade"]]
    df_perdas["quantidade"] = df_perdas["quantidade"].astype("float")
    pd.to_numeric(df_perdas[diametro], downcast="float")

    df_perdas["Perda de carga"] = df_perdas["quantidade"] * df_perdas[diametro]
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
    new_column_names = {
        i: j
        for i, j in enumerate(
            [13, 19, 25, 32, 38, 50, 63, 75, 100, 125, 150, 200, 250, 300]
        )
    }
    df_perdas = df_perdas.rename(columns=new_column_names)
    diametro = float(diametro)
    df_perdas = df_perdas[[diametro, "quantidade"]]
    df_perdas["quantidade"] = df_perdas["quantidade"].astype("float")
    pd.to_numeric(df_perdas[diametro], downcast="float")

    df_perdas["Perda de carga"] = df_perdas["quantidade"] * df_perdas[diametro]
    perda_carga = df_perdas["Perda de carga"].sum()

    return perda_carga


d1 = 75 / 1000
d2 = 63 / 1000
temperatura = 25
altura_reservatorio = 0
altura_bomba = 5
altura_reservatorio_recalque = 55
material = "PVC"
comprimento_tub_succao = 7
comprimento_tub_recalque = 75
rugosidade = 0.0015
perda_localizada_succao = calcula_perda_succao(dict_succao)
perda_localizada_recalque = calcula_perda_recalque(dict_recalque)

Succao = CurvaSistema(
    temperatura,
    0,
    altura_bomba,
    d1,
    material,
    comprimento_tub_succao,
    perda_localizada_succao,
    0.0015,
)
Recalque = CurvaSistema(
    temperatura,
    altura_bomba,
    altura_reservatorio_recalque,
    d2,
    material,
    comprimento_tub_recalque,
    perda_localizada_recalque,
    0.0015,
)

hm_succao, NPSHd = Succao.run()
(
    hm_recalque,
    _,
) = Recalque.run()


hm_sistema = pd.merge(hm_succao, hm_recalque, on="Q")
hm_sistema["Hm"] = hm_sistema["Hm_x"] + hm_sistema["Hm_y"]
hm_sistema1 = hm_sistema[["Q", "Hm"]]


Q_values = hm_sistema1["Q"]*3600
hm_values = hm_sistema1["Hm"]



'''df_hm = pd.read_csv(
    "C:\\Users\\Avell 1513\\Desktop\\TCC I\\hmsAjustados\\ksb_meganorm 40-160 174 3500.csv",
    delimiter=",",
    decimal=".",
)

x_values = df_hm["Q"].values
y_values = df_hm["Hm"].values'''
#path = 'C:\\Users\\Avell 1513\\Desktop\\TCC I\\figuras\\graph_invisible_npsh2.png'


# Set the axis limits
plt.xlim(0, 140)
plt.ylim(0, 10)

plt.tick_params(labelcolor='none', top=False,
                bottom=False, left=False, right=False)

# Plot the data with a solid color line
plt.plot(Q_values, hm_values, color='blue')

# Save the plot with a transparent background
# plt.savefig(path, transparent=True)


# Set Arial font and font size
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 12

# Plot scatter points and lines
plt.scatter(Q_values*3600, hm_values, label='Curva da bomba', s=1, c='red')
plt.scatter(Q_values*3600, hm_sistema1,
            label='Curva do sistema', s=1, c='blue')

plt.xlim(0, 75)
plt.ylim(0, 100)

# Set title and axis labels
plt.title('Curvas genéricas')
plt.xlabel('Q (m³/h)')
plt.ylabel('Hm (m.c.a.)')

# Set legend
plt.legend()

# Show plot
plt.show()
