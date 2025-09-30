
import sqlite3
import os
from pathlib import Path

#NOTE:Caminho do arquivo do banco de dados (ficará na raiz do projeto)
DB_FILE = Path(__file__).resolve().parent / "sys_bank.db"


class DatabaseManager:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """Abre e retorna uma conexão com o banco de dados."""
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def close(self):
        """Fecha conexão se estiver aberta."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=(), commit=False):
        """Executa uma query genérica."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        if commit:
            conn.commit()
        return cursor



    def create_schema(self):
        #NOTE:Cria as tabelas iniciais no banco, se não existirem.
        self.connect()
        schema_sql = """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            data_nascimento DATE,
            endereco TEXT,
            tipo_cliente TEXT CHECK(tipo_cliente IN ('PF', 'PJ')) DEFAULT 'PF',
            email TEXT UNIQUE,
            telefone TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            numero INTEGER UNIQUE NOT NULL,
            agencia TEXT NOT NULL DEFAULT '0001',
            tipo TEXT NOT NULL CHECK(tipo IN ('corrente', 'poupanca')),
            saldo REAL DEFAULT 0.0,
            limite REAL DEFAULT 500.0,
            limite_saques INTEGER DEFAULT 3,
            limite_transacoes INTEGER DEFAULT 10,
            ativa INTEGER DEFAULT 1,
            data_abertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conta_id INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('deposito', 'saque', 'transferencia')),
            valor REAL NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conta_id) REFERENCES contas(id)
        );
        """
        self.connect().cursor().executescript(schema_sql) 
        self.connection.commit()

    def reset_db(self):
        """Apaga e recria o banco de dados do zero."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.create_schema()
        print(f"Banco de dados resetado e pronto em: {self.db_path}")

    # --- MÉTODOS CRUD (AGORA DENTRO DA CLASSE) ---
    def insert_cliente(self, nome, cpf, data_nascimento, endereco):
        query = "INSERT INTO clientes (nome, cpf, data_nascimento, endereco) VALUES (?, ?, ?, ?)"
        self.execute_query(query, (nome, cpf, data_nascimento, endereco), commit=True)

    def get_cliente_by_cpf(self, cpf):
        query = "SELECT * FROM clientes WHERE cpf = ?"
        cursor = self.execute_query(query, (cpf,))
        return cursor.fetchone()

    def insert_conta(self, cliente_id, numero, tipo, saldo=0.0):
        query = "INSERT INTO contas (cliente_id, numero, tipo, saldo) VALUES (?, ?, ?, ?)"
        self.execute_query(query, (cliente_id, numero, tipo, saldo), commit=True)

    def insert_transacao(self, conta_id, tipo, valor):
        query = "INSERT INTO transacoes (conta_id, tipo, valor) VALUES (?, ?, ?)"
        self.execute_query(query, (conta_id, tipo, valor), commit=True)

    def listar_todos(self, tabela):
        query = f"SELECT * FROM {tabela}"
        cursor = self.execute_query(query)
        return cursor.fetchall()

    def get_contas_by_cliente(self, cliente_id):
        query = "SELECT * FROM contas WHERE cliente_id = ?"
        cursor = self.execute_query(query, (cliente_id,))
        return cursor.fetchall()

    def get_transacoes_by_conta(self, conta_id):
        query = "SELECT * FROM transacoes WHERE conta_id = ? ORDER BY data_hora DESC"
        cursor = self.execute_query(query, (conta_id,))
        return cursor.fetchall()

    def atualizar_saldo(self, conta_id, novo_saldo):
        query = "UPDATE contas SET saldo = ? WHERE id = ?"
        self.execute_query(query, (novo_saldo, conta_id), commit=True)

    def listar_contas_com_clientes(self):
        query = """
            SELECT
                c.agencia,
                c.numero,
                cl.nome AS titular
            FROM contas c
            JOIN clientes cl ON c.cliente_id = cl.id
            WHERE c.ativa = 1"""
        cursor = self.execute_query(query)
        return cursor.fetchall()


# =========================================================
# MAIN - inicialização
# =========================================================
if __name__ == "__main__":
    db = DatabaseManager()  # Instancia o gerenciador UMA VEZ
    db.reset_db()           # Reseta e cria o schema

    # Dados de exemplo
    print("\nInserindo dados de exemplo...")
    db.insert_cliente("Gabriel Barbosa", "123.456.789-00", "1996-08-30", "Ninho do Urubu, RJ")
    
    cliente = db.get_cliente_by_cpf("123.456.789-00")
    if cliente:
        db.insert_conta(cliente["id"], numero=1010, tipo="corrente", saldo=5000)
        db.insert_transacao(conta_id=1, tipo="deposito", valor=5000)
    
    print("Dados inseridos com sucesso!")

    # Listando os resultados
    print("\n--- Clientes Cadastrados ---")
    for cliente in db.listar_todos("clientes"):
        print(dict(cliente))

    print("\n--- Contas Abertas ---")
    for conta in db.listar_todos("contas"):
        print(dict(conta))

    print("\n--- Últimas Transações ---")
    for transacao in db.listar_todos("transacoes"):
        print(dict(transacao))
        
    db.close() # Fecha a conexão no final de tudo
