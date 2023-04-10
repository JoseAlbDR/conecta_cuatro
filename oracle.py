from square_board import SquareBoard
from enum import Enum, auto
import copy
from settings import BOARD_LENGTH

class ColumnClassification(Enum):
    FULL = -1   # Imposible jugar ahi
    LOSE = 1    # La peor opcion
    MAYBE = 10   # Indeseable
    WIN = 100   # La mejor opcion
    
    
class ColumnRecommendation():
    def __init__(self, index, classification):
        self.index = index
        self.classification = classification
        
    def __eq__(self, other):
        # Si son de clases distintas, son distintos
        #if self.__class__ != other.__class__:
        if not isinstance(other, self.__class__):
            return False 
        # Si son de la misma clase, comparo las propiedads
        else:
            return self.classification == other.classification
        
    def __hash__(self) -> int: # Devuelve un entero
        return hash((self.index, self.classification))
    
            
class BaseOracle():
    def __init__(self) -> None:
        self.name = "Base"
    def get_recommendation(self, board, player):
        """
        Return a list of ColumnRecommendations
        """
        recommendations = []
        for column in range(0, len(board)):
            # Si la columna no esta llena
            if not board._columns[column].is_full():
                # Obtenemos recomendacion para el board, la columna y el player
                recommendations.append(self._get_column_recommendation(board, column, player))
            else:
                # Si esta llena, la recomendacion es FULL
                recommendations.append(ColumnRecommendation(column, ColumnClassification.FULL))
        return recommendations
    
    def _get_column_recommendation(self, board, index, player):
        """
        Classifies a column as eiter FULL or MAYBE and returns an ColumnRecommendation
        """
        # Como solo hay dos recomendaciones FULL y MAYBE y FULL ya esta filtrada se le asigna MAYBE
        classification = ColumnClassification.MAYBE
        return ColumnRecommendation(index, classification)
    
class SmartOracle(BaseOracle):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Smart"
    def _get_column_recommendation(self, board, index, player):
        """
        Afina la clasificacion de super e intenta encontrar columnas win
        """
        # Como solo hay dos recomendaciones FULL y MAYBE y FULL ya esta filtrada se le asigna MAYBE
        recommendation = ColumnRecommendation(index, ColumnClassification.MAYBE)
        # Si es un movimiento ganador la recomendacion es WIN
        if self._is_winning_move(board, index, player):
            recommendation = ColumnRecommendation(index, ColumnClassification.WIN)
        # Si es un momiviento que implica la derrota la recomendacion es LOSE
        elif self._is_losing_move(board, index, player):
            recommendation = ColumnRecommendation(index, ColumnClassification.LOSE)
        # Se devuelve la recomendacion, por defecto (si no es WIN o LOSE) es MAYBE
        return recommendation
        
    def _is_winning_move(self, board, index, player):
        """
        Determina si al jugar en una posicion nos llevaria a ganar de inmediato
        """
        # Hacemos una copia del tablero
        temp = copy.deepcopy(board)
        # Jugamos en la posicion sugerida
        temp.add(player.char, index)
        # Comprobamos si la jugada es ganadora
        return temp.is_victory(player.char)
            # Devolvemos la recomendacion
            
    def _is_losing_move(self, board, index, player):
        """
        Si player juega en index genera una jugada vencedora para el oponente
        en alguna de las demas columnas
        """
        # Hacemos copia del tablero
        tmp = copy.deepcopy(board)
        # Añadimos la ficha de player
        tmp.add(player.char, index)
        will_lose = False
        # Para cada columna del board
        for i in range(0, BOARD_LENGTH):
            # Si el oponente gana devolvemos True y salimos del bucle
            if self._is_winning_move(tmp, i, player.opponent):
                will_lose = True
                break;
        # Devolvemos False por defecto
        return will_lose
            
    
        
            