from datetime import date
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from sqlalchemy import case
from sqlalchemy import func
from Crud.core import Conexao
from Crud.Models import ContaAReceber
from Crud.Models import Cliente
from Crud.Models import StatusPagamento
from Crud.Models import CatAReceber
from Crud.Models import FormaPagamento

class CrudContaAReceber(object):
    def __init__(self, id="", idVenda="", idCliente="", descricao="",
                 obs="", categoria="", dataVencimento="",
                 valor="", idFormaPagamento="",  formaPagamento="",
                 dataRecebimento="", valorRecebido="", idStatusPagamento="",
                 statusPagamento="", query="", dataFim="", valorAReceber="",
                 nomeCliente="", telefoneCliente=""):
        self.id = id
        self.idVenda = idVenda
        self.idCliente = idCliente
        self.descricao = descricao
        self.obs = obs
        self.categoria = categoria
        self.dataVencimento = dataVencimento
        self.valor = valor
        self.idFormaPagamento = idFormaPagamento
        self.formaPagamento = formaPagamento
        self.dataRecebimento = dataRecebimento
        self.valorRecebido = valorRecebido
        self.idStatusPagamento = idStatusPagamento
        self.statusPagamento = statusPagamento
        self.query = query
        self.dataFim = dataFim
        self.valorAReceber = valorAReceber
        self.nomeCliente = nomeCliente
        self.telefoneCliente = telefoneCliente

    # Recebendo ultimo id

    def lastIdContaAReceber(self):

        try:

            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            ultimo = (sessao.query(ContaAReceber)
                      .order_by(desc(ContaAReceber.id)).limit(1).first())
            self.id = ultimo.id + 1

        except:

            self.id = 1

        return self.id

    # Cadastrando Parcelas de Venda

    def inseriParcelaVenda(self):

        try:

            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = ContaAReceber(
                id=self.id,
                id_venda=self.idVenda,
                id_cliente=self.idCliente,
                descricao=self.descricao,
                categoria=1,
                data_vencimento=self.dataVencimento,
                valor=self.valor,
                forma_pagamento=self.formaPagamento
            )

            # add query sessao
            sessao.add(row)

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # lista de  parcelas de venda
    def listaParcelas(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = (sessao.query(ContaAReceber.__table__,
                                       StatusPagamento.status_pagamento,
                                       FormaPagamento.forma_pagamento.label('fpaga'))
                          .join(StatusPagamento)
                          .join(FormaPagamento)
                          .filter(
                ContaAReceber.id_venda == self.idVenda))
            self.query.all()

            # convertendo variaveis em lista
            self.id = []
            self.descricao = []
            self.dataVencimento = []
            self.valor = []
            self.formaPagamento = []
            self.idFormaPagamento = []
            self.valorRecebido = []
            self.statusPagamento = []
            self.idStatusPagamento = []

            # salvando resultado da query e suas listas
            for row in self.query:
                self.id.append(row.id)
                self.descricao.append(row.descricao)
                self.dataVencimento.append(row.data_vencimento)
                self.valor.append(row.valor)
                self.formaPagamento.append(row.fpaga)
                self.idFormaPagamento.append(row.forma_pagamento)
                self.valorRecebido.append(row.valor_recebido)
                self.idStatusPagamento.append(row.pagamento)
                self.statusPagamento.append(row.status_pagamento)

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # cadastrando conta a receber
    def inseriContaAReceber(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = ContaAReceber(
                id=self.id,
                id_cliente=self.idCliente,
                descricao=self.descricao,
                obs=self.obs,
                categoria=self.categoria,
                data_vencimento=self.dataVencimento,
                valor=self.valor,
                forma_pagamento=self.formaPagamento
            )

            # add query a sessao
            sessao.add(row)

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError:
            self.updateContaAReceber()

    # update conta a receber
    def updateContaAReceber(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            row = sessao.query(ContaAReceber).get(self.id)

            # novos valores
            row.id_cliente = self.idCliente
            row.descricao = self.descricao
            row.obs = self.obs
            row.categoria = self.categoria
            row.data_vencimento = self.dataVencimento
            row.valor = self.valor
            row.forma_pagamento = self.formaPagamento

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # buscando conta a pagar por vencimento, cliente e status
    def listaContaAReceber(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = (sessao.query(ContaAReceber.__table__,
                                       Cliente.nome,
                                       Cliente.celular,
                                       StatusPagamento.status_pagamento)
                          .join(Cliente)
                          .join(StatusPagamento)
                          .filter(ContaAReceber.data_vencimento.between(
                              self.dataVencimento, self.dataFim),
                ContaAReceber.pagamento == self.statusPagamento)
            )

            # convertendo variaveis em lista
            self.id = []
            self.nomeCliente = []
            self.telefoneCliente = []
            self.descricao = []
            self.dataVencimento = []
            self.valor = []
            self.valorRecebido = []
            self.idStatusPagamento = []
            self.statusPagamento = []

            # salvando resultado em suas listas
            for row in self.query:

                self.id.append(row.id)
                self.nomeCliente.append(row.nome)
                self.telefoneCliente.append(row.celular)
                self.descricao.append(row.descricao)
                self.dataVencimento.append(
                    date.strftime(row.data_vencimento, "%d-%m-%Y"))
                self.valor.append(row.valor)
                self.valorRecebido.append(row.valor_recebido)
                self.idStatusPagamento.append(row.pagamento)
                self.statusPagamento.append(row.status_pagamento)

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

        pass

    # selecionando conta a receber por id
    def selectContaID(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = sessao.query(ContaAReceber).get(self.id)

            # salvando resultado em variaveis
            self.id = row.id
            self.idCliente = row.id_cliente
            self.descricao = row.descricao
            self.obs = row.obs
            self.categoria = row.categoria
            self.dataVencimento = row.data_vencimento
            self.valor = row.valor
            self.idFormaPagamento = row.forma_pagamento
            self.dataRecebimento = row.data_recebimento
            self.valorRecebido = row.valor_recebido
            self.idStatusPagamento = row.pagamento

            # fechando conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # receber conta
    def receberConta(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            row = sessao.query(ContaAReceber).get(self.id)

            # update status se valor recebido igual ou maior que valor parcela
            status = case([
                (ContaAReceber.valor_recebido >= row.valor, '1')
            ], else_='2'
            )

            # query
            row.forma_pagamento = self.formaPagamento
            row.data_recebimento = self.dataRecebimento
            row.valor_recebido = ContaAReceber.valor_recebido + self.valorRecebido
            row.pagamento = status

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    """  Obtendo Movimentação financeira """

    # total a receber referente a data selecionada
    def movEntrada(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = (sessao.query(func.COALESCE(
                func.SUM(ContaAReceber.valor_recebido), 0
            ).label('valorRecebido'))

                .filter(ContaAReceber.data_recebimento.between(
                    self.dataRecebimento, self.dataFim))
            )
            row.all()

            # salvando resultado
            for row in row:
                self.valorRecebido = row.valorRecebido

            # query
            row = (sessao.query(func.COALESCE(
                func.SUM(ContaAReceber.valor), 0
            ).label('valorAReceber'))

                .filter(ContaAReceber.data_vencimento.between(
                    self.dataRecebimento, self.dataFim))
            )
            row.all()

            # salvando resultado
            for row in row:
                self.valorAReceber = row.valorAReceber

            # fechando a conexao
            sessao.close

        except IntegrityError as err:
            print(err)

        pass

    # detalhes entrada por categoria de receita
    def detalheEntrada(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = (sessao.query(func.SUM(ContaAReceber.valor_recebido).label('entrada'),
                                       CatAReceber.categoria_a_receber,
                                       FormaPagamento.forma_pagamento)
                          .join(CatAReceber)
                          .join(FormaPagamento)
                          .filter(ContaAReceber.data_recebimento
                                  .between(self.dataRecebimento,
                                           self.dataFim))
                          .group_by(ContaAReceber.forma_pagamento, ContaAReceber.categoria)
                          )

            # convertendo variaveis em lista
            self.valorRecebido = []
            self.categoria = []
            self.formaPagamento = []

            # salvando resultado em suas listas
            for row in self.query:
                self.categoria.append(row.categoria_a_receber)
                self.valorRecebido.append(row.entrada)
                self.formaPagamento.append(row.forma_pagamento)

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # total a receber hoje
    def aReceberHoje(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = (sessao.query(func.COALESCE(
                func.SUM(ContaAReceber.valor), 0).label('total'))
                .filter(ContaAReceber.data_vencimento == date.today(), ContaAReceber.pagamento == 2))

            # salvando resultado
            for row in row:
                self.valorAReceber = row.total

        except IntegrityError as err:
            print(err)

        return self.valorAReceber
