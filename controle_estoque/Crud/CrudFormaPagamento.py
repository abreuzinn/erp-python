from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from Crud.core import Conexao
from Crud.Models import FormaPagamento

class CrudFormaPagamento(object):
    def __init__(self, id="", formaPagamento="", query=""):
        self.id = id
        self.formaPagamento = formaPagamento
        self.query = query

    # recebendo ultimo id inserido
    def lastIdFormaPagamento(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            ultimo = sessao.query(FormaPagamento.id).order_by(
                desc(FormaPagamento.id)).limit(1).first()

            self.id = ultimo.id + 1

            # fechando a conexao
            sessao.close()

        except:
            self.id = 1

        return self.id

    # cadastrando forma pagemento
    def inseriFormaPagamento(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = FormaPagamento(
                id=self.id,
                forma_pagamento=self.formaPagamento
            )

            # add query na sessao
            sessao.add(row)

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError:
            self.updateFormaPagamento()

    # update forma pagamento
    def updateFormaPagamento(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            row = sessao.query(FormaPagamento).get(self.id)

            # query
            row.forma_pagamento = self.formaPagamento

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError:
            print('err')

    # listando todas as categorias
    def listaFormaPagamento(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = sessao.query(FormaPagamento).order_by(
                FormaPagamento.id).all()

            # convertendo variaveis em lista
            self.id = []
            self.formaPagamento = []

            for row in self.query:
                self.id.append(row.id)
                self.formaPagamento.append(row.forma_pagamento)

                # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)
