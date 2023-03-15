import re
from PyQt5.QtCore import QByteArray, QBuffer, Qt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
from Views.mainEmpresa import Ui_ct_empresa
from Crud.CrudEmpresa import CrudEmpresa

class MainEmpresa(Ui_ct_empresa):

    def mainempresa(self, frame):
        super(MainEmpresa, self).setMainEmpresa(frame)
        self.fr_empresa.show()

        # Definindo icones padrão
        self.IconeBotaoMenu(self.bt_AddLogo,
                            self.resourcepath('Images/edit-add.png'))
        self.IconeBotaoMenu(self.bt_DelLogo,
                            self.resourcepath('Images/edit-delete.png'))
        self.IconeBotaoMenu(self.bt_LocalizaCepEmpresa,
                            self.resourcepath('Images/search.png'))
        self.IconeBotaoForm(self.bt_SalvarDadosEmpresa,
                            self.resourcepath('Images/salvar.png'))

        # Ocultando widgets
        # Hidden id input
        self.tx_idEmpresa.setHidden(True)
        # Hidden bt Del Logo
        self.bt_DelLogo.setHidden(True)

        # Botao Add Logo
        self.bt_AddLogo.clicked.connect(self.UploadLogo)
        # Botao Del Logo
        self.bt_DelLogo.clicked.connect(self.DelLogo)
        # Botao salvar Empresa
        self.bt_SalvarDadosEmpresa.clicked.connect(self.CadEmpresa)

        # Set ID Empresa
        self.LastIdEmpresa()

    # logo upload
    def UploadLogo(self):
        Dialog = QFileDialog()
        Dialog.setOption(QFileDialog.DontUseNativeDialog, True)

        fname = Dialog.getOpenFileName(
            self, "Selecionar Logo", "", "Image files (*.jpg *.png)")[0]

        self.lb_LogoEmpresa.setPixmap(QPixmap(fname).scaledToWidth(
            300, Qt.TransformationMode(Qt.FastTransformation)))
        # self.lb_LogoEmpresa.setScaledContents(True)
        self.bt_AddLogo.setHidden(True)
        self.bt_DelLogo.setVisible(True)

    def DelLogo(self):
        self.lb_LogoEmpresa.clear()
        self.bt_DelLogo.setHidden(True)
        self.bt_AddLogo.setVisible(True)

    # auto selectempresa
    def LastIdEmpresa(self):
        try:
            busca = CrudEmpresa()
            self.tx_idEmpresa.setText(str(busca.lastIdEmpresa()))
            self.SelectEmpresa()
        except:
            self.tx_idEmpresa.setText(str(1))

    # selecionar empresa na db
    def SelectEmpresa(self):
        busca = CrudEmpresa()
        busca.idEmpresa = self.tx_idEmpresa.text()
        busca.SelectEmpresaId()
        self.tx_idEmpresa.setText(str(busca.id))
        self.tx_NomeFantasia.setText(busca.nomeFantasia)
        self.tx_RazaoSocial.setText(busca.razaoSocial)
        self.tx_Cnpj.setText(str(busca.cnpj))
        self.tx_IE.setText(str(busca.inscEstadual))
        self.tx_TelefoneEmpresa.setText(
            self.formatoNumTelefone((busca.telefone)))
        self.tx_SiteEmpresa.setText(busca.site)
        self.tx_EmailEmpresa.setText(busca.email)
        self.tx_ObsEmpresa.setText(busca.obs)
        self.tx_CepEmpresa.setText(busca.cep)
        self.tx_Endereco.setText(busca.endereco)
        self.tx_NumEmpresa.setText(str(busca.numero))
        self.tx_BairroEmpresa.setText(busca.bairro)
        self.tx_CidadeEmpresa.setText(busca.cidade)
        self.tx_EstadoEmpresa.setText(busca.estado)
        self.tx_Titulo.setText(busca.titulo)
        self.tx_SubTitulo.setText(busca.subtitulo)
        if busca.logo:
            self.bt_AddLogo.setHidden(True)
            self.bt_DelLogo.setVisible(True)
            # print busca.logo
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray.fromBase64(
                busca.logo))
            self.lb_LogoEmpresa.setPixmap(pixmap.scaledToWidth(
                300, Qt.TransformationMode(Qt.FastTransformation)))

        pass

    # cadastrar empresa
    def CadEmpresa(self):
        inserir = CrudEmpresa()
        inserir.id = self.tx_idEmpresa.text()
        inserir.nomeFantasia = self.tx_NomeFantasia.text().upper()
        inserir.razaoSocial = self.tx_RazaoSocial.text().upper()
        inserir.cnpj = self.tx_Cnpj.text()
        inserir.inscEstadual = self.tx_IE.text()
        inserir.telefone = re.sub(
            '[^[0-9]', '', (self.tx_TelefoneEmpresa.text()))
        inserir.email = self.tx_EmailEmpresa.text()
        inserir.site = self.tx_SiteEmpresa.text()
        inserir.obs = self.tx_ObsEmpresa.text().upper()
        inserir.cep = re.sub('[^[0-9]', '', (self.tx_CepEmpresa.text()))
        inserir.endereco = self.tx_Endereco.text().upper()
        inserir.numero = self.tx_NumEmpresa.text()
        inserir.bairro = self.tx_BairroEmpresa.text().upper()
        inserir.cidade = self.tx_CidadeEmpresa.text().upper()
        inserir.estado = self.tx_EstadoEmpresa.text().upper()
        inserir.titulo = self.tx_Titulo.text()
        inserir.subtitulo = self.tx_SubTitulo.text()

        if self.lb_LogoEmpresa.pixmap():
            image = QPixmap(self.lb_LogoEmpresa.pixmap())
            data = QByteArray()
            buf = QBuffer(data)
            image.save(buf, 'PNG')
            logo = str(data.toBase64()).encode('utf8')[2:-1]
            inserir.logo = logo
        else:
            inserir.logo = False

        inserir.inseriEmpresa()
        self.lb_NomeFantasia.setText(self.tx_Titulo.text())
        self.lb_NomeFantasia2.setText(inserir.subtitulo)
        self.setWindowTitle(inserir.titulo + " " + inserir.subtitulo)
