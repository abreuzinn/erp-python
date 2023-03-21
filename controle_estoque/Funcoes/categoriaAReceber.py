from Crud.CrudCatAReceber import CrudCatAReceber

class CategoriaAReceber(object):
    # pppulando combobox forma de pagamento
    def cboxCatAReceber(self, combobox):
        busca = CrudCatAReceber()
        busca.listaCatAReceber()
        combobox.clear()

        for i in range(len(busca.categoriaReceber)):
            combobox.addItem(busca.categoriaReceber[i], str(
                str(busca.id[i])))
