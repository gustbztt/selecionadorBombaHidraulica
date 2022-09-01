import sys

import numpy as np
import pandas as pd

from curvas.CurvaSistema import CurvaSistema
from dfAjustados.constants import (
    listaCaminhoHmAjustado,
    listaCaminhoNPSHAjustado,
    listaCaminhoPotenciaAjustado,
)

curva1 = CurvaSistema(40, 2, 28, 0.0507, 46.8, "Aço carbono novo")
curva1.setRugosidade("Rugosidade Absoluta")
dfSistema = curva1.hmSistema()


class IndexFuncionamento:
    def __init__(self, dfSistema):
        self.dfSistema = dfSistema

    def getIndexFuncionamento(self):
        # o dfBomba é importado da pasta, enquanto o dfSistema é calculado
        #  com a classe CurvaSistema
        dfFuncionamento = []
        for i in listaCaminhoHmAjustado:
            dfBomba = pd.read_csv(i)
            hmSistema = self.dfSistema["Hm"]
            hmBomba = dfBomba["Hm"]
            idx = np.argwhere(np.diff(np.sign(hmBomba - hmSistema))).flatten()
            idx = idx[0]
            if not idx:
                idx = 0
            vazaoFuncionamento = (dfBomba["Q"][idx] + self.dfSistema["Q"][idx]) / 2
            dfFuncionamento.append(vazaoFuncionamento)
            dfFuncionamento.append(i)

        return dfFuncionamento


a = IndexFuncionamento(dfSistema)

print(a.getIndexFuncionamento())
