from Crud.CrudCliente import CrudCliente

class Clientes(object):
    # autocomplete cliente
    def autocompleCliente(self):
        busca = CrudCliente()
        busca.nome = self.tx_NomeFantasia.text()
        busca.autoCompleteCliente()
        lista = busca.nome
        if busca.nome:
            self.model.setStringList(lista)

    # busca cliente por nome
    def BuscaClienteNome(self, campoFoco):
        busca = CrudCliente()
        busca.nome = self.tx_NomeFantasia.text()
        busca.buscaClienteNome()
        self.tx_Id.setText(str(busca.id))
        self.BuscaClienteId(campoFoco)

    # busca cliente por id
    def BuscaClienteId(self, campoFoco):
        id = int(self.tx_Id.text())
        busca = CrudCliente()
        busca.id = id
        busca.selectClienteId()
        if busca.nome:
            self.tx_NomeFantasia.setText(busca.nome)
            self.TelefoneMask(busca.celular)
            self.tx_Telefone.setText(busca.celular)
            campoFoco.setFocus()
        else:
            self.tx_NomeFantasia.setText(
                "Cliente não encontrado")
            self.tx_Id.clear()
            self.tx_Id.setFocus()
