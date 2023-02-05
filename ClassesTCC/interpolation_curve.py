import numpy as np
from dfAjustados.constants import df_hm, df_NPSH, df_potencia
import pandas as pd
from curvas.CurvaSistema import CurvaSistema
import matplotlib.pyplot as plt

dict_discharge = {'diametro': '32',
                  'material': 'chumbo',
                  'temperatura': '25',
                  'alturaBomba': '10',
                  'alturaRecalque': '40',
                  'comprimentoRecalque': '50',
                  'entradaNormal': '0',
                  'entradaDeBorda': '0',
                  'curva90RaioLongo': '0',
                  'curva90RaioMedio': '3',
                  'curva90RaioCurto': '0',
                  'curva45': '2',
                  'curva90rd1': '0',
                  'registroGavetaAberto': '0',
                  'registroGloboAberto': '2',
                  'registroAnguloAberto': '0',
                  'TePassagemDireta': '0',
                  'TeSaidaLado': '0',
                  'TeSaidaBilateral': '0',
                  'valvulaPeCrivo': '0',
                  'valvulaRetencaoLeve': '0',
                  'valvulaRetencaoPesado': '0',
                  'saidaCanalizacao': '0',
                  'curva_90_rd_1_5': '0'}

dict_suction = {'diametro': '32',
                'material': 'chumbo',
                'temperatura': '25',
                'alturaReservatorio': '0',
                'alturaBomba': '10',
                'comprimentoSuccao': '20',
                'entradaNormal': '1',
                'entradaDeBorda': '0',
                'curva90RaioLongo': '0',
                'curva90RaioMedio': '0',
                'curva90RaioCurto': '0',
                'curva45': '1',
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
                'saidaCanalizacao': '0',
                'curva_90_rd_1_5': '0'}


class CurveIntersection:
    def __init__(self, df_pump, df_system, df_npsh, NPSHd, df_potencia):
        self.df_pump = df_pump
        self.df_system = df_system
        self.df_npsh = df_npsh
        self.NPSHd = NPSHd
        self.df_potencia = df_potencia

    def find_intersection(self, Q, Hm_pump, Hm_system):
        x1, x2 = np.array(Q[:-1]), np.array(Q[1:])
        y1_pump, y2_pump = np.array(Hm_pump[:-1]), np.array(Hm_pump[1:])
        y1_system, y2_system = np.array(
            Hm_system[:-1]), np.array(Hm_system[1:])

        den = (x2 - x1) * (y2_system - y1_system) - \
            (x2 - x1) * (y2_pump - y1_pump)
        mask = den != 0

        x1, x2, y1_pump, y2_pump, y1_system, y2_system, den = x1[mask], x2[
            mask], y1_pump[mask], y2_pump[mask], y1_system[mask], y2_system[mask], den[mask]

        ua = ((x2 - x1) * (y1_pump - y1_system) -
              (y2_pump - y1_pump) * (x1 - x1)) / den
        ub = ((x2 - x1) * (y2_system - y1_system) -
              (y2_pump - y1_pump) * (x2 - x1)) / den

        mask = (ua >= 0) & (ua <= 1) & (ub >= 0) & (ub <= 1)
        if mask.any():
            x_intersection = x1[mask] + ua[mask] * (x2[mask] - x1[mask])
            y_intersection = y1_pump[mask] + \
                ua[mask] * (y2_pump[mask] - y1_pump[mask])
            return x_intersection[0], y_intersection[0]
        else:
            return None, None

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
                    {'nome_bomba': name, 'Q_intersection_hm': intersection[0], 'Hm_intersection': intersection[1]})
        self.df_intersection_hm = pd.DataFrame(intersection_points)

        return self.df_intersection_hm

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
                    {'nome_bomba': name, 'Q_intersection_NPSH': intersection[0], 'NPSH_intersection': intersection[1]})

        self.df_intersection_npsh = pd.DataFrame(intersection_points)

        return self.df_intersection_npsh

    def merge_dataframes(self):
        # Merge the dataframes on the 'nome_bomba' column
        merged_df = pd.merge(self.df_intersection_hm,
                             df_intersection_npsh, on='nome_bomba')

        # Filter rows where Q_intersection_x (from df_hm) is lower than Q_intersection_y (from df_NPSH)
        filtered_df = merged_df[merged_df['Q_intersection_hm']
                                < merged_df['Q_intersection_NPSH']]

        filtered_df = filtered_df.rename(columns={
                                         'Q_intersection_hm': 'Ponto_funcionamento', 'Q_intersection_NPSH': 'Vazao_maxima'})

        # Print the resulting dataframe
        return filtered_df

    def get_eficiencia(self):
        gamma = 9790.38
        merged_df = self.merge_dataframes()
        merged_df['Ponto_funcionamento'] = merged_df['Ponto_funcionamento'].round(
            5)
        self.df_potencia['Q'] = self.df_potencia['Q'].round(5)
        self.potencia_funcionamento = pd.merge(left=merged_df, right=self.df_potencia, left_on=[
            'nome_bomba', 'Ponto_funcionamento'], right_on=['nome_bomba', 'Q'])
        self.potencia_funcionamento["Eficiencia"] = self.potencia_funcionamento["Ponto_funcionamento"] * \
            self.potencia_funcionamento["Hm_intersection"] * \
            gamma / (self.potencia_funcionamento["Potencia"]*745.7)
        return self.potencia_funcionamento

    def treat_dataset(self):
        treated_df = self.get_eficiencia()
        treated_df['Ponto_funcionamento_lpm'] = treated_df['Ponto_funcionamento']*1000*60
        treated_df['Vazao_maxima_lpm'] = treated_df['Vazao_maxima']*1000*60
        treated_df = treated_df[['nome_bomba', 'Ponto_funcionamento', 'Ponto_funcionamento_lpm',
                                 'Hm_intersection', 'Vazao_maxima', 'Vazao_maxima_lpm', 'Potencia', 'Eficiencia']]
        return treated_df


def get_float(dic, key, default=0.0):
    value = dic[key]
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


# parâmetros do sistema
material = "chumbo"
temperatura = get_float(dict_discharge, "temperatura")
altura_bomba = get_float(dict_discharge, "alturaBomba")

# parâmetros da sucção
diametro_succao = get_float(dict_suction, "diametro") / 1000
altura_reservatorio = get_float(dict_suction, "alturaReservatorio")
comprimento_succao = get_float(dict_suction, "comprimentoSuccao")

# parâmetros do recalque
diametro_recalque = get_float(dict_discharge, "diametro") / 1000
altura_recalque = get_float(dict_discharge, "alturaRecalque")
comprimento_recalque = get_float(dict_discharge, "comprimentoRecalque")


curva_recalque = CurvaSistema(
    temperatura, altura_bomba, altura_recalque, diametro_recalque, material, comprimento_recalque
)

curva_succao = CurvaSistema(
    temperatura, altura_reservatorio, altura_bomba, diametro_succao, material, comprimento_succao
)

# gets the system curve for the suction pipe and the available NPSH
df_succao, NPSHd = curva_succao.run("Rugosidade Absoluta", dict_suction)

# get the system curve for discharge pipe and a irrelevant curve
df_recalque, not_NPSHd = curva_recalque.run(
    "Rugosidade Absoluta", dict_discharge)

# gets the overall system curve
curva_sistema = pd.merge(df_succao, df_recalque, on="Q")
curva_sistema["Hm"] = curva_sistema["Hm_x"] + curva_sistema["Hm_y"]
curva_sistema = curva_sistema[["Q", "Hm"]]


intersection = CurveIntersection(
    df_hm, curva_sistema, df_NPSH, NPSHd, df_potencia)
df_intersection_hm = intersection.find_intersections_all_curves_hm()
df_intersection_npsh = intersection.find_intersections_all_curves_NPSH()
merged_df = intersection.treat_dataset()


Q_values = curva_sistema['Q']
Hm_values = curva_sistema['Hm']
Hm_bomba_csv = pd.read_csv(
    r'C:\Users\Avell 1513\Desktop\TCC I\hmsAjustados\ksb_meganorm 80-160 161 3500.csv')
Q_bomba = Hm_bomba_csv['Q']
Hm_bomba = Hm_bomba_csv['Hm']

print(merged_df)

plt.plot(Q_values, Hm_values, color='blue')
plt.plot(Q_bomba, Hm_bomba, color='red')

plt.title("Curvas genéricas")
plt.xlabel("Q (l/min)")
plt.ylabel("Hm (m.c.a.)")
plt.legend(['Curva do sistema', 'Curva da bomba'])
plt.show()
