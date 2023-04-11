from oracle import BaseOracle, ColumnRecommendation, ColumnClassification, SmartOracle, LearningOracle
from square_board import SquareBoard
from random import choice
from list_utils import all_same
from beautifultable import BeautifulTable
from settings import BOARD_LENGTH
from move import Move
from settings import DEBUG

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
        self.moves_stack = []

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
        self._play_on(board, best.index, recommendations)
        
    def _ask_oracle(self, board):
        """
        Pregunta al oraculo y devuelve la mejor opcion
        """
        # Lista con las recomendaciones
        recommendations = self._oracle.get_recommendations(board, self)
        # Selecciono la mejor
        best = self._choose(recommendations)
        # Devuelvo la mejor reomendacion
        return (best, recommendations)
    
    def on_win(self):
        pass
    
    def on_lose(self):
        pass
    
    def _play_on(self, board, position, recommendations):
        if DEBUG:
            self.display_recommendation(board)
        # juega en position
        board.add(self.char, position)
        # Guardo la ultima jugada
        self.last_move = Move(position, board.as_code(), recommendations, self)
        # Guardo la jugada junto al resto de jugadas
        self._save_moves()
        
    def display_recommendation(self, board):
            """
            Al usar h imprimimos una tabla con recomendaciones de nuestro oracle
            """
            recommendations = self._oracle.get_recommendations(board, self)
            bt = BeautifulTable()
            classification = [recommendations[x].classification.name for x in range(0, BOARD_LENGTH)]
            bt.rows.append(classification)
            bt.columns.header = [str(i) for i in range(BOARD_LENGTH)]
            # imprimirla
            print(bt)
        
    def _save_moves(self):
        # Guarda la ultima jugada al principio de una lista de jugadas
        return self.moves_stack.insert(0, self.last_move)
        
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
             self._oracle = LearningOracle()

        def _ask_oracle(self, board):
            """
            Le pido al humano que es mi oráculo
            """
            while True:
                 # Pedimo columna al humano
                 position = input(f"Select a column, (or h for help) (0 - {len(board)-1}): ")
                 if position == "h":
                    self.display_recommendation(board)
                 # Validamos la respuesta
                 else:
                    if is_valid(board, position):
                      # Si no lo es jugamos donde ha dicho y salimos del bucle
                        pos = int(position)
                        return (ColumnRecommendation(pos, None), None)

        def on_lose(self):
            """
            Le pide al oraculo que revise sus recomendaciones
            """
            self._oracle.backtrack(self.moves_stack)
        
            

class ReportingPlayer(Player):
    def __init__(self, name, char=None, opponent=None, oracle=BaseOracle()) -> None:
         super().__init__(name, char, opponent, oracle)
    
    def on_lose(self):
        """
        Le pide al oraculo que revise sus recomendaciones
        """
        self._oracle.backtrack(self.moves_stack)
        
   
        
    
        







