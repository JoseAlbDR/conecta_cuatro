from linear_board import *
from list_utils import *
from string_utils import *

class SquareBoard():
    """
    Representa un tablero cuadrado
    """
    
    @classmethod
    def fromBoardCode(cls, board_code):
        #return cls.fromList(board_code.as_matrix())
        return cls.fromBoardRawCode(board_code.raw_code)
    
    @classmethod
    def fromBoardRawCode(cls, board_raw_code):
        """
        Transforma una cadena en formato de BoardCode en una
        lista de LinearBoards y luego lo transforma en un tablero
        """
        # 1. Convertir la cadena del codigo en una lista de cadenas
        string_list = board_raw_code.split("|")
        # 2. Transformar cada cadena en una lista de caracteres
        char_list = explode_string_list(string_list)
        # 3. Cambiamos todas las ocurrencias de . por None
        matrix = replace_all_in_matrix(char_list, ".", None)
        # 4. Transformamos esa lista en un SquareBoard
        return cls.fromList(matrix)
    
    @classmethod
    def fromList(cls, list_of_lists):
        """
        Transforma una lista de listas en una list de linearboard
        """
        # Creamos un board 
        board = cls()
        # Creamos una matriz de listas de todos los linear board de ._columns
        board._columns = list(map(lambda element: LinearBoard.fromList(element), list_of_lists))
            
        return board
           
    def __init__(self):
        self._columns = [LinearBoard() for i in range(BOARD_LENGTH)]
          
    def __repr__(self):
        return f"{self.__class__}: {self._columns}"
    
    def __len__(self):
        return len(self._columns)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._columns == other._columns

    def __hash__(self):
        return hash(self._columns)

    def is_full(self):
        """
        True si todos los LinearBoard son full
        """
        result = True
        # Por cada linear board en columns
        for lb in self._columns:
            # Comprobamos que todos esten llenos, si hay alguno vacio result sera False
            result = result and lb.is_full()
        # Devolvemos result
        return result
    
    def as_code(self):
        return BoardCode(self)
    
    def as_matrix(self):
        """
        Devuelve una representacion en formato de matriz, es decir, lista de listas
        """
        return list(map(lambda element: element._column, self._columns))

    def add(self, char, column):
        """
        Añade char a la column elegida
        """
        self._columns[column].add(char)    


    # Detectar victoriass
    def is_victory(self, char):
        """
        Detecta si hay una victoria en vertical, horizontal o vertical ascendente o descendente
        """
        return self._any_vertical_victory(char) or self._any_horizontal_victory(char) or self._any_rising_victory(char) or self._any_sinking_victory(char)

    def _any_vertical_victory(self, char):
        """
        True si hay alguna victoria en vertical
        """
        result = False
        # Por cada linear board dentro de columns
        for lb in self._columns:
            # Si hay una victoria en algun linear board reslut sera = True
            result = result or lb.is_victory(char)
        # Devolvemos result
        return result
    
    def _any_horizontal_victory(self, char):
        """
        Devuelve true si hay una victoria en horizontal de char
        """
        # Transponemos las columnas en una matriz
        transpose_matriz = transpose(self.as_matrix())
        # Creamos un tablero temporal
        temp = SquareBoard.fromList(transpose_matriz)
        # Comprobamos si hay victorias verticales
        return temp._any_vertical_victory(char)
        
    def _any_rising_victory(self, char):
        # Obtenemos las columnas como una matriz
        matrix = self.as_matrix()
        # Invertimos la matriz
        inverse_matrix = list(map(lambda column: column[::-1], matrix))
        # Creamos una matriz temporal
        tmp = SquareBoard.fromList(inverse_matrix)
        # Comprobamos las victorias descendentes
        return tmp._any_sinking_victory(char)
    
    def _any_sinking_victory(self, char):
        # Obtenemos las columnas como una matriz
        matrix = self.as_matrix()
        # Las desplazamos
        displaced_matrix = displace_matrix(matrix)
        # Creamos un tablero temporal con esa matriz
        temp = SquareBoard.fromList(displaced_matrix)
        # Averiguamos si tiene una victoria horizontal
        return temp._any_horizontal_victory(char)
            
    # dunders
    def __repr__(self) -> str:
        return f"{self.__class__}:{self._columns}"
   
class BoardCode:
    def __init__(self, board):
        self._raw_code = collapse_matrix(board.as_matrix())
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        else:
            return self.raw_code == other.raw_code
    
    def __hash__(self) -> int:
        return hash(self.raw_code)
    
    def __repr__(self) -> str:
        return f"{self.__class__}: {self.raw_code}"
        
    @property
    def raw_code(self):
        return self._raw_code
    
    @DeprecationWarning
    def as_matrix(self):
        matrix = []
        column = []
        for char in self.raw_code:
            if char == "|":
                matrix.append(column)
                column = []
            else:
                if char == ".":
                    column.append(None)
                else:
                    column += char
        matrix.append(column)
        return matrix
                

