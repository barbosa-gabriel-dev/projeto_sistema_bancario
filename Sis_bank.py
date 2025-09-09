import textwrap
from abc import ABC, abstractmethod, abstractclassmethod, abstractproperty
from datetime import datetime

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
            
        else:
            print("\n@@@ Operação falhou! O valor informado é invalido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depoósito realizado com sucesso! ===")
            return True
        
        else:
            print("\n@@@ Operação falhou! O valor informado é invalido.")
       
        return False

class ContaCorrente(Conta):
    
    def __init__(self, numero, cliente, limite=500, limite_saques=3,limite_transacoes=10):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.limite_transacoes = limite_transacoes
    
    def sacar(self, valor):
        numero_transacoes = len(
            [transacao for transacao in self.historico.transacoes 
            if transacao['data'] > datetime.now().strftime('%d-%m-%Y 00:00:00')
            and transacao['data'] < datetime.now().strftime('%d-%m-%Y %H:%M:%S')]
        )
        
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes 
            if transacao['tipo'] == Saque.__name__]
        )

        excedeu_transacoes = numero_transacoes >= self.limite_transacoes
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor de saque Excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número maximo de saques excedido, @@@")

        elif excedeu_transacoes:
            print("\n@@@ Operação falhou! Número maximo de transações diarias excedido, @@@")

        
        else:
            return super().sacar(valor)
        return False
    
    def depositar(self, valor):
        numero_transacoes = len(
            [transacao for transacao in self.historico.transacoes 
            if transacao['data'] > datetime.now().strftime('%d-%m-%Y 00:00:00')
            and transacao['data'] < datetime.now().strftime('%d-%m-%Y %H:%M:%S')]
        )
        
        excedeu_transacoes = numero_transacoes >= self.limite_transacoes

        if excedeu_transacoes:
            print("\n@@@ Operação falhou! Número maximo de transações diarias excedido, @@@")

        else:
            return super().depositar(valor)
        return False
    
        
    def __str__(self):
        return f'''
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.cpf}\t{self.cliente.nome}
            '''

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            }
        )
        
class Transacao(ABC):
   @property
   @abstractmethod
   def valor(self):
       pass
   
   @classmethod
   @abstractmethod
   def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


def menu():
    menu = """\n
    ==================== MENU ====================
    [1][d]\tDepositar
    [2][s]\tSacar
    [3][e]\tExtrato
    [4][nu]\tNovo Cliente
    [5][nc]\tNova conta
    [6][lc]\tListar Contas
    [0][q]\tSair

    => """
    
    return input(textwrap.dedent(menu))


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    valor = float(input("Informe o valor do deposito:"))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("\n@@@ Cliente não possiu conta! @@@")
        return
    
    cliente.realizar_transacao(conta, transacao)

# TODO: transformar as funções depositar e sacar em uma só que solicita o tipo de transação
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: " )
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    valor = float(input("Informe o valor do saque:"))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
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


def main():
    
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd' or opcao == '1':
            print('Depósito')
            depositar(clientes)

        elif opcao == 's' or opcao == '2':
            print('saque')
            sacar(clientes)

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