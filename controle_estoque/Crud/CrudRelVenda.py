from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from sqlalchemy import case
from Crud.core import Conexao
from Crud.Models import RelacaoVenda, Produto

class CrudRelVenda(object):
    def __init__(self, id="", idVenda="", idProduto="", produto="", qtde="",
                 valorUnitario="", valorTotal="", obs="", query=""):
        self.id = id
        self.idVenda = idVenda
        self.idProduto = idProduto
        self.produto = produto
        self.qtde = qtde
        self.valorUnitario = valorUnitario
        self.valorTotal = valorTotal
        self.obs = obs
        self.query = query

    # cadastrando item referente a venda
    def inseriItens(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = RelacaoVenda(
                id=self.id,
                id_venda=self.idVenda,
                id_produto=self.idProduto,
                qtde=self.qtde,
                valor_unitario=self.valorUnitario,
                valor_total=self.valorTotal,
                obs=self.obs
            )

            # adicionando query na sessao
            sessao.add(row)

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError:
            self.updateItensVenda()

    # update item referente a Venda
    def updateItensVenda(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            row = sessao.query(RelacaoVenda).get(self.id)

            # Novos Valores
            row.id_venda = self.idVenda
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

    # lista itens por id de venda
    def listaItens(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = (sessao.query(
                RelacaoVenda.id, RelacaoVenda.id_venda,
                RelacaoVenda.id_produto, RelacaoVenda.qtde,
                RelacaoVenda.valor_unitario, RelacaoVenda.valor_total,
                RelacaoVenda.obs,
                Produto.produto)
                .join(Produto)
                .filter(RelacaoVenda.id_venda == self.idVenda))
            self.query.all()

            # convertendo variaveis em lista
            self.id = []
            self.idVenda = []
            self.idProduto = []
            self.produto = []
            self.qtde = []
            self.valorUnitario = []
            self.valorTotal = []
            self.obs = []

            # salvando resultado da query e suas listas
            for row in self.query:
                self.id.append(row.id)
                self.idVenda.append(row.id_venda)
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
            self.query = (sessao.query(RelacaoVenda).get(self.id))
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
