from oracle import BaseOracle, ColumnRecommendation, ColumnClassification, SmartOracle
from square_board import SquareBoard
from random import choice
from list_utils import all_same
from beautifultable import BeautifulTable
from settings import BOARD_LENGTH

# Funciones de validacion
def _is_int(strnumber):
    try:
        int(strnumber)
        return True
    except ValueError:
            return False

def _is_within_column_range(board, column):
        return column < len(board) and column >= 0

def _is_non_full_column(board, column):
        return not board._columns[column].is_full()

def is_valid(board, column):
        return _is_int(column) and _is_within_column_range(board, int(column))\
        and _is_non_full_column(board, int(column))
        

class Player():
    def __init__(self, name, char=None, opponent=None, oracle = BaseOracle()) -> None:
        self.name = name
        self.char = char
        self.opponent = opponent
        self._oracle = oracle
        self.last_move = None

    @property
    def opponent(self):
        return self._opponent

    @opponent.setter
    def opponent(self, other):
        if other != None:
            self._opponent = other
            other._opponent = self
    
    def play(self, board):
        """
        Elige la mejor columna de aquellas que recomienda el Oraculo
        """
        # Pregunto al oraculo por el indice
        (best, recommendations) = self._ask_oracle(board)
        # Juego en el indice que me indica el oraculo
        self._play_on(board, best.index)

    
    def _ask_oracle(self, board):
        """
        Pregunta al oraculo y devuelve la mejor opcion
        """
        # Lista con las recomendaciones
        recommendations = self._oracle.get_recommendation(board, self)
        # Selecciono la mejor
        best = self._choose(recommendations)
        # Devuelvo la mejor reomendacion
        return (best, recommendations)
        
        
    def _play_on(self, board, position):
        # juega en position
        board.add(self.char, position)
        # guardo mi ultima jugada
        self.last_move = position

    def _choose(self, recommendations):
        # sacamos las no validas
        valid = list(filter(lambda x: x.classification != ColumnClassification.FULL, recommendations))
        # ordenamos por el valor de clasificacion
        valid = sorted(valid, key=lambda x : x.classification.value, reverse=True )
        #for n in valid:
            #print(self.char, n.index, n.classification)
        # si son todas iguales, pillo una al azar
        if all_same(valid):
            # seleccinamos entre las iguales, una al azar
            return choice(valid)
        # si no lo son, pillo la mas deseable (que sera la primera)
        else:
             return valid[0]
      

class HumanPlayer(Player):
        def __init__(self, name, char=None) -> None:
             super().__init__(name, char)

        def _ask_oracle(self, board):
            """
            Le pido al humano que es mi oráculo
            """
            while True:
                 # Pedimo columna al humano
                 position = input(f"Select a column, (or h for help) (0 - {len(board)}): ")
                 if position == "h":
                    oracle = SmartOracle()
                    recommendations = []
                    recommendations = oracle.get_recommendation(board, self)
                    self._print_recommendation(recommendations)
                 # Validamos la respuesta
                 else:
                    if is_valid(board, position):
                      # Si no lo es jugamos donde ha dicho y salimos del bucle
                        pos = int(position)
                        return (ColumnRecommendation(pos, None), None)
                 

                 
        def _print_recommendation(self, recommendations):
            bt = BeautifulTable()
            classification = [recommendations[x].classification.name for x in range(0, BOARD_LENGTH)]
            bt.rows.append(classification)
            bt.columns.header = [str(i) for i in range(BOARD_LENGTH)]
            # imprimirla
            print(bt)
            






