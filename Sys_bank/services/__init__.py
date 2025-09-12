"""
Módulo de serviços do sistema bancário.
Contém as operações de negócio como depósito, saque, extrato,
criação de clientes e contas.
"""

from .operacoes import (
    operacao,
    exibir_extrato,
    criar_cliente,
    criar_conta,
    listar_contas,
)

__all__ = [
    "operacao",
    "exibir_extrato",
    "criar_cliente",
    "criar_conta",
    "listar_contas",
]