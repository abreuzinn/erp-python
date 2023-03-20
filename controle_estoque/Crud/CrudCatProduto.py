from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from Crud.core import Conexao
from Crud.Models import CategoriaProduto

class CrudCatProduto(object):
    def __init__(self, id="", categoria_produto="", query=""):
        self.id = id
        self.categoria_produto = categoria_produto
        self.query = query

    # recebendo ultimo id inserido
    def lastIdCatProduto(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            ultimo = sessao.query(CategoriaProduto).order_by(
                desc(CategoriaProduto.id)).limit(1).first()
            self.id = ultimo.id + 1

            # fechando conexao
            sessao.close()

        except:
            self.id = 1

        return self.id

    # cadastrando categoria produto

    def inseriCatProduto(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = CategoriaProduto(
                id=self.id,
                categoria_produto=self.categoria_produto
            )

            # salvando query na sessao
            sessao.add(row)

            # executando query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError:
            self.updateCatProduto()

    # cadastrando categoria produto

    def updateCatProduto(self):
        try:
            # abrindo a sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            row = sessao.query(CategoriaProduto).get(self.id)

            # novos valores
            row.categoria_produto = self.categoria_produto

            # executando a query
            sessao.commit()

            # fechando a Conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # listando todas as categorias

    def listaCatProduto(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = sessao.query(CategoriaProduto).all()

            # convertendo variaveis em lista
            self.id = []
            self.categoria_produto = []

            # salvando resultado em sua lista

            for row in self.query:
                self.id.append(row.id)
                self.categoria_produto.append(row.categoria_produto)

            # Fechando Conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

            pass
