# 🏦 Sys Bank

Um sistema bancário simples, desenvolvido em Python, com estrutura modular para fins de estudo e prática de programação orientada a objetos, com persistência em banco de dados SQLite e uma suíte de testes automatizados.


## 📌 Funcionalidades
- Gestão de Clientes: Cadastro e busca de clientes (Pessoa Física).
- Contas: Criação de Contas Correntes vinculadas a um cliente.
- Operações Financeiras: Realização de depósitos, saques e transferências entre contas.
- Histórico: Geração de extrato com o histórico completo de transações por conta.
- Testes Automatizados: Suíte de testes com pytest para garantir a integridade do código.
- Relatórios: Geração de relatórios de testes em formato HTML para fácil visualização.

## 📂 Estrutura do Projeto
```
projeto_sistema_bancario/
│── main.py                 # Ponto de entrada da aplicação (interface do usuário)
│── run_tests.py            # Runner  para executar a suíte de testes com relatório
├── requirements.txt        # Dependências do projeto (para testes)
├── sys_bank/
    │── models/             # Modelos de domínio (Conta, Cliente, Transações, etc.)
    │── services/           # Operações, regras de negócio e acesso ao banco de dados
    │── utils/              # Funções auxiliares (ex: menu da aplicação)
    └── __init__.py
├── tests/
│   ├── conftest.py         # Fixtures e configurações para os testes
│   ├── test_cliente.py
│   ├── test_conta.py
│   └── test_database.py
└── reports/                # Diretório para salvar os relatórios de testes
```


## 🛠️ Tecnologias Utilizadas
- Linguagem: Python 3.10+
- Banco de Dados: SQLite 3 (módulo nativo)
- Testes: ```pytest``` e ```pytest-html```


## 🚀 Como executar

    1. Clone este repositório:
       
        git clone https://github.com/barbosa-gabriel-dev/projeto_sistema_bancario
        cd projeto_sistema_bancario

    2. (Recomendado) Crie e ative um ambiente virtual:
    
        python -m venv venv
        source venv/bin/activate   # Linux/Mac
        venv\Scripts\activate      # Windows
    
    3. Instale as dependências (apenas para testes):
        pip install -r requirements.txt

    4. Rode o sistema:
        python -m sys_bank.main

    ⚠️ Se preferir rodar direto com python projeto_sistema_bancario/sys_bank/main.py


## 🧪 Rodando os testes
    python run_tests.py


## 🎯 Objetivo do Projeto

Este projeto foi desenvolvido como exercício de Python + POO + Estrutura modular + Testes automatizados, servindo como base para futuros projetos maiores (como um ERP).

👨‍💻 Autor: Gabriel Barbosa
📅 Versão inicial: 2025