menu = '''
 
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> '''

saldo = 0
limite = 500
numero_saques = 0
LIMETE_SAQUES = 3
extrato = []

while True:
    opcao = input(menu)

    if opcao == 'd':
        print('Depósito')
        valida_deposito = False
        while valida_deposito == False:
            try:
                deposito = int(input('Quanto gostaria de depositar: '))
                if deposito >= 0:
                    extrato.append(f' + R${deposito}')
                    saldo += deposito
                    valida_deposito = True
                else:
                    print('Valor inválido')
            except ValueError:
                print('Valor inválido')

    elif opcao == 's':
        print('saque')
        try:
            saque = float(input('Quanto gostaria de saquar: '))
            if numero_saques < LIMETE_SAQUES:
                if saque <= limite:
                    if saque <= saldo:
                        extrato.append(f' - R${saque}')
                        saldo -= saque
                        limite -= saque
                    else:
                        print('Saldo insuficiente')
                else:
                    print('Valor inválido. Limite de saque = R$500,00')
            else:
                print('Número de saques diarios excedido')
        except ValueError:
              print('Valor inválido')  


    elif opcao == 'e':
        print('Extrato')
        for linha in extrato:
            print(linha)
        print(f'saldo atual: R${saldo:.2f}')

    elif opcao == 'q':
        break
        
    else:
        print('Operação inválida, por favor selecione a opção desejada.')
