
import pytest
from sys_bank.services import database_manager as db



@pytest.fixture(scope="module", autouse=True)
def setup_db():
    #NOTE:
    # Fixture que roda antes de cada teste:
    # - Reseta o banco de dados
    # - Garante que as tabelas estão criadas
    db.reset_db()
    yield
    db.reset_db()


   # =========================================================
# Testes para Clientes
# =========================================================
def test_insert_and_get_cliente():
    db.insert_cliente("Gabriel Barbosa", "123.456.789-00", "1990-01-01", "Rua A, 123", "PF")
    cliente = db.get_cliente_by_cpf("123.456.789-00")

    assert cliente is not None
    assert cliente["nome"] == "Gabriel Barbosa"
    assert cliente["cpf"] == "123.456.789-00"


def test_listar_clientes():
    db.insert_cliente("Maria Silva", "111.222.333-44", "1985-05-05", "Av. B, 456", "PF")
    db.insert_cliente("João Souza", "555.666.777-88", "1970-07-07", "Rua C, 789", "PF")

    clientes = db.listar_clientes()
    assert len(clientes) == 2


def test_delete_cliente():
    db.insert_cliente("Carlos Pereira", "999.888.777-66", "1995-03-15", "Rua X, 101", "PF")
    db.delete_cliente("999.888.777-66")

    cliente = db.get_cliente_by_cpf("999.888.777-66")
    assert cliente is None


# =========================================================
# Testes para Contas
# =========================================================
def test_insert_and_get_conta():
    db.insert_cliente("Alice", "222.333.444-55", "2000-09-09", "Rua Y, 202", "PF")
    cliente = db.get_cliente_by_cpf("222.333.444-55")

    db.insert_conta(123, cliente["id"])
    contas = db.get_contas_by_cliente(cliente["id"])

    assert len(contas) == 1
    assert contas[0]["numero"] == 123


def test_listar_contas():
    db.insert_cliente("Bruno", "333.444.555-66", "1992-11-11", "Rua Z, 303", "PF")
    cliente = db.get_cliente_by_cpf("333.444.555-66")

    db.insert_conta(1, cliente["id"])
    db.insert_conta(2, cliente["id"])

    contas = db.listar_contas()
    assert len(contas) == 2


# =========================================================
# Testes para Transações
# =========================================================
def test_insert_and_get_transacao():
    db.insert_cliente("Carla", "444.555.666-77", "1998-12-12", "Rua W, 404", "PF")
    cliente = db.get_cliente_by_cpf("444.555.666-77")

    db.insert_conta(999, cliente["id"])
    contas = db.get_contas_by_cliente(cliente["id"])
    conta_id = contas[0]["id"]

    db.insert_transacao("Deposito", 500.00, conta_id)
    transacoes = db.get_transacoes_by_conta(conta_id)

    assert len(transacoes) == 1
    assert transacoes[0]["tipo"] == "Deposito"
    assert transacoes[0]["valor"] == 500.00


def test_listar_transacoes():
    db.insert_cliente("Diego", "555.666.777-88", "1993-04-04", "Rua V, 505", "PF")
    cliente = db.get_cliente_by_cpf("555.666.777-88")

    db.insert_conta(100, cliente["id"])
    contas = db.get_contas_by_cliente(cliente["id"])
    conta_id = contas[0]["id"]

    db.insert_transacao("Deposito", 200.00, conta_id)
    db.insert_transacao("Saque", 50.00, conta_id)

    transacoes = db.listar_transacoes()
    assert len(transacoes) == 2 
    