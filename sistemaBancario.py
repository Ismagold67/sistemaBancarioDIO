menu = '''
    [d] Depositar
    [s] Sacar
    [p] Pagar Boleto
    [e] Extrato
    [q] Sair

=> '''

saldo = 0
limite = 1000
extrato = ''
numeros_saques = 0
LIMITE_SAQUES = 5

while True:

    opcao = input(menu)

    if opcao == 'd':
        valor = float(input('Informe o valor do depósito: '))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print('Realizado com sucesso!')
        else:
            print('Erro na operação! O valor informado é inválido.'),
    elif opcao == 's':
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numeros_saques > LIMITE_SAQUES
        
        if excedeu_saldo:
            print("Erro na operação! Você não tem saldo suficiente.")
        elif excedeu_limite:
            print('Erro na operação! O valor do saque excedeu o limite.')
        elif excedeu_saques:
            print("Erro na operação! Número máximo de saques excedido.")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numeros_saques += 1
            print("Valor sacado com sucesso.")
        else:
            print("Erro na operação! O valor informado é inválido.")
    elif opcao == 'p':
        valor = input('Digite o número do código de barra:')

        while len(str(valor)) != 13:
            print('Falha na operação, verifique se digitou os números corretamente!')
            valor = input('Digite o número do código de barra:')
        else:
            pagamento = input(''' 
            Deseja pagar essa conta?

            [s] Sim
            [n] Não

            => ''')
            if pagamento == 's':
                print('Pagamento realizado com sucesso!')
            elif pagamento == 'n':
                print('Operação cancelada!')
            else:
                print('Digite uma opção válida!')
    elif opcao == 'e':
       print('\n********** Extrato **********')
       print('Não foram realizadas movimentações.'if not extrato else extrato)
       print(f'\nSaldo: R$ {saldo:.2f}')
       print('*****************************')
    elif opcao == 'q':
        break
    else:
        print('Operação inválida, por favor selecione novamente a operação desejada.')