import csv
import datetime
import io
import os
import sqlite3

import pandas as pd

# import names


class Connect(object):
    def __init__(self, db_name):
        try:
            # conectando
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            # imprimindo nome do banco
            print(f"Banco: {db_name}")
            # lendo a versão do SQLite
            self.cursor.execute("SELECT SQLITE_VERSION()")
            self.data = self.cursor.fetchone()
            # imprimindo a versão do SQLite
            print(f"SQLite version: {self.data}")
        except sqlite3.Error:
            print("Erro ao abrir banco.")
            return False

    def commit_db(self):
        if self.conn:
            self.conn.commit()

    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")


class BombasHm(object):
    tb_name = "bombasHm"

    def __init__(self):
        self.db = Connect("bombas.db")
        self.tb_name

    def fechar_conexao(self):
        self.db.close_db()

    def criar_schema(self, schema_name="G:\\Scripts_Python\\create_schemaHm.sql"):
        print(f"Criando tabela {self.tb_name}")

        try:
            with open(schema_name, "rt") as f:
                schema = f.read()
                self.db.cursor.executescript(schema)

        except sqlite3.Error:
            print(f"Aviso: A tabela {self.tb_name} já existe")
            return False

    def inserir_de_csv(
        self,
        file_name="C:\\Users\\Avell 1513\\Desktop\\TCC I\\JSON bombas\\bombasHm.csv",
    ):
        try:
            reader = csv.reader(open(file_name, "rt"), delimiter=";")
            linha = (reader,)
            self.db.cursor.execute("""DELETE from bombasHm""")
            for linha in reader:
                self.db.cursor.execute(
                    """
                INSERT INTO bombasHm (nome_bomba, Q, Hm)
                VALUES (?,?,?)""",
                    linha,
                )

            # gravando no bd
            self.db.commit_db()
            print("Dados importados do csv com sucesso.")

        except sqlite3.IntegrityError:
            print("Não conseguiu importar o csv")
            return

    def ler_todos_dados(self):
        sql = "SELECT * from bombasHm"
        r = self.db.cursor.execute(sql)
        return r.fetchall()

    def to_df(self):
        lista = self.ler_todos_dados()
        df = pd.DataFrame(lista)
        return df


class BombasNPSH(object):
    tb_name = "bombasNPSH"

    def __init__(self):
        self.db = Connect("bombas.db")
        self.tb_name

    def fechar_conexao(self):
        self.db.close_db()

    def criar_schema(self, schema_name="G:\\Scripts_Python\\create_schema_NPSH.sql"):
        print(f"Criando tabela {self.tb_name}")

        try:
            with open(schema_name, "rt") as f:
                schema = f.read()
                self.db.cursor.executescript(schema)

        except sqlite3.Error:
            print(f"Aviso: A tabela {self.tb_name} já existe")
            return False

    def inserir_de_csv(
        self,
        file_name="C:\\Users\\Avell 1513\\Desktop\\TCC I\\JSON bombas\\bombasNPSH.csv",
    ):
        try:
            reader = csv.reader(open(file_name, "rt"), delimiter=";")
            linha = (reader,)
            self.db.cursor.execute("""DELETE from bombasNPSH""")
            for linha in reader:
                self.db.cursor.execute(
                    """
                INSERT INTO bombasNPSH (nome_bomba, Q, NPSH)
                VALUES (?,?,?)""",
                    linha,
                )

            # gravando no bd
            self.db.commit_db()
            print("Dados importados do csv com sucesso.")

        except sqlite3.IntegrityError:
            print("Não conseguiu importar o csv")
            return

    def ler_todos_dados(self):
        sql = "SELECT * from bombasNPSH"
        r = self.db.cursor.execute(sql)
        return r.fetchall()

    def to_df(self):
        lista = self.ler_todos_dados()
        df = pd.DataFrame(lista)
        return df


class BombasPotencia(object):
    tb_name = "bombasPotencia"

    def __init__(self):
        self.db = Connect("bombas.db")
        self.tb_name

    def fechar_conexao(self):
        self.db.close_db()

    def criar_schema(
        self, schema_name="G:\\Scripts_Python\\create_schema_potencia.sql"
    ):
        print(f"Criando tabela {self.tb_name}")

        try:
            with open(schema_name, "rt") as f:
                schema = f.read()
                self.db.cursor.executescript(schema)

        except sqlite3.Error:
            print(f"Aviso: A tabela {self.tb_name} já existe")
            return False

    def inserir_de_csv(
        self,
        file_name="C:\\Users\\Avell 1513\\Desktop\\TCC I\\JSON bombas\\bombasPotencia.csv",
    ):
        try:
            reader = csv.reader(open(file_name, "rt"), delimiter=";")
            linha = (reader,)
            self.db.cursor.execute("""DELETE from bombasPotencia""")
            for linha in reader:
                self.db.cursor.execute(
                    """
                INSERT INTO bombasPotencia (nome_bomba, Q, Potencia)
                VALUES (?,?,?)""",
                    linha,
                )

            # gravando no bd
            self.db.commit_db()
            print("Dados importados do csv com sucesso.")

        except sqlite3.IntegrityError:
            print("Não conseguiu importar o csv")
            return

    def ler_todos_dados(self):
        sql = "SELECT * from bombasPotencia"
        r = self.db.cursor.execute(sql)
        return r.fetchall()

    def to_df(self):
        lista = self.ler_todos_dados()
        df = pd.DataFrame(lista)
        return df


'''class TabelaPerdas(object):
    tb_name = "tabelaPerdas"

    def __init__(self):
        self.db = Connect("bombas.db")
        self.tb_name

    def fechar_conexao(self):
        self.db.close_db()

    def criar_schema(self, schema_name="G:\\Scripts_Python\\create_schema_perdas.sql"):
        print(f"Criando tabela {self.tb_name}")

        try:
            with open(schema_name, "rt") as f:
                schema = f.read()
                self.db.cursor.executescript(schema)

        except sqlite3.Error:
            print(f"Aviso: A tabela {self.tb_name} já existe")
            return False

    def inserir_de_csv(
        self,
        file_name="C:\\Users\\Avell 1513\\Desktop\\TCC I\\JSON bombas\\tabelaPerdas.csv",
    ):
        try:
            reader = csv.reader(open(file_name, "rt"), delimiter=";")
            linha = (reader,)
            # self.db.cursor.execute("""DELETE from tabelaPerdas""")
            for linha in reader:
                self.db.cursor.execute(
                    """
                INSERT INTO tabelaPerdas (`diâmetro (mm)`,
                `diâmetro (pol)`,
                `curva 90º raio longo`,
                `curva 90° raio médio`,
                `curva 90º raio curto`,
                `curva 45°`,
                `curva 90º R/D 1 1/2`,
                `curva 90° r/d 1`,
                `curva 45°2`,
                `entrada normal`,
                `entrada de borda`,
                `registro de gaveta aberto`,
                `registro de globo aberto`,
                `registro de ângulo aberto`,
                `tê passagem direta`,
                `tê saída de lado`,
                `tê saída bilateral`,
                `válvula de pé e crivo`,
                `saída da canalização`,
                `válvula de retenção tipo leve`,
                `válvula de retenção tipo pesado`)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    linha,
                )

            # gravando no bd
            self.db.commit_db()
            print("Dados importados do csv com sucesso.")

        except sqlite3.IntegrityError:
            print("Não conseguiu importar o csv")
            return

    def ler_todos_dados(self):
        sql = "SELECT * from tabelaPerdas"
        r = self.db.cursor.execute(sql)
        return r.fetchall()

    def to_df(self):
        lista = self.ler_todos_dados()
        df = pd.DataFrame(lista)
        return df
'''

hm = BombasHm()
hm.criar_schema()
hm.inserir_de_csv()
dfHm = hm.to_df()

npsh = BombasNPSH()
npsh.criar_schema()
npsh.inserir_de_csv()
dfNPSH = npsh.to_df()

potencia = BombasPotencia()
potencia.criar_schema()
potencia.inserir_de_csv()
dfPotencia = potencia.to_df()

'''perdas = TabelaPerdas()
perdas.criar_schema()
perdas.inserir_de_csv()
dfperdas = perdas.to_df()
'''
