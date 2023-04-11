import pytest
from linear_board import *
from settings import *

def test_empty_board():
    empty = LinearBoard()
    assert empty != None
    assert empty.is_full() == False
    assert empty.is_victory("x") == False
    
def test_add():
    b = LinearBoard()
    for i in range(BOARD_LENGTH):
        b.add("x")
    assert b.is_full() == True

    
def test_victory():
    b = LinearBoard()
    for i in range(VICTORY_STRIKE):
        b.add("x")
        
    assert b.is_victory("o") == False
    assert b.is_victory("x") == True
    
def test_tie():
    b = LinearBoard()
    
    b.add("o")
    b.add("o")
    b.add("x")
    b.add("o")
    
    assert b.is_tie() == True
    
def test_add_to_full():
    full = LinearBoard()
    for i in range(BOARD_LENGTH):
        full.add("x")
    full.add("x")
    assert full.is_full()
    
def test_equals():
    l = LinearBoard.fromList([1, 2, 3, 4])
    p = []
    
    assert l == l
    assert l == LinearBoard.fromList([1, 2, 3, 4])
    
    assert l != LinearBoard.fromList(p)
    assert l != LinearBoard.fromList([2, 3, 4, 5])
    assert l != LinearBoard.fromList([1, 2, 3])
    

    
""" def test_hash():
    l = LinearBoard.fromList([1, 2, 3, 4])
    p = []
    
    assert hash(l) == hash(LinearBoard.fromList(l))
    assert hash(l) == hash(LinearBoard.fromList([1, 2, 3, 4]))
    
    assert hash(l) != hash(LinearBoard.fromList(p))
    assert hash(l) != hash(LinearBoard.fromList([2, 3, 4, 5]))
    assert hash(l) != hash(LinearBoard.fromList([1, 2, 3])) """
    
        
        