from glob import glob

"""
esse arquivo tem a função de armazenar constantes que serão usadas
posteriormente no código.
"""


# folderPath é o caminho onde estão armazenados os dados desejados

folderPath = "C:\\Users\\Avell 1513\\Desktop\\TCC I\\"

# nome das pastas finais
hmFolder = "Gráficos das bombasHm_teste"
NPSHFolder = "Gráficos das bombasNPSH_teste"
potenciaFolder = "Gráficos das bombasPotencia_teste"
listaCaminhoHm = []  # type: list[str]
listaCaminhoNPSH = []  # type: list[str]
listaCaminhoPotencia = []  # type: list[str]


# utilizar uma única função (esperar aux. de branch)
caminhoHm = glob(folderPath + hmFolder + "\\*.csv")
for i in caminhoHm:
    arquivo = i.replace("\\", "/")
    listaCaminhoHm.append(arquivo)

caminhoNPSH = glob(folderPath + NPSHFolder + "\\*.csv")
for i in caminhoNPSH:
    arquivo = i.replace("\\", "/")
    listaCaminhoNPSH.append(arquivo)

caminhoPotencia = glob(folderPath + potenciaFolder + "\\*.csv")
for i in caminhoPotencia:
    arquivo = i.replace("\\", "/")
    listaCaminhoPotencia.append(arquivo)

listaCaminhoHmAjustado = []  # type: list[str]
for i in listaCaminhoHm:
    a = i.replace(hmFolder, "hmsAjustados")
    listaCaminhoHmAjustado.append(a)

listaCaminhoNPSHAjustado = []  # type: list[str]
for i in listaCaminhoNPSH:
    a = i.replace(NPSHFolder, "NPSHsAjustados")
    listaCaminhoNPSHAjustado.append(a)

listaCaminhoPotenciaAjustado = []  # type: list[str]
for i in listaCaminhoPotencia:
    a = i.replace(potenciaFolder, "PotenciasAjustados")
    listaCaminhoPotenciaAjustado.append(a)

listaCaminhoHm.sort()
listaCaminhoHmAjustado.sort()
listaCaminhoNPSH.sort()
listaCaminhoNPSHAjustado.sort()
listaCaminhoPotencia.sort()
listaCaminhoPotenciaAjustado.sort()
