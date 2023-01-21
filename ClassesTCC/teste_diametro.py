import copy

import pandas as pd
from curvas.CurvaSistema import CurvaSistema
from dfAjustados.constants import df_hm, df_NPSH, df_potencia
from interseccao.Interseccao import GetInterseccoes

dic = {
    "diametro": "25",
    "material": "chumbo",
    "temperatura": "30",
    "perdaSuccao": "2",
    "perdaRecalque": "20",
    "comprimentoTotal": "30",
    "entradaNormal": "1",
    "entradaDeBorda": "1",
    "curva90RaioLongo": "0",
    "curva90RaioMedio": "3",
    "curva90RaioCurto": "0",
    "curva45": "0",
    "curva90rd1": "0",
    "registroGavetaAberto": "0",
    "registroGloboAberto": "0",
    "registroAnguloAberto": "0",
    "TePassagemDireta": "3",
    "TeSaidaLado": "0",
    "TeSaidaBilateral": "0",
    "valvulaPeCrivo": "1",
    "valvulaRetencaoLeve": "0",
    "valvulaRetencaoPesado": "1",
    "saidaCanalizacao": "1",
    "curva_90_rd_1_5": "0",
}


temperatura = dic.get("temperatura")
temperatura = float(temperatura)

diametro1 = dic.get("diametro")
diametro = copy.deepcopy(diametro1)
diametro = float(diametro)
diametro_funcao = diametro / 1000

material = dic.get("material")

lSuccao = dic.get("perdaSuccao")
lSuccao = float(lSuccao)

lRecalque = dic.get("perdaRecalque")
lRecalque = float(lRecalque)

comprimentoTotal = dic.get("comprimentoTotal")
comprimentoTotal = float(comprimentoTotal)

curva1 = CurvaSistema(
    temperatura, lSuccao, lRecalque, diametro_funcao, material, comprimentoTotal
)
curva1.set_rugosidade("Rugosidade Absoluta")
curva1.set_densidade()
curva1.set_viscosidade()
curva1.calcula_perda(dic)
df_sistema = curva1.hmSistema()
NPSHd = curva1.NPSHd()

interseccoes = GetInterseccoes(df_sistema, NPSHd, df_hm, df_NPSH, df_potencia)
ponto_funcionamento = interseccoes.get_ponto_funcionamento()
potencia_efetiva = interseccoes.get_potencia_efetiva()
eficiencia = interseccoes.get_eficiencia()
vazao_maxima = interseccoes.get_vazao_maxima()
teste = interseccoes.check_cavitation()


df_sistema.to_csv()
