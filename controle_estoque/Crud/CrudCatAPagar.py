from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from Crud.core import Conexao
from Crud.Models import CatAPagar

class CrudCatAPagar(object):
    def __init__(self, id="", categoriaPagar="", query=""):
        self.id = id
        self.categoriaPagar = categoriaPagar
        self.query = query

    # recebe ultimo id inserido
    def lastIdCatAPagar(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()
            # query
            ultimo = sessao.query(CatAPagar.id).order_by(
                desc(CatAPagar.id)).limit(1).first()
            self.id = ultimo.id + 1
            # fechando a conexao
            sessao.close()
        except:
            self.id = 1

        return self.id

    # cadastra categoria a pagar
    def inseriCatAPagar(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()
            # query
            row = CatAPagar(
                id=self.id,
                categoria_a_pagar=self.categoriaPagar
            )
            # add query na sessao
            sessao.add(row)

            # executa a query
            sessao.commit()

            # fecha a conmexao
            sessao.close()

        except IntegrityError:
            self.updateCatAPagar()

    # update categoria a pagar
    def updateCatAPagar(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecioanndo id
            row = sessao.query(CatAPagar).get(self.id)

            # novos valores
            row.categoria_a_pagar = self.categoriaPagar

            # executa a query
            sessao.commit()

            # fecha a comnexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # lista todas as categorias a pagar
    def listaCatAPagar(self):
        try:
            # abre sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = sessao.query(CatAPagar).all()

            # converte variaveis em lista
            self.id = []
            self.categoriaPagar = []

            # salva resultado em suas lisats
            for row in self.query:
                self.id.append(row.id)
                self.categoriaPagar.append(row.categoria_a_pagar)

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)
