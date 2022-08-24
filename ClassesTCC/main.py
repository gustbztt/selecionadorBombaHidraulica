from flask import Flask, flash, redirect, render_template, request, session, url_for

from curvas.CurvaSistema import CurvaSistema

app = Flask(__name__)
app.secret_key = "stephanjanoski"


@app.route("/")
def index():
    return render_template("index.html")


@app.route(
    "/criar",
    methods=[
        "GET",
    ],
)
def criar():
    temperatura = request.args.get["temperatura"]
    viscosidade = request.args.get["viscosidade"]
    alturaInicial = request.args.get["alturaInicial"]
    alturaFinal = request.args.get["alturaFinal"]
    diametro = request.args.get["diametro"]
    material = request.args.get["material"]
    curva1 = CurvaSistema(
        temperatura, alturaInicial, alturaFinal, diametro, 50, material
    )
    return print(curva1)
    return render_template()


app.run(debug=True)
