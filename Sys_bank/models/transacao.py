from abc import ABC, abstractmethod, abstractclassmethod, abstractproperty
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

     def registrar_transferencia(self, conta_origem, conta_destino):
        #NOTE:Registra a transação em ambas as contas.
        if conta_origem.transferir(conta_destino, self.valor):
            conta_origem.historico.adicionar_transacao(self, tipo="Transferência Enviada")
            conta_destino.historico.adicionar_transacao(self, tipo="Transferência Recebida")

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