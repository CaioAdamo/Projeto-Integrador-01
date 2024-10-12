import oracledb

# Conexão
connection = oracledb.connect(user="BD150224234", password="Bfyqp10", dsn="172.16.12.14/xe")

cursor = connection.cursor()

cursor.execute('''
        CREATE TABLE cadastro_produto(
        codigo_produto varchar2(30) primary key,
        nome_produto varchar(55),
        descricao_produto varchar2(100),
        CP number,
        CF number,
        CV number,
        IV number,
        ML number
        )
    ''')

connection.commit()

def lista():
    cursor.execute("SELECT COUNT(*) FROM cadastro_produto")
    count = cursor.fetchone()[0]

    if count == 0:
        print("Não há produtos cadastrados.")
    else:
        cursor.execute("SELECT * FROM cadastro_produto")
        for row in cursor:
            codigo, nome, desc, cp, cf, cv, iv, ml = row
            pv = cp / (1 - ((cf + cv + iv + ml) / 100))
            #cálculo da receita bruta
            rb = pv - cp

            #cálculo de outros custos
            oc = (cf/100*pv) + (cv/100*pv) + (iv/100*pv)

            print(codigo, nome, desc)
            print(f"Descrição                        Valor       %")
            print(f"A. PREÇO DE VENDA             R${pv:.2f}     100%")
            print(f"B. CUSTO DE AQUISIÇÃO         R${cp:.2f}     {round((cp*100)/pv)}%")
            print(f"C. RECEITA BRUTA              R${rb:.2f}     {round((rb*100)/pv)}%")
            print(f"D. CUSTO FIXO ADMINISTRATIVO  R${cf/100*pv:.2f}     {round(cf)}%")
            print(f"E. COMISSÃO DE VENDAS         R${cv/100*pv:.2f}     {round(cv)}%")
            print(f"F. IMPOSTOS                   R${iv/100*pv:.2f}     {round(iv)}%")
            print(f"G. OUTROS CUSTOS              R${oc:.2f}     {round((oc*100)/pv)}%")
            print(f"H. RENTABILIDADE              R${ml/100*pv:.2f}     {round(ml)}%")

            if ml < 0:
                print(f"Lucro: Prejuízo")
            else:
                if ml == 0:
                    print(f"Lucro: Equilíbrio")
                elif 0 < ml < 10:
                    print(f"Lucro: Baixo")
                elif 10 <= ml <= 20:
                    print(f"Lucro: Médio")
                elif ml > 20:
                    print(f"Lucro: Alto")
            print("\n")

def menu ():
    print (f"Ações disponíveis:")
    print (f"1 - Cadastrar novo produto")
    print (f"2 - Alterar produto existente")
    print (f"3 - Excluir produto existente")
    print (f"4 - Listar informações dos produtos (tabela)")
    print (f"0 - Encerrar programa")

def cadastrar():
    print(f"Digite as informações do produto que deseja cadastrar:")
    cd = input("Digite o Código do produto: ")
    np = input("Digite o nome do produto: ")
    dp = input("Digite a descrição do produto: ")
    cp = float (input("Digite o custo do produto: "))
    cf = float (input("Digite o Custo fixo/administrativo (%): "))
    cv = float (input("Digite a comissão de vendas (%): "))
    iv = float (input("Digite os impostos (%): "))
    ml = float (input("Digite a rentabilidade (%): "))

    #confimação
    check= input(f"Confirmar cadastro?(S/N)")

    if check=='S':
        cursor.execute('''
        INSERT INTO cadastro_produto 
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
        ''', (cd, np, dp, cp, cf, cv, iv, ml))

        connection.commit()

        print(f"Cadastro bem sucedido.")
         
    if check=='N':
         print(f"Voltando ao menu.")
         menu()
         
def alterar():
    print("Digite o código do produto que deseja alterar:")
    cd = input("Código do produto: ")

    #verificar existência
    cursor.execute("SELECT * FROM cadastro_produto WHERE codigo_produto = :1", (cd,))
    produto = cursor.fetchone()

    if produto:
        print(f"Produto encontrado. Informações atuais do produto:")
        print(produto)

        print(f"Insira os dados atualizados do produto (caso queira manter algum campo, basta digitar enter):")
        np = input("Novo nome do produto: ")
        dp = input("Nova descrição do produto: ")
        cp = float(input("Novo custo do produto: ") or produto[3])
        cf = float(input("Novo Custo fixo/administrativo (%): ") or produto[4])
        cv = float(input("Nova comissão de vendas (%): ") or produto[5])
        iv = float(input("Novos impostos (%): ") or produto[6])
        ml = float(input("Nova rentabilidade (%): ") or produto[7])

        check = input("Confirmar alterações? (S/N): ")

        if check == 'S':
            cursor.execute('''
            UPDATE cadastro_produto 
            SET nome_produto = :1, descricao_produto = :2, CP = :3, CF = :4, CV = :5, IV = :6, ML = :7
            WHERE codigo_produto = :8
            ''', (np, dp, cp, cf, cv, iv, ml, cd))
            
            connection.commit()
            print("Informações do produto atualizadas com sucesso!")
        elif check == 'N':
            print("Alteração cancelada.")
            menu() 
    else:
        print("Produto não encontrado.")

def excluir():
    print("Digite o código do produto que deseja excluir:")
    cd = input("Código do produto: ")

    cursor.execute("SELECT * FROM cadastro_produto WHERE codigo_produto = :1", (cd,))
    produto = cursor.fetchone()

    if produto:
        print(f"Produto encontrado. Informações do produto a ser excluído:")
        print(produto)

        check = input("Confirmar exclusão? (S/N): ")

        if check == 'S':
            cursor.execute('''
            DELETE FROM cadastro_produto 
            WHERE codigo_produto = :1
            ''', (cd,))
            
            connection.commit()
            print("Produto excluído com sucesso!")
        elif check == 'N':
            print("Exclusão cancelada.")
            menu()
    else:
        print("Produto não encontrado.")

while True:
    menu()
    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        cadastrar()
    elif opcao == '2':
        alterar()
    elif opcao == '3':
        excluir()
    elif opcao == '4':
        lista()
    elif opcao == '0':
        print("Encerrando o programa...")
        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")

if cursor:
        cursor.close()
if connection:
        connection.close()

