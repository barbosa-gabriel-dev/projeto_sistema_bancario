import textwrap
from sys_bank.services import database_manager as db


def operacao(tipo_transacao):
    cpf = input("Informe o CPF do cliente: ")
    cliente = db.get_cliente_by_cpf(cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    contas = db.get_contas_by_cliente(cliente["id"])
    if not contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # Se o cliente tiver mais de uma conta, deixa escolher
    conta = selecionar_conta(contas)

    if tipo_transacao == "Depositar":
        valor = float(input("Informe o valor do depósito: "))
        novo_saldo = conta["saldo"] + valor
        db.atualizar_saldo(conta["id"], novo_saldo)
        db.insert_transacao("Deposito", valor, conta["id"])
        print("\n=== Depósito realizado com sucesso! ===")

    elif tipo_transacao == "Sacar":
        valor = float(input("Informe o valor do saque: "))
        if valor > conta["saldo"]:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
            return
        novo_saldo = conta["saldo"] - valor
        db.atualizar_saldo(conta["id"], novo_saldo)
        db.insert_transacao("Saque", valor, conta["id"])
        print("\n=== Saque realizado com sucesso! ===")


def exibir_extrato():
    cpf = input("Informe o CPF do cliente: ")
    cliente = db.get_cliente_by_cpf(cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    contas = db.get_contas_by_cliente(cliente["id"])
    if not contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    conta = selecionar_conta(contas)
    transacoes = db.get_transacoes_by_conta(conta["id"])

    print("\n================ EXTRATO ================")
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"{transacao['data_hora']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
    print(f"\nSaldo atual: R$ {conta['saldo']:.2f}")
    print("=========================================")


def criar_cliente():
    cpf = input("Informe o CPF do cliente: ")
    cliente = db.get_cliente_by_cpf(cpf)

    if cliente:
        print("\n@@@ Já existe um cliente cadastrado com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/estado(sigla)): ")

    db.insert_cliente(nome, cpf, data_nascimento, endereco)
    print("\n=== Cliente criado com sucesso! ===")


def criar_conta():
    cpf = input("Informe o CPF do cliente: ")
    cliente = db.get_cliente_by_cpf(cpf)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    contas = db.get_contas_by_cliente(cliente["id"])
    numero_conta = len(contas) + 1

    db.insert_conta(numero_conta, cliente["id"])
    print("\n=== Conta criada com sucesso! ===")


def listar_contas():
    contas = db.listar_contas()
    if not contas:
        print("Não existem contas cadastradas.")
        return

    for conta in contas:
        print("=" * 50)
        print(textwrap.dedent(f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero']}
            Titular:\t{conta['cliente_nome']}
        """))


# ======================================================
# Função auxiliar
# ======================================================
def selecionar_conta(contas):
    print("Contas do cliente:")
    for idx, conta in enumerate(contas):
        print(f"[{idx}] Agência {conta['agencia']} - C/C {conta['numero']} (Saldo: R$ {conta['saldo']:.2f})")

    while True:
        try:
            selecao = int(input("\nSelecione a conta: "))
            if selecao in range(len(contas)):
                return contas[selecao]
            else:
                print("@@@ Número incorreto. Conta não encontrada! @@@")
        except ValueError:
            print("@@@ Entrada inválida. Digite apenas números. @@@")
