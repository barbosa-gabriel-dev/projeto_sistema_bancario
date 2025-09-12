# 🏦 Sys Bank

Um sistema bancário simples, desenvolvido em Python, com estrutura modular para fins de estudo e prática de programação orientada a objetos.

## 📌 Funcionalidades
- Criar clientes (Pessoa Física)
- Criar contas correntes
- Depositar e sacar valores
- Exibir extratos detalhados
- Listar contas cadastradas
- Histórico de transações por conta


## 📂 Estrutura do Projeto
sys_bank/
│── main.py # Ponto de entrada do sistema
│── models/ # Modelos de domínio (Conta, Cliente, Transações, etc.)
│── services/ # Operações e regras de negócio
│── utils/ # Utilitários (menu, helpers)
│── tests/ # Testes automatizados com pytest


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
    pytest -v


## 🎯 Objetivo do Projeto

Este projeto foi desenvolvido como exercício de Python + POO + Estrutura modular + Testes automatizados, servindo como base para futuros projetos maiores (como um ERP).

👨‍💻 Autor: Gabriel Barbosa
📅 Versão inicial: 2025