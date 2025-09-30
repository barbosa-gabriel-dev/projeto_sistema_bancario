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
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
            return False
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        
        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        
        else:
            print("\n@@@ Operação falhou! O valor informado é invalido.")
       
        return False

    def transferir(self, conta_destino, valor):
        #NOTE:Tenta sacar da conta atual e depositar na conta de destino.
        if not self.sacar(valor):
            return False

        conta_destino.depositar(valor)
        return True

class ContaCorrente(Conta):
    
    def __init__(self, numero, cliente, tipo="corrente", limite=500, limite_saques=3,limite_transacoes=10):
        super().__init__(numero, cliente)
        self.tipo = tipo
        self.limite = limite
        self.limite_saques = limite_saques
        self.limite_transacoes = limite_transacoes
    
    def _transacoes_diarias(self):
        #NOTE:Retorna uma lista de transações realizadas hoje.
        return [t for t in self.historico.transacoes if t['data'].date() == date.today()]
    
    def sacar(self, valor):
        transacoes_hoje = self._transacoes_diarias()
        
        numero_saques = len(
            [t for t in transacoes_hoje if t['tipo'] == Saque.__name__]
        )

        if valor > self.limite:
            print("\n@@@ Operação falhou! O valor de saque excede o limite. @@@")
            return False
        if numero_saques >= self.limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False
        if len(transacoes_hoje) >= self.limite_transacoes:
            print("\n@@@ Operação falhou! Número máximo de transações diárias excedido. @@@")
            return False

        return super().sacar(valor)
    
    def depositar(self, valor):
        transacoes_hoje = self._transacoes_diarias()
        
        excedeu_transacoes = len(transacoes_hoje) >= self.limite_transacoes

        if len(transacoes_hoje) >= self.limite_transacoes:
            print("\n@@@ Operação falhou! Número maximo de transações diarias excedido, @@@")
            return False

        return super().depositar(valor)
        return True
    
        
    def __str__(self):
        return f'''
            Agência:\t{self.agencia}
            C/C:\t{self.numero:04d}
            Titular:\t{self.cliente.cpf}\t{self.cliente.nome}
            '''
