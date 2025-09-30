from sys_bank.services.database_manager import DatabaseManager
# IMPORTANTE: Importar os modelos que vamos usar
from sys_bank.models.cliente import PessoaFisica
from sys_bank.models.conta import ContaCorrente
from sys_bank.models.transacao import Deposito, Saque, Transferencia

# A instância do db_manager continua sendo a ponte com o banco de dados
db_manager = DatabaseManager()

def depositar():
    # 1. Recuperamos os OBJETOS do cliente e da conta
    cliente_obj, conta_obj = recuperar_cliente_e_conta()
    if not cliente_obj:
        return

    try:
        valor = float(input("Informe o valor do depósito: "))
        # 2. Criamos o OBJETO da transação
        transacao = Deposito(valor)
        
        # 3. Usamos o método do OBJETO cliente para realizar a transação
        cliente_obj.realizar_transacao(conta_obj, transacao)
        
        # 4. Persistimos a mudança no banco de dados
        db_manager.atualizar_saldo(conta_obj.id_db, conta_obj.saldo)
        db_manager.insert_transacao(conta_obj.id_db, "deposito", valor)

    except ValueError:
        print("\n@@@ Valor inválido! Por favor, informe um número. @@@")

def sacar():
    cliente_obj, conta_obj = recuperar_cliente_e_conta()
    if not cliente_obj:
        return
        
    try:
        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)

        # A chamada é a mesma, mas o polimorfismo faz com que a lógica de saque seja executada
        cliente_obj.realizar_transacao(conta_obj, transacao)
        
        # Apenas persistimos no banco se a transação foi bem-sucedida (o saldo mudou)
        conta_db = db_manager.execute_query("SELECT saldo FROM contas WHERE id=?", (conta_obj.id_db,)).fetchone()
        if conta_db['saldo'] != conta_obj.saldo:
            db_manager.atualizar_saldo(conta_obj.id_db, conta_obj.saldo)
            db_manager.insert_transacao(conta_obj.id_db, "saque", valor)

    except ValueError:
        print("\n@@@ Valor inválido! Por favor, informe um número. @@@")

def transferir():
    # 1. Recupera os objetos do cliente e da conta de ORIGEM
    cliente_origem_obj, conta_origem_obj = recuperar_cliente_e_conta()
    if not cliente_origem_obj:
        return

    # 2. Pede os dados da conta de DESTINO
    try:
        numero_conta_destino = int(input("Informe o número da conta de destino: "))
        conta_destino_data = db_manager.execute_query(
            "SELECT * FROM contas WHERE numero = ?", (numero_conta_destino,)
        ).fetchone()

        if not conta_destino_data:
            print("\n@@@ Conta de destino não encontrada! @@@")
            return
        
        if conta_destino_data['id'] == conta_origem_obj.id_db:
            print("\n@@@ Conta de origem e destino não podem ser a mesma! @@@")
            return
        
        valor = float(input("Informe o valor da transferência: "))

    except ValueError:
        print("\n@@@ Valor ou número de conta inválido! Operação cancelada. @@@")
        return

    # 3. "Hidrata" o objeto da conta de DESTINO
    cliente_destino_data = db_manager.execute_query(
        "SELECT * FROM clientes WHERE id = ?", (conta_destino_data['cliente_id'],)
    ).fetchone()

    cliente_destino_obj = PessoaFisica(
        nome=cliente_destino_data['nome'], cpf=cliente_destino_data['cpf'],
        data_nascimento=cliente_destino_data['data_nascimento'], endereco=cliente_destino_data['endereco']
    )
    
    conta_destino_obj = ContaCorrente(numero=conta_destino_data['numero'], cliente=cliente_destino_obj)
    conta_destino_obj._saldo = conta_destino_data['saldo']
    conta_destino_obj.id_db = conta_destino_data['id']
    
    # 4. Cria o objeto da transação e executa
    transacao = Transferencia(valor)
    cliente_origem_obj.realizar_transferencia(conta_origem_obj, conta_destino_obj, transacao)

    # 5. Persiste as alterações no banco de dados, se houveram
    conta_origem_db = db_manager.execute_query("SELECT saldo FROM contas WHERE id=?", (conta_origem_obj.id_db,)).fetchone()
    
    if conta_origem_db['saldo'] != conta_origem_obj.saldo:
        print("\n=== Transferência realizada com sucesso! ===")
        db_manager.atualizar_saldo(conta_origem_obj.id_db, conta_origem_obj.saldo)
        db_manager.atualizar_saldo(conta_destino_obj.id_db, conta_destino_obj.saldo)
        # O registro de transações no DB já é feito pelo método transferir do database_manager
        # que podemos chamar para garantir consistência
        db_manager.transferir(conta_origem_obj.id_db, conta_destino_obj.id_db, valor)

def exibir_extrato():
    cliente_obj, conta_obj = recuperar_cliente_e_conta()
    if not cliente_obj:
        return

    print("\n================ EXTRATO ================")
    if not conta_obj.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta_obj.historico.transacoes:
            # Usamos os dados do histórico do objeto
            print(f"{transacao['data'].strftime('%Y-%m-%d %H:%M:%S')} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
    
    print(f"\nSaldo atual: R$ {conta_obj.saldo:.2f}")
    print("=========================================")

def criar_cliente():
    cpf = input("Informe o CPF (apenas números): ")
    cliente_data = db_manager.get_cliente_by_cpf(cpf)

    if cliente_data:
        print("\n@@@ Já existe um cliente cadastrado com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (AAAA-MM-DD): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ")

    db_manager.insert_cliente(nome, cpf, data_nascimento, endereco)
    print(f"\n=== Cliente {nome} criado com sucesso! ===")

def criar_conta():
    cpf = input("Informe o CPF do cliente: ")
    cliente_data = db_manager.get_cliente_by_cpf(cpf)

    if not cliente_data:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    cursor = db_manager.execute_query("SELECT MAX(numero) AS max_num FROM contas")
    max_num = cursor.fetchone()['max_num']
    numero_conta = (max_num or 1000) + 1

    db_manager.insert_conta(cliente_data["id"], numero_conta, tipo="corrente")
    print(f"\n=== Conta {numero_conta} criada com sucesso para o cliente {cliente_data['nome']}! ===")

def listar_contas():
    """Busca todas as contas no banco de dados e as exibe de forma formatada."""
    print("\n================ LISTA DE CONTAS ================")
    
    # 1. Chama o método do DatabaseManager que já faz o JOIN com a tabela de clientes
    contas = db_manager.listar_contas_com_clientes()

    # 2. Verifica se a lista de contas está vazia
    if not contas:
        print("Nenhuma conta cadastrada no sistema.")
        print("=================================================")
        return

    # 3. Itera sobre os resultados e exibe cada conta formatada
    for conta in contas:
        info_conta = f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero']}
            Titular:\t{conta['titular']}
        """
        print(textwrap.dedent(info_conta))
        print("-" * 40)
    
    print("=================================================")

# ======================================================
# Função auxiliar para "hidratar" os objetos
# ======================================================
def recuperar_cliente_e_conta():
    """Busca os dados no DB e retorna os objetos Cliente e Conta prontos para uso."""
    cpf = input("Informe o CPF do cliente: ")
    cliente_data = db_manager.get_cliente_by_cpf(cpf)
    if not cliente_data:
        print("\n@@@ Cliente não encontrado! @@@")
        return None, None

    contas_data = db_manager.get_contas_by_cliente(cliente_data["id"])
    if not contas_data:
        print("\n@@@ Cliente não possui conta! @@@")
        return None, None

    # Hidratação do objeto Cliente
    cliente_obj = PessoaFisica(
        nome=cliente_data['nome'],
        cpf=cliente_data['cpf'],
        data_nascimento=cliente_data['data_nascimento'],
        endereco=cliente_data['endereco']
    )

    # Permite ao usuário escolher a conta
    conta_selecionada_data = selecionar_conta(contas_data)
    if not conta_selecionada_data:
        return cliente_obj, None

    # Hidratação do objeto Conta
    conta_obj = ContaCorrente(
        numero=conta_selecionada_data['numero'],
        cliente=cliente_obj,
        limite=500, # Estes valores poderiam vir do DB no futuro
        limite_saques=3
    )
    # Define o saldo inicial e o ID do DB no objeto
    conta_obj._saldo = conta_selecionada_data['saldo']
    conta_obj.id_db = conta_selecionada_data['id'] # Atributo para guardar o ID do DB

    # Adiciona a conta ao cliente e carrega o histórico
    cliente_obj.adicionar_conta(conta_obj)
    transacoes_data = db_manager.get_transacoes_by_conta(conta_obj.id_db)
    for t in transacoes_data:
        transacao_classe = Saque if t['tipo'] == 'saque' else Deposito
        conta_obj.historico.adicionar_transacao(transacao_classe(t['valor']))

    return cliente_obj, conta_obj

def selecionar_conta(contas):
    # (Esta função auxiliar permanece a mesma do seu código original)
    if len(contas) == 1:
        return contas[0]
    # ... (resto da função igual)