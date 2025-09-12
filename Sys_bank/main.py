import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )))

from sys_bank.utils import menu
from sys_bank.services import (
    operacao,
    exibir_extrato,
    criar_cliente,
    criar_conta,
    listar_contas,
)



def main():
    
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd' or opcao == '1':
            print('Depósito')
            operacao(clientes, "Depositar")

        elif opcao == 's' or opcao == '2':
            print('saque')
            operacao(clientes, "Sacar")

        elif opcao == 'e' or opcao == '3':
            print('Extrato')
            exibir_extrato(clientes)

        elif opcao == 'nu' or opcao == '4':
            criar_cliente(clientes)
        
        elif opcao == 'nc' or opcao == '5':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == 'lc' or opcao == '6':
            listar_contas(contas)

        elif opcao == 'q' or opcao == '0':
            break
        
        else:
            print("Operação inválida, por favor selecione a opção desejada.")

if __name__ == "__main__":
    main()