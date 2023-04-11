from square_board import SquareBoard
from enum import Enum, auto
import copy
from settings import BOARD_LENGTH


class ColumnClassification(Enum):
    FULL = -1   # Imposible jugar ahi
    LOSE = 1    # Si juegas ahi pierdes
    BAD = 5    # Mala opcion
    MAYBE = 10   # Indeseable
    WIN = 100   # La mejor opcion


class ColumnRecommendation():
    def __init__(self, index, classification):
        self.index = index
        self.classification = classification

    def __eq__(self, other):
        # Si son de clases distintas, son distintos
        # if self.__class__ != other.__class__:
        if not isinstance(other, self.__class__):
            return False
        # Si son de la misma clase, comparo las propiedads
        else:
            return self.classification == other.classification

    def __hash__(self) -> int:  # Devuelve un entero
        return hash((self.index, self.classification))


class BaseOracle():
    def __init__(self) -> None:
        self.name = "Base"
    
    # Metodos sobreescritos por mis subclases
    def backtrack(self, moves):
        pass
    
    def update_to_bad(self, move):
        pass
    #
    
    def get_recommendations(self, board, player):
        """
        Returns a list of ColumnRecommendations
        """
        recommendations = []
        for i in range(len(board)):
            recommendations.append(
                self._get_column_recommendation(board, i, player))
        return recommendations
    
    def _get_column_recommendation(self, board, index, player):
        """
        Classifies a column as either FULL or MAYBE and returns an ColumnRecommendation
        """
        classification = ColumnClassification.MAYBE
        if board._columns[index].is_full():
            classification = ColumnClassification.FULL

        return ColumnRecommendation(index, classification)
    
    def no_good_options(self, board, player):
        """
        Determinamos si todas las opciones de unas recomendations son BAD o FULL
        """
        # Obtenemos las recomendaciones
        recommendations = self.get_recommendations(board, player)
        # Recorremos las recomendations
        for recommendation in recommendations:
            # Si hay alguna distinta a BAD and FULL devolvemos false
            if (recommendation.classification == ColumnClassification.WIN) or (recommendation.classification == ColumnClassification.MAYBE):
                return False
        # Si hemos terminado el bucle significa que no todas son malas y devolvemos True
        return True


class SmartOracle(BaseOracle):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Smart"

    def _get_column_recommendation(self, board, index, player):
        """
        Afina la clasificacion de super e intenta encontrar columnas WIN
        """
        recommendation = super()._get_column_recommendation(board, index, player)
        if recommendation.classification == ColumnClassification.MAYBE:
            # se puede mejorar
            if self._is_winning_move(board, index, player):
                recommendation.classification = ColumnClassification.WIN
            elif self._is_losing_move(board, index, player):
                recommendation.classification = ColumnClassification.LOSE

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
        for i in range(0, len(tmp)):
            # Si el oponente gana devolvemos True y salimos del bucle
            if self._is_winning_move(tmp, i, player.opponent):
                will_lose = True
                break
        # Devolvemos False por defecto
        return will_lose


class MemoizingOracle(SmartOracle):
    """
    El método get_recomendation está memoizado
    """

    def __init__(self) -> None:
        super().__init__()
        self._past_recommendations = {}

    def _make_key(self, board_code, player):
        """
        La clave debe de combinar el board y el player de la forma mas sencilla posible
        """
        return f"{board_code.raw_code}@{player.char}"

    def get_recommendations(self, board, player):
        """
        Creamos la key del board y el player, si la key no esta en recomendaciones pasadas
        pedimos nueva recomendacion y la guardamos, si ya estaba devolvemos la recomendacion pasada
        """
        # Creamos la clave
        key = self._make_key(board.as_code(), player)
        # Miramos en el cache: si no está, calculo y guardo en cache
        if key not in self._past_recommendations:
            print("Recomendacion nueva.")
            self._past_recommendations[key] = super().get_recommendations(board, player)
        # Devuelvo lo que está en el caché
        return self._past_recommendations[key]


class LearningOracle(MemoizingOracle):

    def update_to_bad(self, move):
        """
        Actualiza la ultima recomencacion usada que le hizo perder a BAD y la guarda
        """
        # crear clave
        key = self._make_key(move.board_code, move.player)
        # obtener la clasificacion erronea
        recommendations = self.get_recommendations(SquareBoard.fromBoardCode(move.board_code), move.player)
        # corregirla
        recommendations[move.position] = ColumnRecommendation(move.position, ColumnClassification.BAD)
        # sustituirla
        self._past_recommendations[key] = recommendations
        
    def backtrack(self, moves):
        """
        Repasa todas las jugadas y si encuentra una en la cual todo esta en BAD
        quiere decir que la anterior tiene que ser actualizada a BAD
        """
        # los moves estan en orden inverso (LIFO)
        print(f"{moves[0].player.name} is learning...")
        # por cada move
        for move in moves:
            # lo reclasifico a bad
            self.update_to_bad(move)
            # evaluo si todo estaba perdido tras esta clasificacion
            board = SquareBoard.fromBoardCode(move.board_code)
            if not self.no_good_options(board, move.player):
                # si no todo estaba perdido, salgo, Sino, sigo
                break

        print(f"Size of knowledgebase: {len(self._past_recommendations)}")
        
        
