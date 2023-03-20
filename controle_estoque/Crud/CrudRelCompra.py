from sqlalchemy.exc import IntegrityError
from Crud.core import Conexao
from Crud.Models import RelacaoCompra, Produto

class CrudRelCompra(object):
    def __init__(self, id="", idCompra="", idProduto="", produto="", qtde="", valorUnitario="", valorTotal="", obs="", query=""):
        self.id = id
        self.idCompra = idCompra
        self.idProduto = idProduto
        self.produto = produto
        self.qtde = qtde
        self.valorUnitario = valorUnitario
        self.valorTotal = valorTotal
        self.obs = obs
        self.query = query

    # cadastrando item referente a compra
    def inseriItens(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = RelacaoCompra(
                id=self.id,
                id_compra=self.idCompra,
                id_produto=self.idProduto,
                qtde=self.qtde,
                valor_unitario=self.valorUnitario,
                valor_total=self.valorTotal,
                obs=self.obs
            )

            # add query sessao
            sessao.add(row)

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError:
            self.updateItens()

    # update item referente a compra
    def updateItens(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            row = sessao.query(RelacaoCompra).get(self.id)

            # novos valores
            row.id_compra = self.idCompra
            row.id_produto = self.idProduto
            row.qtde = self.qtde
            row.valor_unitario = self.valorUnitario
            row.valor_total = self.valorTotal
            row.obs = self.obs

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # lista itens por id de compra
    def listaItens(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = (sessao.query(
                RelacaoCompra.id, RelacaoCompra.id_compra,
                RelacaoCompra.id_produto, RelacaoCompra.qtde,
                RelacaoCompra.valor_unitario, RelacaoCompra.valor_total,
                RelacaoCompra.obs,
                Produto.produto)
                .join(Produto)
                .filter(RelacaoCompra.id_compra == self.idCompra))
            self.query.all()

            # convertendo variaveis em lista
            self.id = []
            self.idCompra = []
            self.idProduto = []
            self.produto = []
            self.qtde = []
            self.valorUnitario = []
            self.valorTotal = []
            self.obs = []

            # salvando resultado da query e suas listas
            for row in self.query:
                self.id.append(row.id)
                self.idCompra.append(row.id_compra)
                self.idProduto.append(row.id_produto)
                self.produto.append(row.produto)
                self.qtde.append(row.qtde)
                self.valorUnitario.append(row.valor_unitario)
                self.valorTotal.append(row.valor_total)
                self.obs.append(row.obs)

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # deletando item
    def delItem(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            self.query = sessao.query(RelacaoCompra).get(self.id)

            if self.query:
                # add query na sessao
                sessao.delete(self.query)

                # executando a query
                sessao.commit()

            # fechando conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

        pass
