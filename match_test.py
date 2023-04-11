from match import *
import pytest
from player import *

yusep = None
otto = None

def setup():
    global yusep
    yusep = HumanPlayer("YuSeP")
    global otto
    otto = Player("Otto")

def teardown():
    global yusep
    yusep = None
    global otto
    otto = None

def test_different_players_have_different_chars():
    setup()
    t = Match(yusep, otto)
    assert yusep.char != otto.char
    teardown()
    
def test_no_player_with_none_char():
    setup()
    t = Match(yusep, otto)
    assert yusep.char != None
    assert otto.char != None
    teardown()
    
def test_next_player_is_round_robbin():
    setup()
    t = Match(otto, yusep)
    p1 = t.next_player
    p2 = t.next_player
    assert p1 != p2
    teardown()
    
def test_players_are_opponents():
    setup()
    t = Match(otto, yusep)
    p1 = t.get_player("x")
    p2 = t.get_player("o")
    assert p1.opponent == p2
    assert p2.opponent == p1
    teardown()