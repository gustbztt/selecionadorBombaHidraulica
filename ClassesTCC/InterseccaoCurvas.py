import sys

import numpy as np
import pandas as pd

from curvas.CurvaSistema import CurvaSistema
from dfAjustados.constants import (
    listaCaminhoHmAjustado,
    listaCaminhoNPSHAjustado,
    listaCaminhoPotenciaAjustado,
)

# salva as informações do sistema
curva1 = CurvaSistema(40, 2, 28, 0.0507, 46.8, "Aço carbono novo")
# seta a rugosidade
curva1.setRugosidade("Rugosidade Absoluta")
# obtem os dados da curva [Hm] do sistema
hmSistema = curva1.hmSistema()
NPSHd = curva1.NPSHd()


class IndexFuncionamento:
    def __init__(self, dfSistema, NPSHd):
        self.dfSistema = dfSistema
        self.NPSHd = NPSHd

    def getIndexFuncionamento(self):
        # o dfBomba é importado da pasta, enquanto o dfSistema é calculado
        # com a classe CurvaSistema
        dictFuncionamento = dict()
        for i in listaCaminhoHmAjustado:
            dfBomba = pd.read_csv(i)

            hmSistema = self.dfSistema["Hm"]
            hmBomba = dfBomba["Hm"]
            # salva o ponto de intersecção das curvas
            idx = np.argwhere(np.diff(np.sign(hmBomba - hmSistema))).flatten()
            # pega o primeiro ponto imediatamente após a intersecção
            idx = idx[0]
            if not idx:
                idx = 0
            # faz a média entre os índices para mitigar a pequena diferença
            vazaoFuncionamento = (dfBomba["Q"][idx] + self.dfSistema["Q"][idx]) / 2

            dictFuncionamento[i] = vazaoFuncionamento

        return dictFuncionamento

    def getVazaoMaxima(self):
        dictVazaoMaxima = dict()
        for i in listaCaminhoNPSHAjustado:
            # recupera os caminhos do NPSH disponível
            dfBomba = pd.read_csv(i)
            # lê os dados dentro do arquivo do caminho
            NPSHBomba = dfBomba["NPSH"]
            NPSHSistema = self.NPSHd["NPSHd"]

            idx = np.argwhere(np.diff(np.sign(NPSHSistema - NPSHBomba))).flatten()
            idx = idx[0]
            if not idx:
                idx = 0
            vazaoMaxima = self.NPSHd["Q"][idx]
            dictVazaoMaxima[i] = vazaoMaxima
            # isso se trata do valor máximo com que a bomba pode operar sem
            # cavitar
        return dictVazaoMaxima


pontoFuncionamento = IndexFuncionamento(hmSistema, NPSHd)

ponto_funcionamento_do_sistema = pontoFuncionamento.getIndexFuncionamento()
vazao_maxima_do_sistema = pontoFuncionamento.getVazaoMaxima()
