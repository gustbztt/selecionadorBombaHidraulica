from enum import Enum

import numpy as np
import pandas as pd
from typing_extensions import Self


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

    def ajustar_dados_bomba(self):

        """
        essa função trata os dados armazenados na classe GetCurvaBomba,
        criando um dataframe com altura manométrica e vazão ajustados.
        """
        df_bomba = pd.read_csv(self.arquivo, delimiter=";", header=None, decimal=",")

        # convertendo de m³/h para m³/s
        df_bomba[0] = df_bomba[0] / 3600
        # pegando o último valor de vazão da curva
        last_number = df_bomba[0].iloc[-1]

        # polyfit obtem os coeficientes da curva ajustada
        curva_bomba = np.polyfit(df_bomba[0], df_bomba[1], self.grau, rcond=True)

        # coeficientes_curva transforma os coeficientes da curva
        #  calculada em vetor
        coeficientes_curva = np.array(curva_bomba)

        # polival(p, x); p = coeficientes do maior para a constante; x = vetor
        #  numpy
        step = 0.000003
        vazao = np.arange(0, last_number, step)
        # vazao = vetor numpy; np.polival(...) = função curva
        """plt.plot(vazao, np.polyval(coeficientes_curva, vazao))
        plt.title('Altura Manométrica x Vazão')
        plt.xlabel('Vazão (m³/s)')
        plt.ylabel('Hm (m.c.a)')
        plt.show()"""

        # criando uma lista com os Hm
        lista = np.polyval(coeficientes_curva, vazao)
        lista_Q = vazao

        # as linhas a seguir criar o R², para definição da precisão entre
        #  dados coletados e dados ajustados
        y_exp = df_bomba[1]
        y_pred = np.polyval(coeficientes_curva, df_bomba[0])
        corr_matrix = np.corrcoef(y_exp, y_pred)
        corr = corr_matrix[0, 1]
        R_sq = corr**2
        Rsq_adj = 1 - (1 - R_sq) * (len(y_exp) - 1) / (len(y_exp) - self.grau - 1)

        return Rsq_adj, lista, lista_Q
