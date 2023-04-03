def find_one(list, needle):
    """
    Devuelve True si encuentra una o más ocurrencias de needle en list
    """
    return find_n(list, needle, 1)


def find_n(list, needle, times): 
    """
    Devuelve True si en list hay times o mas ocurrencias de needle
    False si hay menos o si n < 0
    """
    # Si times < 0 devolvemos False
    if times < 0:
        return False
    
    # Inicializamos el indice y el contador
    acum = 0
    index = 0
    
    # Mientras no hayamos encontrado al elemento n veces o no hayamos terminado la lista
    while acum < times and index < len(list):
        # SI lo encontramos, actualizamos el contador
        if list[index] == needle:
            acum += 1
        # Avanzamos al siguiente elemento
        index += 1
    # Devolvemos el resultado igualado a times
    return acum == times

def find_streak(list, needle, times): 
    """
    Devuelve True si en list hay times o mas ocurrencias de needle seguidas
    False si hay menos o si n < 0
    """
    # Si times < 0 devolvemos False
    if times < 0:
        return False
    # Inicializamos el indice y el contador
    acum = 0
    index = 0
    # Mientras no hayamos encontrado al elemento n veces seguidas o no hayamos terminado la lista
    while acum < times and index < len(list):
        # SI lo encontramos, aumentamos en uno el acumulador de coincidencias
        if list[index] == needle:
            acum += 1
        # Si no encontramos el elemento ponemos el acumulador de coincidencias a 0, y rompemos la racha siempre que acum sea < que times
        else:
            acum = 0
        # Avanzamos al siguiente elemento
        index += 1
    # Devolvemos el resultado igualado a times
    return acum == times

#    assert find_n([1, 2, 3, 4, 5], 42, 2) == False

print(find_streak([1, 2, 3, 1, 2], 2, 2))