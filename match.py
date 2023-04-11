from player import *
from square_board import *

class Match:
    def __init__(self, player1, player2):
        player1.char = "x"
        player2.char = "o"
        player1.opponent = player2
        
        self._players = {
            "x": player1,
            "o": player2
        }
        
        self._round_robbin = [player1, player2]
      
    @property  
    def next_player(self):
        current_player = self._round_robbin[0]
        self._round_robbin.reverse()
        return current_player
    
    def get_player(self, char):
        return self._players[char]
    
    def get_winner(self, board):
        if board.is_victory("x"):
            return self.get_player("x")
        elif board.is_victory("o"):
            return self.get_player("o")
        else:
            return None
        
    def current_players(self):
        players = {}
        players["x"] = self.get_player("x")
        players["o"] = self.get_player("o")
        return players    
    
    def is_match_over(self):
        """
        Pregunta al usuario si hay huevos a echar otra partida
        """
        answer = ""
        while answer != "y" or answer != "n":
            answer = input("Would you like to play another match? (Y/N): ").lower()
            if answer == "y":
                return False
            elif answer == "n":
                return True
        
    def is_match_over_(self):
        return False