# sys_bank/tests/test_database.py

import pytest
from sys_bank.services.database_manager import DatabaseManager


@pytest.fixture
def db():
    """Cria um banco em memória para rodar os testes isolados."""
    db = DatabaseManager(":memory:")
    yield db
    db.conn.close()


def test_criar_cliente(db):
    cliente_id = db.criar_cliente("João", "12345678900", "joao@email.com", "99999-9999")
    assert cliente_id is not None

    cliente = db.get_cliente(cliente_id)
    assert cliente[1] == "João"
    assert cliente[2] == "12345678900"


def test_criar_conta(db):
    cliente_id = db.criar_cliente("Maria", "98765432100", "maria@email.com", "88888-8888")
    conta_id = db.criar_conta(cliente_id, "corrente")
    assert conta_id is not None

    conta = db.get_conta(conta_id)
    assert conta[1] == cliente_id
    assert conta[2] == "corrente"
    assert conta[3] == 0.0  # saldo inicial


def test_deposito_e_saque(db):
    cliente_id = db.criar_cliente("Carlos", "11122233344", "carlos@email.com", "77777-7777")
    conta_id = db.criar_conta(cliente_id, "poupanca")

    # Depositar
    db.registrar_transacao(conta_id, "deposito", 1000.0)
    conta = db.get_conta(conta_id)
    assert conta[3] == 1000.0

    # Sacar
    db.registrar_transacao(conta_id, "saque", 200.0)
    conta = db.get_conta(conta_id)
    assert conta[3] == 800.0


def test_transferencia(db):
    cliente1 = db.criar_cliente("Ana", "22233344455", "ana@email.com", "66666-6666")
    conta1 = db.criar_conta(cliente1, "corrente")

    cliente2 = db.criar_cliente("Bruno", "33344455566", "bruno@email.com", "55555-5555")
    conta2 = db.criar_conta(cliente2, "poupanca")

    db.registrar_transacao(conta1, "deposito", 500.0)
    db.transferir(conta1, conta2, 200.0)

    saldo1 = db.get_conta(conta1)[3]
    saldo2 = db.get_conta(conta2)[3]

    assert saldo1 == 300.0
    assert saldo2 == 200.0


def test_listar_clientes_contas_transacoes(db):
    cliente_id = db.criar_cliente("Diego", "44455566677", "diego@email.com", "44444-4444")
    conta_id = db.criar_conta(cliente_id, "corrente")
    db.registrar_transacao(conta_id, "deposito", 150.0)

    clientes = db.listar_clientes()
    contas = db.listar_contas()
    transacoes = db.listar_transacoes()

    assert any("Diego" in str(c) for c in clientes)
    assert any("corrente" in str(c) for c in contas)
    assert any("deposito" in str(t) for t in transacoes)
