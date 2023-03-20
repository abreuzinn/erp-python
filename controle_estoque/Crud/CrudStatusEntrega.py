from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from Crud.core import Conexao
from Crud.Models import StatusEntrega

class CrudStatusEntrega(object):
    def __init__(self, id="", statusEntrega="", query=""):
        self.id = id
        self.statusEntrega = statusEntrega
        self.query = query

    # recebendo ultimo id inserido
    def lastIdStatusEntrega(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            ultimo = sessao.query(StatusEntrega.id).order_by(
                desc(StatusEntrega.id)).limit(1).first()

            self.id = ultimo.id + 1

            # fechando a conexao
            sessao.close()

        except:
            self.id = 1

        return self.id

    # cadastrando categoria a receber
    def inseriStatusEntrega(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = StatusEntrega(
                id=self.id,
                status_entrega=self.statusEntrega
            )

            # add query na sessao
            sessao.add(row)

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            self.updateStatusEntrega()

    # update categoria a receber
    def updateStatusEntrega(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            row = sessao.query(StatusEntrega).get(self.id)

            # novos dados
            row.status_entrega = self.statusEntrega

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # listando todas as categorias
    def listaStatusEntrega(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = sessao.query(StatusEntrega).all()

            # convertendo variaveis em lista
            self.id = []
            self.statusEntrega = []

            # salvando dados em suas variaveis
            for row in self.query:
                self.id.append(row.id)
                self.statusEntrega.append(row.status_entrega)

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)
