import sqlite3
from pathlib import Path

#NOTE:Caminho do arquivo do banco de dados (ficará na raiz do projeto)
DB_PATH = Path(__file__).resolve().parent.parent / "sys_bank.db"


def get_connection():
    #NOTE: Cria (ou abre) uma conexão com o banco de dados SQLite.
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
    return conn


def init_db():
    #NOTE: Inicializa o banco de dados com o schema básico.
    schema = """
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE NOT NULL,
        data_nascimento TEXT,
        endereco TEXT,
        tipo_cliente TEXT NOT NULL DEFAULT 'PF'
    );

    CREATE TABLE IF NOT EXISTS contas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero INTEGER NOT NULL,
        agencia TEXT NOT NULL DEFAULT '0001',
        saldo REAL NOT NULL DEFAULT 0,
        limite REAL DEFAULT 500,
        limite_saques INTEGER DEFAULT 3,
        limite_transacoes INTEGER DEFAULT 10,
        cliente_id INTEGER NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    );

    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        valor REAL NOT NULL,
        data_hora TEXT NOT NULL DEFAULT (datetime('now')),
        conta_id INTEGER NOT NULL,
        FOREIGN KEY (conta_id) REFERENCES contas(id)
    );
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()


def reset_db():
    """Apaga todas as tabelas e recria o schema (útil para testes)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
    DROP TABLE IF EXISTS transacoes;
    DROP TABLE IF EXISTS contas;
    DROP TABLE IF EXISTS clientes;
    """)
    conn.commit()
    conn.close()
    init_db()


# =========================================================
# CRUD - CLIENTES
# =========================================================
def insert_cliente(nome, cpf, data_nascimento, endereco, tipo_cliente="PF"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, cpf, data_nascimento, endereco, tipo_cliente)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, cpf, data_nascimento, endereco, tipo_cliente))
    conn.commit()
    conn.close()


def get_cliente_by_cpf(cpf):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE cpf = ?", (cpf,))
    cliente = cursor.fetchone()
    conn.close()
    return cliente


def listar_clientes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_cliente(cpf):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE cpf = ?", (cpf,))
    conn.commit()
    conn.close()


# =========================================================
# CRUD - CONTAS
# =========================================================
def insert_conta(numero, cliente_id, agencia="0001", saldo=0, limite=500, limite_saques=3, limite_transacoes=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contas (numero, agencia, saldo, limite, limite_saques, limite_transacoes, cliente_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (numero, agencia, saldo, limite, limite_saques, limite_transacoes, cliente_id))
    conn.commit()
    conn.close()


def get_contas_by_cliente(cliente_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contas WHERE cliente_id = ?", (cliente_id,))
    contas = cursor.fetchall()
    conn.close()
    return contas


def listar_contas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contas")
    rows = cursor.fetchall()
    conn.close()
    return rows


# =========================================================
# CRUD - TRANSAÇÕES
# =========================================================
def insert_transacao(tipo, valor, conta_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transacoes (tipo, valor, conta_id)
        VALUES (?, ?, ?)
    """, (tipo, valor, conta_id))
    conn.commit()
    conn.close()


def get_transacoes_by_conta(conta_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacoes WHERE conta_id = ? ORDER BY data_hora ASC", (conta_id,))
    transacoes = cursor.fetchall()
    conn.close()
    return transacoes


def listar_transacoes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacoes ORDER BY data_hora DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


# =========================================================
# MAIN - inicialização
# =========================================================
if __name__ == "__main__":
    print("Inicializando banco de dados...")
    reset_db()
    print("Banco de dados pronto em:", DB_PATH)

    # Dados de exemplo
    insert_cliente("Gabriel Barbosa", "123.456.789-00", "1990-01-01", "Rua A, 123 - Centro - Cidade/UF")
    cliente = get_cliente_by_cpf("123.456.789-00")
    insert_conta(1, cliente["id"])
    insert_transacao("Deposito", 1000.00, 1)

    print("Clientes:", listar_clientes())
    print("Contas:", listar_contas())
    print("Transações:", listar_transacoes())
