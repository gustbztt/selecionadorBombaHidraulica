from enum import Enum

import numpy as np
import pandas as pd
from typing_extensions import Self


class DataOptions(Enum):
    HM = "Hm"
    NPSH = "NPSH"
    POTENCIA = "Potencia"


class GetCurvaBomba:
    """
    arquivo: str (path)
    grau: int (grau da função de reg. linear)
    essa classe tem a intenção de armazenar os dados das bombas para que
    sejam tratados adequadamente.
    """

    def __init__(self, arquivo, grau):
        self.arquivo = arquivo
        self.grau = grau

    def ajustarDadosBomba(self):

        """
        essa função trata os dados armazenados na classe GetCurvaBomba,
        criando um dataframe com altura manométrica e vazão ajustados.
        """
        dfBomba = pd.read_csv(self.arquivo, delimiter=";", header=None, decimal=",")

        # convertendo de m³/h para m³/s
        dfBomba[0] = dfBomba[0] / 3600
        # pegando o último valor de vazão da curva
        lastNumber = dfBomba[0].iloc[-1]

        # polyfit obtem os coeficientes da curva ajustada
        curvaBomba = np.polyfit(dfBomba[0], dfBomba[1], self.grau, rcond=True)

        # coeficientesCurva transforma os coeficientes da curva
        #  calculada em vetor
        coeficientesCurva = np.array(curvaBomba)

        # polival(p, x); p = coeficientes do maior para a constante; x = vetor
        #  numpy
        vazao = np.arange(0, lastNumber, 0.000001)
        # vazao = vetor numpy; np.polival(...) = função curva
        """plt.plot(vazao, np.polyval(coeficientesCurva, vazao))
        plt.title('Altura Manométrica x Vazão')
        plt.xlabel('Vazão (m³/s)')
        plt.ylabel('Hm (m.c.a)')
        plt.show()"""

        # criando uma lista com os Hm
        lista = np.polyval(coeficientesCurva, vazao)
        listaQ = vazao

        # as linhas a seguir criar o R², para definição da precisão entre
        #  dados coletados e dados ajustados
        y_exp = dfBomba[1]
        y_pred = np.polyval(coeficientesCurva, dfBomba[0])
        corr_matrix = np.corrcoef(y_exp, y_pred)
        corr = corr_matrix[0, 1]
        R_sq = corr**2
        Rsq_adj = 1 - (1 - R_sq) * (len(y_exp) - 1) / (len(y_exp) - self.grau - 1)

        return Rsq_adj, lista, listaQ
