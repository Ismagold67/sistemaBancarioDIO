import textwrap

menu = """\n
    ========== Menu ==========
    [d]\tDepositar
    [s]\tSacar
    [p]\tPagar Boleto
    [nc]\tNova Conta
    [lc]\tListar contas
    [nu]\tNovo Usuário
    [e]\tExtrato
    [q]\tSair
    => """

saldo = 0
limite = 1000
extrato = ''
numeros_saques = 0
contas = []
usuarios = []
LIMITE_SAQUES = 5
AGENCIA = "0001"

while True:
    
    opcao = input(textwrap.dedent(menu))

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
            valor_total = float(input('Informe o valor total do boleto: '))

            if saldo < valor_total:
                print('\n')
                print('Saldo insuficiente para efetuar pagamento!')
                print(f'Saldo da Conta: R$ {saldo:.2f}')
                print('Operação Cancelada!!')
            else:
                pagamento = input(f''' 
                Saldo da Conta: R$ {saldo}
                Total do boleto: R${valor_total}
                Deseja pagar essa conta?

                [s] Sim
                [n] Não

                =>''')
                print('\n')
                if pagamento == 's':
                    extrato += 'PG de Boleto:'+f'R$ {valor_total:.2f}'
                    saldo -= valor_total
                    print('Pagamento realizado com sucesso!')
                elif pagamento == 'n':
                    print('Operação cancelada!')
                else:
                    print('Digite uma opção válida!')
    elif opcao == 'lc':

        if len(contas) == 0:
            print('Você não possui contas cadastradas, favor, volte ao menu e crie sua conta!')
        else:
            for conta in contas:
                msg = f""" 
                =====================================================================
                Agência:\t {conta["agencia"]}
                C/C:\t\t   {conta["numero_conta"]}
                Titular:\t {conta["usuario"]['nome']}
                =====================================================================
                """
                print(textwrap.dedent(msg))
    elif opcao == 'nc':

        def other_filter_user(cpf, usuarios):
            usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
            return usuarios_filtrados[0] if usuarios_filtrados else None

        cpf = input('Informe os números do CPF: ') 
        usuario = other_filter_user(cpf, usuarios)

        if usuario:
            print('\n')
            print('$$$ Conta criada com sucesso! $$$')
            conta = ({"agencia": AGENCIA, "numero_conta": len(contas) + 1, "usuario": usuario})
            contas.append(conta)
        else:
            print('\n')
            print('$$$ Usuário não cadastrado em nosso banco de dados, fim de operação! $$$')

    elif opcao == 'nu':
        def other_filter_user(cpf, usuarios):
            usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
            return usuarios_filtrados[0] if usuarios_filtrados else None
                
        cpf = input("Informe os números do CPF: ")
        usuario = other_filter_user(cpf, usuarios)

        if usuario:
                    print('\n')
                    print('~~ CPF informado já possui usuário, refaça a operação! ~~')

        nome = input('Informe o nome completo: ')
        data_nascimento = input('Informe a data de nascumento (dd-mm-aaaa):')
        endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigla do estado):")

        usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

        print('\n')
        print("$$$ Usuário cadastrado com sucesso! $$$")

    elif opcao == 'e':
       print('\n********** Extrato **********')
       print('Não foram realizadas movimentações.'if not extrato else extrato)
       print(f'\nSaldo: R$ {saldo:.2f}')
       print('*****************************')
    elif opcao == 'q':
        break
    else:
        print('Operação inválida, por favor selecione novamente a operação desejada.')