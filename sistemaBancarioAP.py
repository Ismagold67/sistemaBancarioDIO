import textwrap


def menu():
    menu = """\n
    ############### MENU ###############
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [pb]\tPagar Boleto
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n$$$ Depósito realizado com sucesso! $$$")
    else:
        print("\n~~ Erro na operação! O valor informado é inválido. ~~")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n~~ Erro na operação! Você não tem saldo suficiente. ~~")

    elif excedeu_limite:
        print("\n~~ Erro na operação! O valor do saque excede o limite. ~~")

    elif excedeu_saques:
        print("\n~~ Erro na operação! Número máximo de saques excedido. ~~")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n~~ Erro na operação! O valor informado é inválido. ~~")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n############### EXTRATO ###############")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("#########################################")


def criar_usuario(usuarios):
    cpf = input("Informe os números do CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n~~ CPF informado já possui usuário, refaça a operação! ~~")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("### Usuário cadastrado com sucesso! ###")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n$$$ Conta cadastrada com sucesso! $$$")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n~~ Usuário não encontrado, fluxo de criação de conta encerrado! ~~")

def pagar_boleto(*,valor, extrato, saldo):

    while len(valor) != 13:
        print('Falha na operação, verifique se digitou os números corretamente!')
        print('\n')
        valor = input('Digite os números do código de barra ou digite "q" para cancelar a operação:')
        if valor == 'q':
            print('\n')
            print('~~ Operação Cancelada! ~~')
            return
    else:
        valor_total = float(input('Informe o valor total do boleto: '))

        if saldo < valor_total:
            mensagem = f'''\n
            Saldo insuficiente para realizar pagamento!

            Saldo da Conta: R$ {saldo}
            Total do boleto: R$ {valor_total}
            Operação Cancelada!!
            \n'''
            print(mensagem)
            
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
                saldo -= valor_total 
                extrato += 'PG de Boleto\t'+f'R$ {valor_total:.2f}\n'
                print('Pagamento realizado com sucesso!')
                
            elif pagamento == 'n':
                print('Operação Cancelada')
            else:
                print('Digite uma opção válida!')

            return saldo, extrato

                       

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def principal():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == 'pb':
            valor = str(input('Digite o número do código de barra: '))
            saldo, extrato = pagar_boleto(
                saldo=saldo, 
                extrato=extrato, 
                valor=valor,
            )
        elif opcao == "q":
            break

        else:
            print("Operação inválida, favor, refaça a operação.")


principal()
