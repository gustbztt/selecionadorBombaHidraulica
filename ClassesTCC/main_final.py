import copy

import pandas as pd
from curvas.CurvaSistema import CurvaSistema
from dfAjustados.constants import df_hm, df_NPSH, df_potencia
from flask import Flask, render_template, request, session, url_for
from interseccao.Interseccao import GetInterseccoes
from interseccao.interpolation_curve import CurveIntersection
from pretty_html_table import build_table
from dataclasses import dataclass
from interseccao.get_diametro import get_diametro_economico


app = Flask(__name__)
app.secret_key = "guti$R!@123AS!2dasfv."


def get_float(key, default=0.0):
    value = request.form.get(key)
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


@dataclass
class DadosInputs:
    def __init__(self):
        pass
    temperatura: float
    diametro_succao: int
    diametro_recalque: int
    l_succao: float
    l_recalque: float
    comprimento_total: float
    material: str
    tempo_funcionamento: float
    vazao_desejada: float
    dic_succao: dict
    diametro_succao_opc: int
    diametro_recalque_opc: int


dados = DadosInputs()


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("first.html")


@app.route(
    "/second",
    methods=[
        "POST",
    ],
)
def second():
    temperatura = get_float("temperatura")
    material = request.form.get("material")

    tempo_funcionamento = get_float("tempoFuncionamento")
    vazao_desejada = get_float("vazaoDesejada")

    dados.temperatura = temperatura
    dados.material = material
    dados.tempo_funcionamento = tempo_funcionamento
    dados.vazao_desejada = vazao_desejada

    if tempo_funcionamento != 0.0 or vazao_desejada != 0.0:
        diametro_succao, diametro_recalque = get_diametro_economico(
            dados.vazao_desejada, dados.tempo_funcionamento)

        dados.diametro_succao_opc = diametro_succao
        dados.diametro_recalque_opc = diametro_recalque

    if hasattr(dados, 'diametro_succao_opc'):
        return render_template("second.html", diametro_succao=dados.diametro_succao_opc)
    else:
        return render_template('second.html')


@app.route(
    "/third",
    methods=[
        "POST",
    ],
)
def third():
    diametro_succao = get_float("diametroSuccao") / 1000
    altura_succao = get_float('perdaSuccao')
    comprimento_succao = get_float("comprimentoTotalSuccao")

    dados.diametro_succao = diametro_succao
    dados.altura_succao = altura_succao
    dados.comprimento_succao = comprimento_succao

    dic_succao = request.form.to_dict()
    dados.dic_succao = dic_succao
    if hasattr(dados, 'diametro_recalque_opc'):
        return render_template('third.html', diametro_recalque=dados.diametro_recalque_opc)
    else:
        return render_template('third.html')


@app.route(
    "/final",
    methods=[
        "POST",
    ],
)
def final():
    diametro_recalque = get_float("diametroRecalque") / 1000
    altura_recalque = get_float('perdaRecalque')
    comprimento_recalque = get_float("comprimentoTotalRecalque")

    dados.diametro_recalque = diametro_recalque
    dados.altura_recalque = altura_recalque
    dados.comprimento_recalque = comprimento_recalque
    
    curva_succao = CurvaSistema(dados.temperatura, 0, dados.altura_succao,
                                dados.diametro_succao, dados.material, dados.comprimento_succao)

    dic_recalque = request.form.to_dict()
    curva_recalque = CurvaSistema(dados.temperatura, 0, dados.altura_recalque,
                                  dados.diametro_recalque, dados.material, dados.comprimento_recalque)

    dados.dic_recalque = dic_recalque

    NPSHd, hm_succao = curva_succao.run_succao(
        "Rugosidade Absoluta", dados.dic_succao)

    hm_recalque = curva_recalque.run_recalque(
        "Rugosidade Absoluta", dados.dic_recalque)

    hm_sistema = pd.merge(hm_succao, hm_recalque, on='Q')
    hm_sistema['Hm'] = hm_sistema['Hm_x'] + hm_sistema['Hm_y']
    hm_sistema = hm_sistema[['Q', 'Hm']]

    intersection = CurveIntersection(
        df_hm, hm_sistema, df_NPSH, NPSHd, df_potencia)
    df_intersection_hm = intersection.find_intersections_all_curves_hm()
    df_intersection_npsh = intersection.find_intersections_all_curves_NPSH()
    merged_df = intersection.treat_dataset()

    html_table_blue_light = build_table(
        merged_df, "blue_light", text_align="center", width="auto"
    )
    return f'{html_table_blue_light}, {dados.dic_succao}, {dados.dic_recalque}, {dados.material}'


app.run(debug=True)
