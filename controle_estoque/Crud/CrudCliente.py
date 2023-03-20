from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from Crud.core import Conexao
from Crud.Models import Cliente

class CrudCliente(object):
    def __init__(self, id="", nome="", sobrenome="", cpf="", rg="",
                 celular="", telefone="", email="", obs="", cep="",
                 endereco="", numero="", bairro="", cidade="", estado="",
                 dataEmissao="", dataEntrega="", Total="",
                 idPedido="", query=""):
        self.id = id
        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf
        self.rg = rg
        self.celular = celular
        self.telefone = telefone
        self.email = email
        self.obs = obs
        self.cep = cep
        self.endereco = endereco
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.query = query

    # recebendo última id inserido
    def lastIdCliente(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            ultimo = sessao.query(Cliente).order_by(
                desc(Cliente.id)).limit(1).first()

            self.id = ultimo.id + 1

            # fechando conexao
            sessao.close()

            pass

        except:

            self.id = 1

        return self.id

    # cadastro Cliente
    def inseriCliente(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = Cliente(
                id=self.id,
                nome=self.nome,
                sobrenome=self.sobrenome,
                cpf=self.cpf,
                rg=self.rg,
                celular=self.celular,
                telefone=self.telefone,
                email=self.email,
                obs=self.obs,
                cep=self.cep,
                endereco=self.endereco,
                numero=self.numero,
                bairro=self.bairro,
                cidade=self.cidade,
                estado=self.estado
            )

            # executa query
            sessao.add(row)
            sessao.commit()

            # fecha sessao
            sessao.close()

            pass

        except IntegrityError:

            self.updateCliente()

            pass

    #  update cliente
    def updateCliente(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            query = sessao.query(Cliente).get(self.id)

            # novos valores
            query.nome = self.nome
            query.sobrenome = self.sobrenome
            query.cpf = self.cpf
            query.rg = self.rg
            query.celular = self.celular
            query.telefone = self.telefone
            query.email = self.email
            query.obs = self.obs
            query.cep = self.cep
            query.endereco = self.endereco
            query.numero = self.numero
            query.bairro = self.bairro
            query.cidade = self.cidade
            query.estado = self.estado

            # executa query
            sessao.commit()

            # fecha sessao
            sessao.close()

            pass

        except IntegrityError as err:

            print(err)

            pass

    # Buscando cliente por ID
    def selectClienteId(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            busca = sessao.query(Cliente).get(self.id)

            # salvando resultado da query
            self.id = busca.id
            self.nome = busca.nome
            self.sobrenome = busca.sobrenome
            self.cpf = busca.cpf
            self.rg = busca.rg
            self.celular = busca.celular
            self.telefone = busca.telefone
            self.email = busca.email
            self.obs = busca.obs
            self.cep = busca.cep
            self.endereco = busca.endereco
            self.numero = busca.numero
            self.bairro = busca.bairro
            self.cidade = busca.cidade
            self.estado = busca.estado

            # fechando conexao
            sessao.close()

            pass

        except:

            pass

        pass

    # buscando cliente por nome
    def listaCliente(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            query = sessao.query(Cliente).filter(
                Cliente.nome.contains(self.nome))
            query.all()

            # convertendo variaveis em lista
            self.id = []
            self.nome = []
            self.sobrenome = []
            self.celular = []
            self.telefone = []
            self.email = []

            # salvando resultado da query e suas listas
            for row in query:
                self.id.append(row.id)
                self.nome.append(row.nome)
                self.sobrenome.append(row.sobrenome)
                self.celular.append(row.celular)
                self.telefone.append(row.telefone)
                self.email.append(row.email)

            # fechando a conexao
            sessao.close()

            pass

        except IntegrityError as err:

            print(err)

            pass

    # lista AutoComplete cliente
    def autoCompleteCliente(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = sessao.query(Cliente).filter(
                Cliente.nome.contains(self.nome))
            self.query.all()

            # convertendo variavel em lista
            self.nome = []

            # salvando resultado em lista
            for row in self.query:
                self.nome.append(row.nome)

            # fechando conexao
            sessao.close()

            pass

        except IntegrityError as err:

            print(err)

            pass

    # busca cliente por nome
    def buscaClienteNome(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            self.query = sessao.query(Cliente).filter(
                Cliente.nome == self.nome).first()

            # salvando Resultado
            self.id = self.query.id
            self.nome = self.query.nome
            self.celular = self.query.celular

            # fechando conexao
            sessao.close()

        except IntegrityError as err:
            print(err)
