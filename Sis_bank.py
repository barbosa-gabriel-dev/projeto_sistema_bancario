from abc import ABC, abstractclassmethod, abstractproperty
import textwrap
from datetime import date

class Conta:
    def __init__(self):
        self.__saldo: float
        self.__numero: int
        self.__agencia: str
        self.__cliente: Cliente
        self.__historico: Historico

    def saldo():
        pass

    def nova_conta(cliente:Cliente, numero:int):
        pass

    def sacar(valor:float):
        pass

    def depositar(valor:float):
        pass


class Historico:
    def adicionar_transacao(transacao:Transacao):
        pass

class ContaCorrente(Conta):
    def __init__(self):
        super().__init__()
        self._limite: float
        self._limite_saques: int
        
        
class Transacao(ABC):
    @abstractclassmethod
    def registrar(conta:Conta):
        pass

class Saque(Transacao):
    def __init__(self):
        super().__init__()
        self._valor: float

class Deposito(Transacao):
    def __init__(self):
        super().__init__()
        self._valor: float

class Cliente:
    def __init__(self):
        self.endereco: str
        self.contas: list

    def realizar_transacao(conta:Conta, transacao:Transacao):
        pass
    
    def adicionar_conta(conta:Conta):
        pass

class PessoaFisica(Cliente):
    def __init__(self):
        super().__init__()
        self._cpf: str
        self._nome: str
        self._data_nascimento: date

class PessoaJuridica(Cliente):
    def __init__(self):
        super().__init__()
        self._cnpj: str
        self._razao_social: str


def menu():
    menu = '''\n
    ==================== MENU ====================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar Contas
    [nu]\tNovo Usuário
    [q]\tSair

    => '''
    
    return input(textwrap.dedent(menu))


def depositar(saldo,extrato,/):
    valida_deposito = False
    
    while valida_deposito == False:
        try:
            valor = int(input('Quanto gostaria de depositar: '))
            if valor > 0:
                extrato += f'Depósito:\t+ R${valor:.2f}\n'
                saldo += valor
                valida_deposito = True
            else:
                print('Valor inválido')
        
        except ValueError:
            print('Valor inválido')
    
    return saldo, extrato


def sacar(*,saldo,extrato,limite,numero_saques,limite_saques):
    try:
        valor = float(input('Quanto gostaria de sacar: '))
        excedeu_limite = valor > limite
        excedeu_saldo = valor > saldo
        excedeu_saques = numero_saques >= limite_saques
        
        if excedeu_saques:
            print('Número de saques diarios excedido')
        
        elif excedeu_limite:
            print('Valor inválido. Limite de saque = R$500,00')
            print(f'Limite disponivel = R${limite}')
       
        elif excedeu_saldo:
            print('Saldo insuficiente')   
        
        else:
            extrato += f'Saque:\t\t- R${valor:.2f}\n'
            saldo -= valor
            limite -= valor     
    
    except ValueError:
        print('Valor inválido')
    
    return saldo, extrato


def exibir_extrato(saldo,/,*,extrato):
    print('\n================ EXTRATO ================')
    print('Não foram realizadas movimentações.'if not extrato else extrato)
    print(f'saldo atual: R${saldo:.2f}')
    print('\n=========================================')


def criar_usuario(usuarios):
    cpf = input('Informe o CPF (somente números): ')
    usuario = filtrar_usuario(cpf, usuarios)

    try:
        if cpf in usuario.items:
            print('\n Já existe usuário cadastrado com esse CPF!')
            return
    except AttributeError:
        pass

    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd/mm/aaaa): ')
    endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/estado(sigla)): ')
    print('Usuário criado com sucesso!')
    return {'nome':nome,'data_nascimento':data_nascimento,'cpf':cpf,'endereço':endereco}
    

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if cpf in usuario['cpf']:
            return usuario


def cria_conta(agencia,usuarios,contas):
    numero_da_conta = len(contas)
    numera_conta = '1000'+ str(numero_da_conta)
    cpf = input('Informe o CPF (somente números): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n Conta criada com sucesso!')
        return {'Agencia':agencia,'Conta':numera_conta,'Usuário':usuario}

    print('\nUsuário não encontrado, fluxo de crianção de conta encerrado')


def listar_contas(contas):
    print('\n========== CONTAS CADASTRADAS ==========')
    print('Não existem contas cadastradas.'if not contas else contas)
    print('\n=========================================')


def main():
    LIMITE_SAQUES = 3
    AGENCIA = '0001'

    saldo = 0
    limite = 500
    numero_saques = 0
    extrato = ''
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 'd':
            print('Depósito')
            saldo, extrato = depositar(saldo,extrato)

        elif opcao == 's':
            print('saque')
            saldo, extrato = sacar(
                saldo=saldo,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
                )

        elif opcao == 'e':
            print('Extrato')
            exibir_extrato(saldo,extrato=extrato)

        elif opcao == 'nu':
            usuario = criar_usuario(usuarios)
            if usuario:
                usuarios.append(usuario)

        elif opcao == 'nc':
            
            conta = cria_conta(AGENCIA,usuarios,contas)
            if conta:
                contas.append(conta)

        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'q':
            break
        
        else:
            print('Operação inválida, por favor selecione a opção desejada.')

if __name__ == "__main__":
    main()