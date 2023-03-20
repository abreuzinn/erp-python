from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from Crud.core import Conexao
from Crud.Models import CatAReceber

class CrudCatAReceber(object):
    def __init__(self, id="", categoriaReceber="", query=""):
        self.id = id
        self.categoriaReceber = categoriaReceber
        self.query = query

    # recebe ultimo id inserido

    def lastIdCatAReceber(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            ultimo = sessao.query(CatAReceber.id).order_by(
                desc(CatAReceber.id)).limit(1).first()

            self.id = ultimo.id + 1

            # fechando a conexao
            sessao.close()

        except:
            self.id = 1

        return self.id

    # cadastrando categoria a receber

    def inseriCatAReceber(self):
        try:

            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = CatAReceber(
                id=self.id,
                categoria_a_receber=self.categoriaReceber
            )

            # add query na sessao
            sessao.add(row)

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError:
            self.updateCatAReceber()

    # update categoria a pagar
    def updateCatAReceber(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            row = sessao.query(CatAReceber).get(self.id)

            # novos valores
            row.categoria_a_receber = self.categoriaReceber

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # listando todas as categorias
    def listaCatAReceber(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = sessao.query(CatAReceber).all()

            # convertendo variaveis em lista
            self.id = []
            self.categoriaReceber = []

            # salvando resultado em suas lisats
            for row in self.query:
                self.id.append(row.id)
                self.categoriaReceber.append(row.categoria_a_receber)

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)
