import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )))


def test_adicionar_conta(cliente_fisico, conta_corrente):
    assert len(cliente_fisico.contas) == 1
    assert cliente_fisico.contas[0] == conta_corrente

def test_realizar_transacao(cliente_fisico, conta_corrente):
    from sys_bank.models.transacao import Deposito
    
    deposito = Deposito(200)
    cliente_fisico.realizar_transacao(conta_corrente, deposito)
    
    assert conta_corrente.saldo == 200
    assert len(conta_corrente.historico.transacoes) == 1