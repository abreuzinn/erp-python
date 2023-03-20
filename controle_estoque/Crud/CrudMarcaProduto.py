from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from Crud.core import Conexao
from Crud.Models import MarcaProduto

class CrudMarcaProduto(object):
    def __init__(self, id="", marca_produto="", query=""):
        self.id = id
        self.marca_produto = marca_produto
        self.query = query

    # recebendo ultimo id inserido
    def lastIdMarcaProduto(self):
        try:
            # abrindo a sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            ultimo = (sessao.query(MarcaProduto).order_by(
                desc(MarcaProduto.id)).limit(1).first())

            self.id = ultimo.id + 1

            # fechando conexao
            sessao.close()

        except:

            self.id = 1

        return self.id

    # cadastrando marca produto
    def inseriMarcaProduto(self):
        try:
            # abrindo a sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = MarcaProduto(
                id=self.id,
                marca_produto=self.marca_produto
            )

            # add query na sessao
            sessao.add(row)

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError:
            self.updateMarcaProduto()

        pass

    # cadastrando marca produto
    def updateMarcaProduto(self):
        try:
            # abrindo a sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            row = sessao.query(MarcaProduto).get(self.id)

            # novos valores
            row.marca_produto = self.marca_produto

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

        pass

    # listando todas as marcas
    def listaMarcaProdutos(self):
        try:
            # abrindo a sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = sessao.query(MarcaProduto).all()

            # convertendo variaveis em lista
            self.id = []
            self.marca_produto = []

            # salvando resultado em sua lista

            for row in self.query:
                self.id.append(row.id)
                self.marca_produto.append(row.marca_produto)

            # fechando conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

        pass
