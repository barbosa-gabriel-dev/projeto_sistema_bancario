import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )))

import pytest
from sys_bank.models.cliente import PessoaFisica
from sys_bank.models.conta import ContaCorrente
from sys_bank.models.transacao import Deposito, Saque

@pytest.fixture
def cliente_fisico():
    """Retorna um cliente PessoaFisica pronto para testes"""
    cliente = PessoaFisica(
        nome="Gabriel Barbosa",
        cpf="12345678900",
        data_nascimento="01-01-1990",
        endereco="Rua A, 100 - Bairro B - Cidade/UF"
    )
    return cliente

@pytest.fixture
def conta_corrente(cliente_fisico):
    """Retorna uma conta corrente associada a um cliente"""
    conta = ContaCorrente.nova_conta(cliente=cliente_fisico, numero=1)
    cliente_fisico.adicionar_conta(conta)
    return conta

@pytest.fixture
def clientes_lista():
    """Retorna uma lista de clientes pronta para testes"""
    cliente1 = PessoaFisica("Gabriel", "12345678900", "01-01-1990", "Rua A")
    cliente2 = PessoaFisica("Maria", "98765432100", "02-02-1990", "Rua B")
    return [cliente1, cliente2]