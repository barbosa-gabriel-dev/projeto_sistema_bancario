from datetime import datetime
from .historico import Historico
from .transacao import Saque

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
            print("\n=== Depósito realizado com sucesso! ===")
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
            C/C:\t{self.numero:04d}
            Titular:\t{self.cliente.cpf}\t{self.cliente.nome}
            '''
