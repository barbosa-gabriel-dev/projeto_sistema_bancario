# 🏦 Sys Bank

Um sistema bancário simples, desenvolvido em Python, com estrutura modular para fins de estudo e prática de programação orientada a objetos, com persistência em banco de dados SQLite.


## 📌 Funcionalidades
- Cadastro de clientes
- Criação de contas (corrente e poupança)
- Depósitos, saques e transferências
- Histórico de transações
- Listagem de clientes, contas e transações
- Testes automatizados com pytest


## 📂 Estrutura do Projeto
```
sys_bank/
│── main.py # Ponto de entrada da aplicação
│── run_tests.py # Runner de testes com relatório HTML
│── models/ # Modelos de domínio (Conta, Cliente, Transações, etc.)
│── services/ # Operações, regras de negócio e banco de dados
│── utils/ # Funções auxiliares (menu, helpers)
│── tests/ # Testes automatizados com pytest
```


## 🛠️ Requisitos
- Python 3.10+


## 🚀 Como executar

    1. Clone este repositório:
        ```bash
        git clone https://github.com/seu-usuario/sys_bank.git
        cd sys_bank

    2. (Opcional) Crie e ative um ambiente virtual:
        python -m venv venv
        source venv/bin/activate   # Linux/Mac
        venv\Scripts\activate      # Windows

    3. Instale as dependências (apenas para testes):
        pip install -r requirements.txt

    4. Rode o sistema:
        python -m sys_bank.main

    ⚠️ Se preferir rodar direto com python sys_bank/main.py


## 🧪 Rodando os testes
    python run_tests.py


## 🎯 Objetivo do Projeto

Este projeto foi desenvolvido como exercício de Python + POO + Estrutura modular + Testes automatizados, servindo como base para futuros projetos maiores (como um ERP).

👨‍💻 Autor: Gabriel Barbosa
📅 Versão inicial: 2025