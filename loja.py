import sqlite3

class Produto:
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def __str__(self):
        return f"{self.nome} - R$ {self.preco:.2f} (Estoque: {self.estoque})"


class Loja:
    def __init__(self):
        self.conexao = sqlite3.connect("loja.db")
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

#Criando tabela para armazenar dados no banco
    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE,
                preco REAL,
                estoque INTEGER
            )
        """)
        self.conexao.commit()

    def adicionar_produto(self, produto):
        try:
            self.cursor.execute("INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)",
                                (produto.nome, produto.preco, produto.estoque))
            self.conexao.commit()
            return f"\nProduto '{produto.nome}' adicionado com sucesso."
        except sqlite3.IntegrityError:
            return f"\nO produto '{produto.nome}' já está cadastrado."

    def listar_produtos(self):
        self.cursor.execute("SELECT nome, preco, estoque FROM produtos")
        produtos = self.cursor.fetchall()
        if not produtos:
            return "\nAinda não há produtos cadastrados na loja."
        else:
            resultado = "\nProdutos registrados:\n"
            for produto in produtos:
                resultado += f"{produto[0]} - R$ {produto[1]:.2f} (Estoque: {produto[2]})\n"
            return resultado

    def vender_produto(self, nome, quantidade):
        self.cursor.execute("SELECT estoque, preco FROM produtos WHERE nome = ?", (nome,))
        produto = self.cursor.fetchone()
        if produto:
            estoque, preco = produto
            if estoque >= quantidade:
                novo_estoque = estoque - quantidade
                self.cursor.execute("UPDATE produtos SET estoque = ? WHERE nome = ?", (novo_estoque, nome))
                self.conexao.commit()
                total = preco * quantidade
                return f"\nVenda realizada! {quantidade} unidade(s) de '{nome}' vendida(s) por R$ {total:.2f}."
            else:
                return f"\nEstoque insuficiente para '{nome}'. Estoque atual: {estoque}."
        return f"\nO produto '{nome}' não está cadastrado na loja."

    def repor_estoque(self, nome, quantidade):
        self.cursor.execute("SELECT estoque FROM produtos WHERE nome = ?", (nome,))
        produto = self.cursor.fetchone()
        if produto:
            novo_estoque = produto[0] + quantidade
            self.cursor.execute("UPDATE produtos SET estoque = ? WHERE nome = ?", (novo_estoque, nome))
            self.conexao.commit()
            return f"\nEstoque do produto '{nome}' atualizado. Novo estoque: {novo_estoque}."
        return f"\nO produto '{nome}' não está cadastrado na loja."

    def fechar_conexao(self):
        self.conexao.close()


def menu_loja():
    loja = Loja()

    while True:
        print("\nMenu da Loja:")
        print("1. Adicionar Produto")
        print("2. Listar Produtos")
        print("3. Vender Produto")
        print("4. Repor Estoque")
        print("5. Sair")

        opcao = input("\nEscolha uma opção (1-5): ")

        if opcao == "1":
            nome = input("Digite o nome do produto: ")
            preco = float(input("Digite o preço do produto: R$ "))
            estoque = int(input("Digite a quantidade em estoque: "))
            produto = Produto(nome, preco, estoque)
            print(loja.adicionar_produto(produto))

        elif opcao == "2":
            print(loja.listar_produtos())

        elif opcao == "3":
            nome = input("Digite o nome do produto a ser vendido: ")
            quantidade = int(input("Digite a quantidade a ser vendida: "))
            print(loja.vender_produto(nome, quantidade))

        elif opcao == "4":
            nome = input("Digite o nome do produto a ser reposto: ")
            quantidade = int(input("Digite a quantidade a ser adicionada ao estoque: "))
            print(loja.repor_estoque(nome, quantidade))

        elif opcao == "5":
            print("Agradecemos pela preferência!")
            loja.fechar_conexao()
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção entre 1 e 5.")


menu_loja()