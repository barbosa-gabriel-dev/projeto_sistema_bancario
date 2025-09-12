import textwrap
from sys_bank.models import ContaCorrente, PessoaFisica, Saque, Deposito


def operacao(clientes, tipo_transacao):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    tipo_transacao = tipo_transacao
    if tipo_transacao == "Depositar":
        valor = float(input("Informe o valor do deposito:"))
        transacao = Deposito(valor)
    
    elif tipo_transacao == "Sacar":
        valor = float(input("Informe o valor do saque:"))
        transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("\n@@@ Cliente não possiu conta! @@@")
        return
    
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
        
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo atual:\n\tR$ {conta.saldo:.2f}")
    print("\n=========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        print("\n@@@ Já existe um cliente cadastrado com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/estado(sigla)): ")
    print("Usuário criado com sucesso!")
    
    cliente = PessoaFisica(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")
    

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('\n@@@ Cliente não possui conta! @@@')
        return
    
    numerador = 0
    print("Contas do cliente:")
    for conta in cliente.contas:
        print(f"[{numerador}]  {conta}")
        numerador += 1
   
    while True:
        try:
            selecao_conta = int(input("\nSelecione a conta: "))
            
            if selecao_conta in range(len(cliente.contas)):
                return cliente.contas[selecao_conta]   
            else:
                print("@@@ Número incorreto conta não encontrada! @@@")
            
        except ValueError:
            print("@@@ Entrada inválida. Por favor, digite apenas números. @@@")


def criar_conta(numero_conta,clientes,contas):
    cpf = input('Informe o CPF do cliente:')
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print('\n@@@ Cliente não encontrado! @@@')
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente,numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('\n=== Conta criada com sucesso! ===')
    

def listar_contas(contas):
    if len(contas) == 0:
        print("Não existem contas cadastradas.")
        
    for conta in contas:
        print("=" * 50)
        print(textwrap.dedent(str(conta)))
