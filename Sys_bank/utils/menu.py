import textwrap


def menu():
    menu_texto = """
   === Sistema Bancário - SysBank ===

    [1] Criar Cliente
    [2] Criar Conta
    [3] Depositar
    [4] Sacar
    [5] Exibir Extrato
    [6] Listar Contas
    [0] Sair

    => """
    
    return input(textwrap.dedent(menu))
