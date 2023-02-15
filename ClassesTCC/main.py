import copy

from curvas.CurvaSistema import CurvaSistema
from dfAjustados.constants import df_hm, df_NPSH, df_potencia
from flask import Flask, flash, redirect, render_template, request, session, url_for
from interseccao.Interseccao import GetInterseccoes
from pretty_html_table import build_table

app = Flask(__name__)
app.secret_key = "guti$R!@123AS!2dasfv."

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route(
    "/felipe",
    methods=[
        "POST",
    ],
)
def felipe():
    def get_float(key, default=0.0):
        value = request.form.get(key)
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    temperatura = get_float("temperatura")
    diametro = get_float("diametro") / 1000
    l_succao = get_float("perdaSuccao")
    l_recalque = get_float("perdaRecalque")
    comprimento_total = get_float("comprimentoTotal")
    material = request.form.get("material")

    dic = request.form.to_dict()

    curva1 = CurvaSistema(
        temperatura, l_succao, l_recalque, diametro, material, comprimento_total
    )
    df_sistema, NPSHd = curva1.run("Rugosidade Absoluta", dic)

    interseccoes = GetInterseccoes(
        df_sistema, NPSHd, df_hm, df_NPSH, df_potencia)
    output = interseccoes.run()
    html_table_blue_light = build_table(
        output, "blue_light", text_align="center", width="auto"
    )

    return f"{html_table_blue_light}"


app.run(debug=True)
