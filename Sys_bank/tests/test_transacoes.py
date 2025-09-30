import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )))

from sys_bank.services.operacoes import filtrar_cliente, recuperar_conta_cliente

def test_filtrar_cliente(clientes_lista):
    cliente = filtrar_cliente("12345678900", clientes_lista)
    assert cliente.nome == "Gabriel"

    cliente_inexistente = filtrar_cliente("00000000000", clientes_lista)
    assert cliente_inexistente is None

def test_recuperar_conta_cliente(cliente_fisico, conta_corrente, monkeypatch):
    # Simula a entrada do usuário selecionando a primeira conta
    monkeypatch.setattr('builtins.input', lambda _: '0')
    conta = recuperar_conta_cliente(cliente_fisico)
    
    assert conta == conta_corrente