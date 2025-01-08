class Produto:
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def __str__(self):
        return f"{self.nome} - R$ {self.preco:.2f} (Estoque: {self.estoque})"


class Loja:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, produto):
        for p in self.produtos:
            if p.nome == produto.nome:
                return f"\nO produto '{produto.nome}' já está cadastrado."
        self.produtos.append(produto)
        return f"\nProduto '{produto.nome}' adicionado com sucesso."

    def listar_produtos(self):
        if not self.produtos:
            return "\nAinda não há produtos cadastrados na loja."
        else:
            print(f"\nProdutos registrados: ")
            return "\n".join(str(produto) for produto in self.produtos)

    def vender_produto(self, nome, quantidade):
        for produto in self.produtos:
            if produto.nome == nome:
                if produto.estoque >= quantidade:
                    produto.estoque -= quantidade
                    total = produto.preco * quantidade
                    return f"\nVenda realizada! {quantidade} unidade(s) de '{nome}' vendida(s) por R$ {total:.2f}."
                else:
                    return f"\nEstoque insuficiente para '{nome}'. \nEstoque atual: {produto.estoque}."
        return f"\nO produto '{nome}' não está cadastrado na loja."

    def repor_estoque(self, nome, quantidade):
        for produto in self.produtos:
            if produto.nome == nome:
                produto.estoque += quantidade
                return f"\nEstoque do produto '{nome}' atualizado. Novo estoque: {produto.estoque}."
        return f"\nO produto '{nome}' não está cadastrado na loja."


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
            produtos = loja.listar_produtos()
            print(produtos)

        elif opcao == "3":
            nome = input("Digite o nome do produto a ser vendido: ")
            quantidade = int(input("Digite a quantidade a ser vendida: "))
            print(loja.vender_produto(nome, quantidade))

        elif opcao == "4":
            nome = input("Digite o nome do produto a ser reposto: ")
            quantidade = int(input("Digite a quantidade a ser adicionada ao estoque: "))
            print(loja.repor_estoque(nome, quantidade))

        elif opcao == "5":
            print("Agradecemos pela preferência")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção entre 1 e 5.")


menu_loja()