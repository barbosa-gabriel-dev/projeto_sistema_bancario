# O sys.path pode ser removido se você executar o script como um módulo
# a partir da raiz do projeto, ex: python -m sys_bank.main
from sys_bank.utils.menu import menu
from sys_bank.services.operacoes import (
    criar_cliente,
    criar_conta,
    depositar,
    sacar,
    exibir_extrato
)
# A função listar_contas_formatado não foi importada para manter o menu simples

def main():
    while True:
        opcao = menu()

        if opcao == "1":
            criar_cliente()

        elif opcao == "2":
            criar_conta()

        elif opcao == "3":
            depositar()

        elif opcao == "4":
            sacar()

        elif opcao == "5":
            exibir_extrato()
            
        elif opcao == "6":
            #TODO: Para listar contas, você pode criar uma função em operacoes.py
            # que chame db_manager.listar_contas_com_clientes() e formate a saída
            print("Funcionalidade de listar contas ainda não implementada no menu principal.")
            
        elif opcao == "0":
            print("\nSaindo do sistema... Obrigado por usar o SysBank!")
            break

        else:
            print("\n@@@ Opção inválida! Tente novamente. @@@")

if __name__ == "__main__":
    main()