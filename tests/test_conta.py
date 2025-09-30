import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )))

from sys_bank.models.transacao import Deposito, Saque

def test_deposito(conta_corrente):
    deposito = Deposito(150)
    deposito.registrar(conta_corrente)
    
    assert conta_corrente.saldo == 150
    assert len(conta_corrente.historico.transacoes) == 1
    assert conta_corrente.historico.transacoes[0]['tipo'] == "Deposito"

def test_saque(conta_corrente):
    # Primeiro, depositar para ter saldo
    conta_corrente.depositar(200)
    
    saque = Saque(100)
    saque.registrar(conta_corrente)
    
    assert conta_corrente.saldo == 100
    assert len(conta_corrente.historico.transacoes) == 2
    assert conta_corrente.historico.transacoes[-1]['tipo'] == "Saque"

def test_saque_sem_saldo(conta_corrente):
    saque = Saque(50)
    saque.registrar(conta_corrente)
    
    # Saldo não deve mudar
    assert conta_corrente.saldo == 0
    assert len(conta_corrente.historico.transacoes) == 0