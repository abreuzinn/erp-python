from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from sqlalchemy import func
from Crud.core import Conexao
from Crud.Models import Produto, CategoriaProduto, MarcaProduto

class CrudProduto(object):

    def __init__(self, id="", produto="", imagem="",
                 categoria="", marca="", estoqueMinimo="", estoqueMaximo="",
                 qtdeProduto="", valorCompra="", valorUnitario="",
                 valorAtacado="", qtdeAtacado="", obsProduto="", query=""):
        self.id = id
        self.produto = produto
        self.imagem = imagem
        self.categoria = categoria
        self.marca = marca
        self.estoqueMinimo = estoqueMinimo
        self.estoqueMaximo = estoqueMaximo
        self.qtdeProduto = qtdeProduto
        self.valorCompra = valorCompra
        self.valorUnitario = valorUnitario
        self.valorAtacado = valorAtacado
        self.qtdeAtacado = qtdeAtacado
        self.obsProduto = obsProduto
        self.query = query

    # recendo ultimo id inserido
    def lastIdProduto(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            ultimo = sessao.query(Produto.id).order_by(
                desc(Produto.id)).limit(1).first()
            self.id = ultimo.id + 1

            # fechando conexao
            sessao.close()

        except:

            self.id = 1

        return self.id

    # cadastro de produto
    def inseriProduto(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = Produto(
                id=self.id,
                produto=self.produto,
                imagem=self.imagem,
                categoria=self.categoria,
                marca=self.marca,
                estoque_minimo=self.estoqueMinimo,
                estoque_maximo=self.estoqueMaximo,
                valor_compra=self.valorCompra,
                valor_unitario=self.valorUnitario,
                valor_atacado=self.valorAtacado,
                qtde_atacado=self.qtdeAtacado,
                obs=self.obsProduto

            )

            # add query na sessao
            sessao.add(row)

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError:
            self.updateProduto()

        pass

    # update de produto
    def updateProduto(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            row = sessao.query(Produto).get(self.id)

            # novos valores
            row.produto = self.produto
            row.imagem = self.imagem
            row.categoria = self.categoria
            row.marca = self.marca
            row.estoque_minimo = self.estoqueMinimo
            row.estoque_maximo = self.estoqueMaximo
            row.valor_compra = self.valorCompra
            row.valor_unitario = self.valorUnitario
            row.valor_atacado = self.valorAtacado
            row.qtde_atacado = self.qtdeAtacado
            row.obs = self.obsProduto

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

        pass

    # busca por id
    def selectProdutoId(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            busca = sessao.query(Produto).get(self.id)

            # salvando resultado da query
            self.id = busca.id
            self.produto = busca.produto
            self.imagem = busca.imagem
            self.categoria = busca.categoria
            self.marca = busca.marca
            self.estoqueMinimo = busca.estoque_minimo
            self.estoqueMaximo = busca.estoque_maximo
            self.qtdeProduto = busca.qtde
            self.valorCompra = busca.valor_compra
            self.valorUnitario = busca.valor_unitario
            self.valorAtacado = busca.valor_atacado
            self.qtdeAtacado = busca.qtde_atacado
            self.obsProduto = busca.obs

            # fechando a Conexao
            sessao.close()

            pass

        except:
            pass

    # busca produto por nome
    def listaProduto(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = (sessao.query(Produto.id, Produto.produto,
                                       Produto.estoque_minimo, Produto.qtde,
                                       Produto.valor_unitario,
                                       Produto.valor_atacado,
                                       Produto.qtde_atacado,
                                       MarcaProduto.marca_produto
                                       )
                          .join(MarcaProduto)
                          .filter(Produto.produto.contains(self.produto))
                          )
            self.query.all()

            # convertendo variaveis em lista
            self.id = []
            self.produto = []
            self.marca = []
            self.estoqueMinimo = []
            self.qtdeProduto = []
            self.valorUnitario = []
            self.valorAtacado = []
            self.qtdeAtacado = []

            # salvando resultado da query e suas listas
            for row in self.query:
                self.id.append(row.id)
                self.produto.append(row.produto)
                self.marca.append(row.marca_produto)
                self.estoqueMinimo.append(row.estoque_minimo)
                self.qtdeProduto.append(row.qtde)
                self.valorUnitario.append(row.valor_unitario)
                self.valorAtacado.append(row.valor_atacado)
                self.qtdeAtacado.append(row.qtde_atacado)

           # fechando a conexao
            sessao.close()

            pass

        except IntegrityError as err:

            print(err)

            pass

    # busca nome AutoComplete
    def autoCompleteProduto(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = (sessao.query(Produto.produto).filter(
                Produto.produto.contains(self.produto)))
            self.query.all()

            # convertendo variavel em lista
            self.produto = []

            # salvando resultado em lista
            for row in self.query:
                self.produto.append(row.produto)

            # fechando conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # busca produto por nome Autocomplete
    def buscaProdutoNome(self):
        try:
            # abrindo a sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = sessao.query(Produto.id, Produto.produto).filter(
                Produto.produto == self.produto).first()

            # salvando resultado
            self.id = self.query.id

            # fechando a conexao
            sessao.close()

            pass
        except:
            self.produto = 'Produto Não Encontrado'
            pass

    # retirando produto do estoque
    def retiradaEstoque(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id produto
            row = sessao.query(Produto).get(self.id)
            row.qtde = row.qtde - float(self.qtdeProduto)

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # entrada produto no estoque
    def entradaEstoque(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id produto
            row = sessao.query(Produto).get(self.id)
            row.qtde = row.qtde + float(self.qtdeProduto)
            row.valorCompra = self.valorCompra
            row.obs = self.obsProduto

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # listar produtos com estoque abaixo do minimo
    def listaEstoqueBaixo(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = sessao.query(Produto).filter(
                Produto.qtde < Produto.estoque_minimo).count()

            # fechando sessao
            sessao.close()

        except IntegrityError as err:
            print(err)

        return row

    # lista total de produtos
    def totalProdutoCadastrado(self):
        try:

            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = sessao.query(Produto).count()

            # fechando sessao
            sessao.close()

        except IntegrityError as err:
            print(err)

        return row
