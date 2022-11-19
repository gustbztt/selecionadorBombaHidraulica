import copy

from flask import Flask, flash, redirect, render_template, request, session, url_for

from curvas.CurvaSistema import CurvaSistema
from dfAjustados.constants import df_hm, df_NPSH, df_potencia
from interseccao.Interseccao import GetInterseccoes

app = Flask(__name__)
app.secret_key = "guti"


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

    temperatura = request.form.get("temperatura")
    temperatura = float(temperatura)

    diametro1 = request.form.get("diametro")
    diametro = copy.deepcopy(diametro1)
    diametro = float(diametro)
    diametro_funcao = diametro / 1000

    material = request.form.get("material")

    lSuccao = request.form.get("perdaSuccao")
    lSuccao = float(lSuccao)

    lRecalque = request.form.get("perdaRecalque")
    lRecalque = float(lRecalque)

    dic = request.form.to_dict()

    curva1 = CurvaSistema(temperatura, lSuccao, lRecalque, diametro_funcao, material)
    curva1.setRugosidade("Rugosidade Absoluta")
    curva1.setDensidade()
    curva1.setViscosidade()
    curva1.calculaPerda(dic)
    df_sistema = curva1.hmSistema()
    NPSHd = curva1.NPSHd()

    interseccoes = GetInterseccoes(df_sistema, NPSHd, df_hm, df_NPSH, df_potencia)
    ponto_funcionamento = interseccoes.get_ponto_funcionamento()
    potencia_efetiva = interseccoes.get_potencia_efetiva()
    eficiencia = interseccoes.get_eficiencia()
    vazao_maxima = interseccoes.get_vazao_maxima()

    ponto_funcionamento = ponto_funcionamento.to_html()
    eficiencia = eficiencia.to_html()

    return f"{eficiencia}"


app.run(debug=True)
