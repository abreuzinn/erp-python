from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from Crud.core import Conexao
from Crud.Models import StatusPagamento

class CrudStatusPagamento(object):
    def __init__(self, id="", statusPagamento="", query=""):
        self.id = id
        self.statusPagamento = statusPagamento
        self.query = query

    # recebendo ultimo id inserido
    def lastIdStatusPagamento(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            ultimo = sessao.query(StatusPagamento.id).order_by(
                desc(StatusPagamento.id)).limit(1).first()

            self.id = ultimo.id + 1

            # fechando a conexao
            sessao.close()

        except:
            self.id = 1

        return self.id

    # cadastrando status pagamento
    def inseriStatusPagamento(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = StatusPagamento(
                id=self.id,
                status_pagamento=self.statusPagamento
            )

            # add query na sessao
            sessao.add(row)

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError:
            self.updateStatusPagamento()

    # update status pagamento
    def updateStatusPagamento(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando
            row = sessao.query(StatusPagamento).get(self.id)

            # query
            row.status_pagamento = self.statusPagamento

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # listando todas as categorias
    def listaStatusPagamento(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = sessao.query(StatusPagamento).all()

            # convertendo variaveis em lista
            self.id = []
            self.statusPagamento = []

            # salvando resultado em suas listas
            for row in self.query:
                self.id.append(row.id)
                self.statusPagamento.append(row.status_pagamento)

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)
