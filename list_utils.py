from settings import *

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

def first_elements(matriz):
    """
    Devuelve en una lista los primeros elementos de una matriz (la primera columna)
    """
    return any_element(matriz, 0)

def any_element(matriz, n):
    """
    Devuelve en una lista los elementos de la columna n
    """
    # Coge el elemento n de cada fila de la matriz y lo mete en una lista
    result = []
    for list in matriz:
        result.append(list[n])
    return result

def transpose(matriz):
    """
    Devuelve una matriz transpuesta
    """
    # Matriz vacia
    transpose_matriz = []
    # Para cada fila que tenga matriz 
    for n in range(len(matriz[0])):
        # Añade a la fila de matriz transpuesta los primeros elementos de la columna n de matriz
        transpose_matriz.append(any_element(matriz, n))
    return transpose_matriz

def positive_displace(l, distance, filler):
    """
    Devuelve la lista l con sus elementos desplazados distance posiciones y rellenando los huecos con filler
    """
    n = 0
    # Mientras que n sea menor a la distancia
    while n < distance:
        # Sacamos el ultimo item e intruducimos el filtro en el primero
        l.pop()
        l.insert(0, filler)
        # Incrementamos el contador
        n += 1
    # Devolvemos la lista transformada
    return l
    
    
def displace(l, distance, filler=None):
    """
    Devuelve una lista con los elementos desplazados por distancia y reelenando con filler
    """
    # Si la distancia es 0 o la lista esta vacia devuelve la lista
    if distance == 0:
        return l
    elif distance > 0:
        filling = [filler] * distance
        res = filling + l
        res = res[:-distance]
        return res
    else:
        filling = [filler] * abs(distance)
        res = l + filling
        res = res[abs(distance):]
        return res
        
def displace_matrix(m, filler=None):
    # creamos una matriz vacia
    matrix = []
    # por cada columna de la matriz original la desplazamos su indice -1
    # añadimos la columna desplazada a m
    for i in range(len(m)):
        matrix.append(displace(m[i], i-1, filler))
    # devolvemos m
    return matrix

def reverse_list(l):
    """
    Devuelve la lista invertida
    """
    return list(reversed(l))
     
def reverse_matrix(matrix):
    """
    Devuelve una matriz invertida
    """
    rm = []
    for col in matrix:
        rm.append(reverse_list(col))
    return rm

def all_same(l):
    """
    Devuelve True si todos los elementos de la lista son iguales
    o la lista esta vacia
    """
    if l == []:
        return True
    else:
        for i in l:
            for j in l:
                if i != j:
                    return False
            return True

def collapse_list(l, empty = "."):
    # Variable que contiene la lista colapsada
    colapsed_list = ""
    # Si la lista es vacia devolvemos la lista colapsada vacia
    if l == []:
        return colapsed_list
    # Si no esta vacia
    else:
        # Por cada elemento de la lista
        for elem in l:
            # Si el elemento es None lo sustituimos por "."
            if elem == None:
                colapsed_list += empty
            # Si no lo es añadimos el elemento
            else:
                colapsed_list += elem
    return colapsed_list


def collapse_matrix(matrix, fence = "|"):
    # Creamos la variable que va a contener la matriz colapsada
    collapsed_matrix = ""
    # Recorremos las columnas de la matriz
    #return [fence + collapse_list(matrix[column]) if column != 0 and column != len(matrix) else collapse_list(matrix[column]) for column in range(0, len(matrix))]
    for column in range(0, len(matrix)):
    # Por cada columna la colapsamos y la añadimos a la matriz colapsada
        if column != 0 and column != len(matrix):
            collapsed_matrix += fence + collapse_list(matrix[column])
        else:
            collapsed_matrix += collapse_list(matrix[column])
    # Devolvemos la matriz colapsada
    return collapsed_matrix


def replace_all_in_list(l, old, new):
    """
    Cambia todas las ocurrencias de old por new
    """
    return [new if element == old else element for element in l]

def replace_all_in_matrix(matrix, old, new):
    """
    Aplica replace_all_in_list a todas las listas
    """
    return [replace_all_in_list(column, old, new) for column in matrix]





