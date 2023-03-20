from datetime import date
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from sqlalchemy import case
from sqlalchemy import func
from Crud.core import Conexao
from Crud.Models import ContaAPagar
from Crud.Models import Fornecedor
from Crud.Models import StatusPagamento
from Crud.Models import CatAPagar
from Crud.Models import FormaPagamento

class CrudContaAPagar(object):
    def __init__(self, id="", idCompra="", idFornecedor="", descricao="",
                 obs="", categoria="", dataVencimento="", valor="",
                 formaPagamento="", dataPagamento="", valorPago="",
                 statusPagamento="", query="", dataFim="", valorAPagar="",
                 nomeFantasia="", telefone=""):
        self.id = id
        self.idCompra = idCompra
        self.idFornecedor = idFornecedor
        self.nomeFantasia = nomeFantasia
        self.telefone = telefone
        self.descricao = descricao
        self.obs = obs
        self.categoria = categoria
        self.dataVencimento = dataVencimento
        self.valor = valor
        self.formaPagamento = formaPagamento
        self.dataPagamento = dataPagamento
        self.valorPago = valorPago
        self.statusPagamento = statusPagamento
        self.query = query
        self.dataFim = dataFim
        self.valorAPagar = valorAPagar

    # recebendo ultimo id
    def lastIdContaAPagar(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            ultimo = (sessao.query(ContaAPagar.id).order_by(
                desc(ContaAPagar.id)).limit(1).first())
            self.id = ultimo.id + 1

            # fechando sessao
            sessao.close()

        except:
            self.id = 1

        return self.id

    # Cadastrando Parcelas de Compra
    def inseriParcelaCompra(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = ContaAPagar(
                id=self.id,
                id_compra=self.idCompra,
                id_fornecedor=self.idFornecedor,
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

    # lista de  parcelas de compra
    def listaParcelas(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = (sessao.query(ContaAPagar.__table__,
                                       StatusPagamento.status_pagamento,
                                       FormaPagamento.forma_pagamento.label('fpaga'))
                          .join(StatusPagamento)
                          .join(FormaPagamento)
                          .filter(
                ContaAPagar.id_compra == self.idCompra))
            self.query.all()

            # convertendo variaveis em lista
            self.id = []
            self.descricao = []
            self.dataVencimento = []
            self.valor = []
            self.idFormaPagamento = []
            self.formaPagamento = []
            self.valorPago = []
            self.idStatusPagamento = []
            self.statusPagamento = []

            # salvando resultado da query e suas listas
            for row in self.query:
                self.id.append(row.id)
                self.descricao.append(row.descricao)
                self.dataVencimento.append(row.data_vencimento)
                self.valor.append(row.valor)
                self.idFormaPagamento.append(row.forma_pagamento)
                self.formaPagamento.append(row.fpaga)
                self.valorPago.append(row.valor_pago)
                self.idStatusPagamento.append(row.pagamento)
                self.statusPagamento.append(row.status_pagamento)

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # Cadastrando Conta a Pagar
    def inseriContaAPagar(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = ContaAPagar(
                id=self.id,
                id_fornecedor=self.idFornecedor,
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
            self.updateContaAPagar()

    # update conta a pagar
    def updateContaAPagar(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            row = sessao.query(ContaAPagar).get(self.id)

            # novos valores
            row.id_fornecedor = self.idFornecedor
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

    # buscando conta a pagar por vencimento, fornecedor e status
    def listaContaAPagar(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = (sessao.query(ContaAPagar.__table__,
                                       Fornecedor.nome_fantasia,
                                       Fornecedor.telefone,
                                       StatusPagamento.status_pagamento)
                          .join(Fornecedor)
                          .join(StatusPagamento)
                          .filter(ContaAPagar.data_vencimento.between(
                              self.dataVencimento, self.dataFim),
                ContaAPagar.pagamento == self.statusPagamento)
            )
            self.query.all()

            # convertendo variaveis em lista
            self.id = []
            self.nomeFantasia = []
            self.telefone = []
            self.descricao = []
            self.dataVencimento = []
            self.valor = []
            self.valorPago = []
            self.idStatusPagamento = []
            self.statusPagamento = []

            # salvando resultado em suas listas
            for row in self.query:

                self.id.append(row.id)
                self.nomeFantasia.append(row.nome_fantasia)
                self.telefone.append(row.telefone)
                self.descricao.append(row.descricao)
                self.dataVencimento.append(
                    date.strftime(row.data_vencimento, "%d-%m-%Y"))
                self.valor.append(row.valor)
                self.valorPago.append(row.valor_pago)
                self.idStatusPagamento.append(row.pagamento)
                self.statusPagamento.append(row.status_pagamento)

            # fechando a Conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # selecionando conta a pagar por id
    def selectContaID(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = sessao.query(ContaAPagar).get(self.id)

            # salvando resultado em variaveis
            self.id = row.id
            self.idFornecedor = row.id_fornecedor
            self.descricao = row.descricao
            self.obs = row.obs
            self.categoria = row.categoria
            self.dataVencimento = row.data_vencimento
            self.valor = row.valor
            self.idFormaPagamento = row.forma_pagamento
            self.dataPagamento = row.data_pagamento
            self.valorPago = row.valor_pago
            self.idStatusPagamento = row.pagamento

            # fechando Conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # pagar conta
    def pagarConta(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            row = sessao.query(ContaAPagar).get(self.id)

            # update status se valor pago igual ou maior que valor parcela
            status = case([
                (ContaAPagar.valor_pago >= ContaAPagar.valor, '1')
            ], else_='2'
            )

            # novos valores
            row.forma_pagamento = self.formaPagamento
            row.data_pagamento = self.dataPagamento
            row.valor_pago = ContaAPagar.valor_pago + self.valorPago
            row.pagamento = status

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

        pass

    """  Obtendo Movimentação financeira """

    # total a receber referente a data selecionada
    def movDespesa(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = (sessao.query(func.COALESCE(
                func.SUM(ContaAPagar.valor_pago), 0
            ).label('valorPago'))

                .filter(ContaAPagar.data_pagamento.between(
                    self.dataPagamento, self.dataFim))
            )
            row.all()

            # salvando resultado
            for row in row:
                self.valorPago = row.valorPago

            # query
            row = (sessao.query(func.COALESCE(
                func.SUM(ContaAPagar.valor), 0
            ).label('valorAPagar'))

                .filter(ContaAPagar.data_vencimento.between(
                    self.dataPagamento, self.dataFim))
            )
            row.all()

            # salvando resultado
            for row in row:
                self.valorAPagar = row.valorAPagar

            # fechando a conexao
            sessao.close

        except IntegrityError as err:
            print(err)

    # detalhes entrada por categoria de receita
    def detalheDespesa(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = (sessao.query(func.SUM(ContaAPagar.valor_pago),
                                       CatAPagar.categoria_a_pagar,
                                       FormaPagamento.forma_pagamento)
                          .join(CatAPagar)
                          .join(FormaPagamento)
                          .filter(ContaAPagar.data_pagamento
                                  .between(self.dataPagamento,
                                           self.dataFim))
                          .group_by(ContaAPagar.forma_pagamento, ContaAPagar.categoria)
                          )

            # convertendo variaveis em lista
            self.valorPago = []
            self.categoria = []
            self.formaPagamento = []

            # salvando resultado em suas listas
            for row in self.query:
                self.categoria.append(row.categoria_a_pagar)
                self.valorPago.append(row[0])
                self.formaPagamento.append(row.forma_pagamento)

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # total a pagar hoje
    def aPagarHoje(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = (sessao.query(func.COALESCE(
                func.SUM(ContaAPagar.valor), 0).label('total'))
                .filter(ContaAPagar.data_vencimento == date.today(), ContaAPagar.pagamento == 2))

            # salvando resultado
            for row in row:
                self.valorAPagar = row.total

        except IntegrityError as err:
            print(err)

        return self.valorAPagar
