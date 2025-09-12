import textwrap


def menu():
    menu = """\n
    ==================== MENU ====================
    [1][d]\tDepositar
    [2][s]\tSacar
    [3][e]\tExtrato
    [4][nu]\tNovo Cliente
    [5][nc]\tNova conta
    [6][lc]\tListar Contas
    [0][q]\tSair

    => """
    
    return input(textwrap.dedent(menu))
