from Crud.CrudFormaPagamento import CrudFormaPagamento

class FormaPagamento(object):
    # populando combobox forma de pagamento
    def CboxFPagamento(self, combobox):
        busca = CrudFormaPagamento()
        busca.listaFormaPagamento()
        combobox.clear()
        i = 0
        for lista in busca.formaPagamento:
            combobox.addItem(lista, str(
                str(busca.id[i])))
            i += 1
