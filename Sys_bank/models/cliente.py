class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transferencia(self, conta_origem, conta_destino, transacao):
        """Método para orquestrar uma transferência."""
        # CORRIGIDO: Chama o método com o novo nome
        transacao.registrar_transferencia(conta_origem, conta_destino)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
