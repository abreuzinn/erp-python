from Crud.CrudCatAPagar import CrudCatAPagar

class CategoriaAPagar(object):
    # populando combobox forma de pagamento
    def cboxCatAPagar(self, combobox):
        busca = CrudCatAPagar()
        busca.listaCatAPagar()
        combobox.clear()

        for i in range(len(busca.categoriaPagar)):
            combobox.addItem(busca.categoriaPagar[i], str(
                str(busca.id[i])))
