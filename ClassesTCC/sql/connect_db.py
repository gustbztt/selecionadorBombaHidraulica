import sqlite3


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

    def close_db(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")


class BombasHm(object):
    def __init__(self):
        self.db = Connect("bombas.db")

    def close_connection(self):
        self.db.close_db()


if __name__ == "__main__":
    bomba = BombasHm()
    bomba.close_connection()
