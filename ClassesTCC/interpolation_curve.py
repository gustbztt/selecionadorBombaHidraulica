import numpy as np
from dfAjustados.constants import df_hm, df_NPSH, df_potencia
import pandas as pd
from curvas.CurvaSistema import CurvaSistema


dic = {'diametro': '100',
       'material': 'chumbo',
       'temperatura': '25',
       'perdaSuccao': '10',
       'perdaRecalque': '100',
       'comprimentoTotal': '125',
       'entradaNormal': '0',
       'entradaDeBorda': '1',
       'curva90RaioLongo': '0',
       'curva90RaioMedio': '0',
       'curva90RaioCurto': '0',
       'curva45': '2',
       'curva90rd1': '0',
       'registroGavetaAberto': '0',
       'registroGloboAberto': '2',
       'registroAnguloAberto': '0',
       'TePassagemDireta': '0',
       'TeSaidaLado': '0',
       'TeSaidaBilateral': '0',
       'valvulaPeCrivo': '1',
       'valvulaRetencaoLeve': '0',
       'valvulaRetencaoPesado': '0',
       'saidaCanalizacao': '1',
       'curva_90_rd_1_5': '0'}


def get_float(key, default=0.0):
    value = dic[key]
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


temperatura = get_float("temperatura")
diametro = get_float("diametro") / 1000
l_succao = get_float("perdaSuccao")
l_recalque = get_float("perdaRecalque")
comprimento_total = get_float("comprimentoTotal")
material = "chumbo"

curva1 = CurvaSistema(
    temperatura, l_succao, l_recalque, diametro, material, comprimento_total
)

df_system, NPSHd = curva1.run("Rugosidade Absoluta", dic)
df_pump = df_hm


class CurveIntersection:
    def __init__(self, df_pump, df_system, df_npsh, NPSHd):
        self.df_pump = df_pump
        self.df_system = df_system
        self.df_npsh = df_npsh
        self.NPSHd = NPSHd

    def find_intersection(self, Q, Hm_pump, Hm_system):
        x_intersection = None
        y_intersection = None
        for i in range(len(Q) - 1):
            x1, x2 = Q[i], Q[i+1]
            y1_pump, y2_pump = Hm_pump[i], Hm_pump[i+1]
            y1_system, y2_system = Hm_system[i], Hm_system[i+1]
            den = (x2 - x1) * (y2_system - y1_system) - \
                (x2 - x1) * (y2_pump - y1_pump)
            if den == 0:
                continue
            # Use linear interpolation to estimate the intersection point
            ua = ((x2 - x1) * (y1_pump - y1_system) -
                  (y2_pump - y1_pump) * (x1 - x1)) / den
            ub = ((x2 - x1) * (y2_system - y1_system) -
                  (y2_pump - y1_pump) * (x2 - x1)) / den

            # Check if the intersection point is within the segment of both curves
            if 0 <= ua <= 1 and 0 <= ub <= 1:
                x_intersection = x1 + ua * (x2 - x1)
                y_intersection = y1_pump + ua * (y2_pump - y1_pump)
                break

        return x_intersection, y_intersection

    def find_intersections_all_curves_hm(self):
        self.df_pump = self.df_pump.sort_values('Q')
        self.merged_df = pd.merge_asof(
            self.df_pump, self.df_system, on='Q', tolerance=1e-6)
        intersection_points = []
        for name, group in self.merged_df.groupby('nome_bomba'):
            Q = group['Q'].values
            Hm_pump = group['Hm_x'].values
            Hm_system = group['Hm_y'].values
            intersection = self.find_intersection(Q, Hm_pump, Hm_system)
            if intersection[0] is not None:
                intersection_points.append(
                    {'nome_bomba': name, 'Q_intersection': intersection[0], 'Hm_intersection': intersection[1]})
        return intersection_points

    def find_intersections_all_curves_NPSH(self):
        self.df_npsh = self.df_npsh.sort_values('Q')
        self.merged_df = pd.merge_asof(
            self.df_npsh, self.NPSHd, on='Q', tolerance=1e-6)
        intersection_points = []
        for name, group in self.merged_df.groupby('nome_bomba'):
            Q = group['Q'].values
            NPSH_pump = group['NPSH'].values
            NPSH_system = group['NPSHd'].values
            intersection = self.find_intersection(Q, NPSH_pump, NPSH_system)
            if intersection[0] is not None:
                intersection_points.append(
                    {'nome_bomba': name, 'Q_intersection': intersection[0], 'NPSH_intersection': intersection[1]})
        return intersection_points


df_npsh = df_NPSH

intersection = CurveIntersection(df_pump, df_system, df_npsh, NPSHd)
intersection_points_hm = intersection.find_intersections_all_curves_hm()
intersection_points_npsh = intersection.find_intersections_all_curves_NPSH()

print(intersection_points_hm)
print(intersection_points_npsh)
