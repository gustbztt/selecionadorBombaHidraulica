import sqlite3
import csv
import pandas as pd


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

    def create_table(self, table_name, schema):
        try:
            self.cursor.execute(f"CREATE TABLE {table_name} ({schema})")
            print(f"Tabela {table_name} criada com sucesso.")
        except sqlite3.Error:
            print(f"Aviso: A tabela {table_name} já existe")


class BombasHm(object):
    tb_name = "bombasHm"
    schema = "id INTEGER PRIMARY KEY, nome_bomba TEXT, Q FLOAT, Hm FLOAT"

    def __init__(self, db_name):
        self.db = Connect(db_name)
        self.db.cursor.execute("DROP TABLE IF EXISTS bombasHm")

        self.db.create_table(self.tb_name, self.schema)

    def fechar_conexao(self):
        self.db.close_db()

    def inserir_de_csv(self, file_path):
        with open(file_path, 'r') as file:
            # create a CSV reader object
            reader = csv.DictReader(file)

            # iterate through each row in the CSV file
            for row in reader:
                # extract the values for the three columns
                nome_bomba = row['nome_bomba']
                Q = float(row['Q'])
                Hm = float(row['Hm'])

                # insert the values into the table
                self.db.cursor.execute(
                    "INSERT INTO bombasHm (nome_bomba, Q, Hm) VALUES (?, ?, ?)",
                    (nome_bomba, Q, Hm)
                )

        # commit changes to the database
        self.db.commit_db()
        print("Dados inseridos com sucesso!")

    def ler_todos_dados(self):
        sql = f"SELECT * from {self.tb_name}"
        r = self.db.cursor.execute(sql)
        return r.fetchall()

    def to_df(self):
        lista = self.ler_todos_dados()
        df = pd.DataFrame(lista)
        return df


class BombasNPSH(object):
    tb_name = "bombasNPSH"
    schema = "id INTEGER PRIMARY KEY, nome_bomba TEXT, Q FLOAT, NPSH FLOAT"

    def __init__(self, db_name):
        self.db = Connect(db_name)
        self.db.cursor.execute("DROP TABLE IF EXISTS bombasNPSH")

        self.db.create_table(self.tb_name, self.schema)

    def fechar_conexao(self):
        self.db.close_db()

    def inserir_de_csv(self, file_path):
        with open(file_path, 'r') as file:
            # create a CSV reader object
            reader = csv.DictReader(file)

            # iterate through each row in the CSV file
            for row in reader:
                # extract the values for the three columns
                nome_bomba = row['nome_bomba']
                Q = float(row['Q'])
                NPSH = float(row['NPSH'])

                # insert the values into the table
                self.db.cursor.execute(
                    "INSERT INTO bombasNPSH (nome_bomba, Q, NPSH) VALUES (?, ?, ?)",
                    (nome_bomba, Q, NPSH)
                )

        # commit changes to the database
        self.db.commit_db()
        print("Dados inseridos com sucesso!")

    def ler_todos_dados(self):
        sql = f"SELECT * from {self.tb_name}"
        r = self.db.cursor.execute(sql)
        return r.fetchall()

    def to_df(self):
        lista = self.ler_todos_dados()
        df = pd.DataFrame(lista)
        return df


class BombasPotencia(object):
    tb_name = "bombasPotencia"
    schema = "id INTEGER PRIMARY KEY, nome_bomba TEXT, Q FLOAT, Potencia FLOAT"

    def __init__(self, db_name):
        self.db = Connect(db_name)
        self.db.cursor.execute("DROP TABLE IF EXISTS bombasPotencia")

        self.db.create_table(self.tb_name, self.schema)

    def fechar_conexao(self):
        self.db.close_db()

    def inserir_de_csv(self, file_path):
        with open(file_path, 'r') as file:
            # create a CSV reader object
            reader = csv.DictReader(file)

            # iterate through each row in the CSV file
            for row in reader:
                # extract the values for the three columns
                nome_bomba = row['nome_bomba']
                Q = float(row['Q'])
                Potencia = float(row['Potencia'])

                # insert the values into the table
                self.db.cursor.execute(
                    "INSERT INTO bombasPotencia (nome_bomba, Q, Potencia) VALUES (?, ?, ?)",
                    (nome_bomba, Q, Potencia)
                )

        # commit changes to the database
        self.db.commit_db()
        print("Dados inseridos com sucesso!")

    def ler_todos_dados(self):
        sql = f"SELECT * from {self.tb_name}"
        r = self.db.cursor.execute(sql)
        return r.fetchall()

    def to_df(self):
        lista = self.ler_todos_dados()
        df = pd.DataFrame(lista)
        return df


if __name__ == "__main__":
    db_name = "mydatabase.db"
    bombaHm = BombasHm(db_name)
    bombaHm.inserir_de_csv(
        "C:\\Users\\Avell 1513\\Desktop\\TCC I\\JSON bombas\\bombasHm.csv")
    bombaHm.fechar_conexao()

if __name__ == "__main__":
    db_name = "mydatabase.db"
    bombaNPSH = BombasNPSH(db_name)
    bombaNPSH.inserir_de_csv(
        "C:\\Users\\Avell 1513\\Desktop\\TCC I\\JSON bombas\\bombasNPSH.csv")
    bombaNPSH.fechar_conexao()

if __name__ == "__main__":
    db_name = "mydatabase.db"
    bombaPotencia = BombasPotencia(db_name)
    bombaPotencia.inserir_de_csv(
        "C:\\Users\\Avell 1513\\Desktop\\TCC I\\JSON bombas\\bombasPotencia.csv")
    bombaPotencia.fechar_conexao()
