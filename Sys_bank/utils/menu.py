import textwrap


def menu():
    menu = """\n
   print("\n=== Sistema Bancário - SysBank ===")
    print("1. Criar Cliente")
    print("2. Criar Conta")
    print("3. Depositar")
    print("4. Sacar")
    print("5. Transferir")
    print("6. Listar Clientes")
    print("7. Listar Contas")
    print("8. Listar Transações")
    print("0. Sair")

    => """
    
    return input(textwrap.dedent(menu))
