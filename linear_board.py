from settings import *
from list_utils import *

class LinearBoard():
    """
    Clase que representa un tablero de una sola columna
    x un jugador
    o otro jugador
    None un espacio vacio
    """
    
    @classmethod
    def fromList(cls, list):
        """
        Transforma un linear board en una lista para poder trabajar con len()
        """
        linear_board = cls()
        linear_board._column = list
        return linear_board
        
    def __init__(self):
        """
        Una lista de None
        """
        self._column = [None for i in range(BOARD_LENGTH)]
        
    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        else:
            if self._column == other._column:
                return True
    
        
    def add(self, token):
        """
        Juega en la primera posicion disponible
        """
        # Intenta añadir una ficha
        try:
            i = self._column.index(None)
            self._column[i] = token
        # Si ya esta lleno lo devuelve
        except ValueError:
            self.add_to_full()
            
    def add_to_full(self):
        return self.is_full()
        
    def empty_board(self):
        """
        Si el tablero esta vacio
        """
        if "x" in self._column or "o" in self._column:
            return False
        return True
        
    def is_full(self):
        """
        Si el tablero esta lleno
        """
        # Si el elemento del final es distinto de None el tablero esta lleno
        return self._column[-1] != None
       
    def is_victory(self, token):
        """
        Si un jugador ha ganado
        """
        # Buscamos si hay una racha de token repetido VICTORY_STRIKE veces
        return find_streak(self._column, token, VICTORY_STRIKE)

    def is_tie(self):
        """
        Si hay un empate
        """
        # Si el tablero esta lleno y no ha ganado ninguno
        if (not self.is_victory("x")) and (not self.is_victory("o")):
                return True
            
    #