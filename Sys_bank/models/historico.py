from datetime import datetime

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao, tipo=None):
        self._transacoes.append(
            {
                'tipo': tipo or transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now(),
            }
        )