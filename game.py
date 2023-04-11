import pyfiglet
from square_board import *
from enum import Enum, auto
from match import *
from player import *
from list_utils import *
from beautifultable import BeautifulTable
from oracle import SmartOracle, BaseOracle, MemoizingOracle, LearningOracle

class RoundType(Enum):
    COMPUTER_VS_COMPUTER = auto()
    COMPUTER_VS_HUMAN = auto()
    HUMAN_VS_HUMAN = auto()
    
class DifficultyLevel(Enum):
    EASY = auto()
    NORMAL = auto()
    HARD = auto()


class Game:
    def __init__(self, round_type=RoundType.COMPUTER_VS_COMPUTER, match=Match(Player("Chip"), Player("Chop"))) -> None:
        # Guardar variables
        self.round_type = round_type
        self.match = match
        
        # Tablero vacio sobre el que jugar
        self.board = SquareBoard()
    
    def start(self):
        # imprimo el nombre o logo del juego
        self.print_logo()
        # configuro la partida
        self._configure_by_user()
        # arrancamos el game loop
        self._start_game_loop()
    
    def _start_game_loop(self):
        # bucle infinito
        while True:
            # obtengo el jugador de turno
            current_player = self.match.next_player
            # le hago jugar
            current_player.play(self.board)
            # muestro su jugada
            self._display_move(current_player) #implementar
            # imprimo el tablero
            self._display_board() #implementar
            # si el jugeo ha terminado...
            if self._has_winner_or_tie():
                # mostrar el resultado final
                self.display_result()
                if self.match.is_match_over():
                    break
                # salgo del bucle
                else:
                    self.board = SquareBoard()
                    self._display_board()

    def _display_move(self, player):
        print(f"\n{player.name}({player.char}) has moved in column {player.moves_stack[0].position}")
    
    def _display_board(self):
        """
        Imprimir el tablero en su estado actual
        """# obtenemos una matriz de caracteres a partir del tablero
        matriz = self.board.as_matrix()
        matriz = list(map(lambda column: column[::-1], matriz))
        # crear la tabla de beautifultable
        bt = BeautifulTable()
        for col in matriz:
            bt.columns.append(col)
        bt.columns.header = [str(i) for i in range(BOARD_LENGTH)]
        # imprimirla
        print(bt)

    
    def display_result(self):
        winner = self.match.get_winner(self.board)
        if winner != None:
            print(f"\n{winner.name} ({winner.char} wins!!!)")
        else:
            print(f"\nA tie between {self.match.get_player('x').name} and {self.match.get_player('o').name}")
        
    def _has_winner_or_tie(self):
        """
        El juego se acaba cuando hay vencedor o empate
        """
        winner = self.match.get_winner(self.board)
        if winner != None:         # Alguien ha ganado
            winner.opponent.on_lose()
            return True
        elif self.board.is_full(): # Empate
            # obtengo los players y los mando a aprender
            players = self.match.current_players()
            players["x"].on_lose()
            players["o"].on_lose()
            return True
        else:                      # Sigue el juego
            return False
            
    def _configure_by_user(self):
        """
        Le pido al usuario los valores que quiere para tipo de partyda y dificultad
        """
        # determinar el tipo de partida (preguntando al usuario)
        self.round_type = self._get_round_type()
        #determinar la dificultad (preguntando al usuario)
        if self.round_type == RoundType.COMPUTER_VS_HUMAN:
            self._difficulty_level = self._get_difficulty_level()
            
        self.match = self._make_match()
    
    def _get_difficulty_level(self):
        """
        Pregunta al usuario como de listo quiere que sea su oponente
        """
        print("""
              Choose your opponent, human:
              1) Bender: for clowns and wimps.
              2) T-1000: you may regret it.
              3) Skynet: don't even think about it!
              """)
        response = ""
        
        while response != "1" and response != "2" and response != "3":
            response = input("Please type either 1 or 2 or 3: ").strip()
            if response == "1":
                level = DifficultyLevel.EASY
            elif response == "2":
                level = DifficultyLevel.NORMAL
            else:
                level = DifficultyLevel.HARD
        return level
        
        
    def _get_round_type(self):
        """
        Preguntar al usuario
        """
        print("""
              Select type of round:
              1) Computer vs Computer
              2) Computers vs Human
              3) Human vs Human
              
              """)
        response = ""
        
        while response != "1" and response != "2" and response != "3":
            response = input("Please choose type 1 or 2 or 3: ").strip()
            
        if response == "1":
            return RoundType.COMPUTER_VS_COMPUTER
        elif response == "2":
            return RoundType.COMPUTER_VS_HUMAN
        else:
            return RoundType.HUMAN_VS_HUMAN
        
    def _make_match(self):
        
        _levels = {DifficultyLevel.EASY: BaseOracle(),
                   DifficultyLevel.NORMAL: SmartOracle(),
                   DifficultyLevel.HARD: LearningOracle()}
        
        _names = {DifficultyLevel.EASY: "Bender",
                  DifficultyLevel.NORMAL: "T-1000",
                  DifficultyLevel.HARD: "Skynet"}
        
        if self.round_type == RoundType.COMPUTER_VS_COMPUTER:
            player1 = ReportingPlayer("Skynet", oracle=SmartOracle())
            player2 = ReportingPlayer("ChatGPT", oracle=LearningOracle())
        elif self.round_type == RoundType.COMPUTER_VS_HUMAN:
            player1 = ReportingPlayer(name=_names[self._difficulty_level], oracle=_levels[self._difficulty_level])
            player2 = HumanPlayer(name=input("Enter your name: "))
        else:
            player1 = HumanPlayer(name=input("1) Enter your name: "))
            player2 = HumanPlayer(name=input("2) Enter your name: "))
            
        return Match(player1, player2)
            
    def print_logo(self):
        logo = pyfiglet.Figlet(font="stop")
        print(logo.renderText("Connecta4"))
        