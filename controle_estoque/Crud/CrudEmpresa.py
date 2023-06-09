from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from Crud.core import Conexao
from Crud.Models import Empresa

class CrudEmpresa(object):

    def __init__(self, id="", nomeFantasia="", razaoSocial="", cnpj="",
                 inscEstadual="", telefone="", email="", site="", obs="",
                 cep="", endereco="", numero="", bairro="", cidade="",
                 estado="",  titulo="", subtitulo="", logo="",
                 query=""):

        self.id = id
        self.nomeFantasia = nomeFantasia
        self.razaoSocial = razaoSocial
        self.cnpj = cnpj
        self.inscEstadual = inscEstadual
        self.telefone = telefone
        self.email = email
        self.site = site
        self.obs = obs
        self.cep = cep
        self.endereco = endereco
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.logo = logo
        self.query = query

    # recebendo última id inserido
    def lastIdEmpresa(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            ultimo = sessao.query(Empresa).order_by(
                desc(Empresa.id)).limite(1).first()

            self.id = ultimo.id + 1

            # fechando conexao
            sessao.close()

            pass

        except:

            self.id = 1

            pass

        return self.id

    # cadastro de empresa
    def inseriEmpresa(self):

        try:

            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            row = Empresa(
                id=1,
                nome_fantasia=self.nomeFantasia,
                razao_social=self.razaoSocial,
                cnpj=self.cnpj,
                insc_estadual=self.inscEstadual,
                telefone=self.telefone,
                email=self.email,
                site=self.site,
                obs=self.obs,
                cep=self.cep,
                endereco=self.endereco,
                numero=self.numero,
                bairro=self.bairro,
                cidade=self.cidade,
                estado=self.estado,
                titulo=self.titulo,
                subtitulo=self.subtitulo,
                logo=self.logo
            )

            # add query sessao
            sessao.add(row)

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError:

            self.updateEmpresa()

    # update de Empresa
    def updateEmpresa(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # selecionando id
            row = sessao.query(Empresa).get(1)

            # novos valores
            row.nome_fantasia = self.nomeFantasia
            row.razao_social = self.razaoSocial
            row.cnpj = self.cnpj
            row.insc_estadual = self.inscEstadual
            row.telefone = self.telefone
            row.email = self.email
            row.site = self.site
            row.obs = self.obs
            row.cep = self.cep
            row.endereco = self.endereco
            row.numero = self.numero
            row.bairro = self.bairro
            row.cidade = self.cidade
            row.estado = self.estado
            row.titulo = self.titulo
            row.subtitulo = self.subtitulo
            row.logo = self.logo

            # add query sessao
            sessao.add(row)

            # executando a query
            sessao.commit()

            # fechando a conexao
            sessao.close()

        except IntegrityError as err:
            print(err)

    # selecionar empresa por id
    def SelectEmpresaId(self):
        try:
            # abrindo sessao
            conecta = Conexao()
            sessao = conecta.Session()

            # query
            busca = sessao.query(Empresa).get(1)

            # salvando resultado da query
            self.id = busca.id
            self.nomeFantasia = busca.nome_fantasia
            self.razaoSocial = busca.razao_social
            self.cnpj = busca.cnpj
            self.inscEstadual = busca.insc_estadual
            self.telefone = busca.telefone
            self.email = busca.email
            self.site = busca.site
            self.obs = busca.obs
            self.cep = busca.cep
            self.endereco = busca.endereco
            self.numero = busca.numero
            self.bairro = busca.bairro
            self.cidade = busca.cidade
            self.estado = busca.estado
            self.titulo = busca.titulo
            self.subtitulo = busca.subtitulo
            self.logo = busca.logo

            # fechando a conexao
            sessao.close()

            pass
        except:
            self.titulo = None
