import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )))

from sys_bank.utils import menu
from sys_bank.services.operacoes import (
    criar_cliente,
    criar_conta,
    depositar,
    sacar,
    transferir,
    listar_clientes,
    listar_contas,
    listar_transacoes,
)


def main():
    while True:
        opcao = menu()

        if opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            email = input("Email: ")
            telefone = input("Telefone: ")
            criar_cliente(nome, cpf, email, telefone)

        elif opcao == "2":
            cliente_id = int(input("ID do Cliente: "))
            tipo = input("Tipo de Conta (corrente/poupanca): ").lower()
            criar_conta(cliente_id, tipo)

        elif opcao == "3":
            conta_id = int(input("ID da Conta: "))
            valor = float(input("Valor do Depósito: "))
            depositar(conta_id, valor)

        elif opcao == "4":
            conta_id = int(input("ID da Conta: "))
            valor = float(input("Valor do Saque: "))
            sacar(conta_id, valor)

        elif opcao == "5":
            origem_id = int(input("ID da Conta de Origem: "))
            destino_id = int(input("ID da Conta de Destino: "))
            valor = float(input("Valor da Transferência: "))
            transferir(origem_id, destino_id, valor)

        elif opcao == "6":
            listar_clientes()

        elif opcao == "7":
            listar_contas()

        elif opcao == "8":
            listar_transacoes()

        elif opcao == "0":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()