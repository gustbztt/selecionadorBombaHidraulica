import sys

import numpy as np
import pandas as pd

from curvas.CurvaSistema import CurvaSistema

curva1 = CurvaSistema(40, 2, 28, 0.0507, 46.8, "Aço carbono novo")
curva1.setRugosidade("Rugosidade Absoluta")
dfSistema = curva1.hmSistema()


def getIndexFuncionamento(nomeBomba, dfSistema):
    # o dfBomba é importado da pasta, enquanto o dfSistema é calculado
    #  com a classe CurvaSistema
    path = "C:\\Users\\Avell 1513\\Desktop\\TCC I\\hmsAjustados\\" + nomeBomba + ".csv"
    dfBomba = pd.read_csv(path)

    hmSistema = dfSistema["Hm"]
    hmBomba = dfBomba["Hm"]
    idx = np.argwhere(np.diff(np.sign(hmBomba - hmSistema))).flatten()
    idx = idx[0]
    if not idx:
        idx = 0
    vazaoFuncionamento = (dfBomba["Q"][idx] + dfSistema["Vazao"][idx]) / 2
    return vazaoFuncionamento, nomeBomba


print(getIndexFuncionamento("ksb_meganorm 32-250 249 3500", dfSistema))
