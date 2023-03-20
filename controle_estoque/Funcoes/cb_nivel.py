from Crud.CrudNivel import CrudNivel

# populando combobox nivel
def cb_nivel(campo):

    busca = CrudNivel()
    busca.listaNivel()

    i = 0

    for row in busca.nivel:
        campo.addItem(row, str(busca.id[i]))
        i += 1
