import pytest
from list_utils import *
from oracle import ColumnRecommendation, ColumnClassification

def test_find_one():
    needle = 1
    none = [0, 0, 0, "s"]
    beginning = [1, None, 9, 6, 0, 0]
    end = ["x", "0", 1]
    several = [0, 0, 3, 4, 1, 3, 2, 1, 3, 4]
    
    assert find_one(none, needle) == False
    assert find_one(beginning, needle)
    assert find_one(end, needle)
    assert find_one(several, needle)
    

def test_find_n():
    assert find_n([2, 3, 4, 5, 6], 2, -1) == False
    assert find_n([1, 2, 3, 4, 5], 42, 2) == False
    assert find_n([1, 2, 3, 4, 5], 1, 2) == False
    assert find_n([1, 2, 3, 2, 4, 5], 2, 2)
    assert find_n([1, 2, 3, 4, 5, 4, 6, 4, 7, 4, 6], 4, 2)
    assert find_n([1, 2, 3, 4], "x", 0)
    
    
def test_find_streaks():
    assert find_streak([1, 2, 3, 4, 5], 4, -1) == False
    assert find_streak([1, 2, 3, 4, 5], 42, 2) == False
    assert find_streak([1, 2, 3, 4], 4, 1)
    assert find_streak([1, 2, 3, 1, 2], 2, 2) == False
    assert find_streak([1, 2, 3, 4, 5, 5, 5], 5, 3)
    assert find_streak([5, 5, 5, 1, 2, 3, 4], 5, 3)
    assert find_streak([1, 2, 5, 5, 5, 5, 4], 5, 3)
    assert find_streak([1, 2, 3, 4, 5, 5, 5], 5, 4) == False
    

def test_first_elements():
    original = [[0, 7 , 3], 
                [4,0,1]]
    
    vertical_start = [["x", None, None, None, None],
                    ["x", None, None, None, None],
                    ["x", "o", None, None, None],
                    ["x", "o", None, None, None],
                    ["x", "o", None, None, None]]
    
    assert first_elements(original) == [0, 4]
    assert first_elements(vertical_start) == ["x", "x", "x", "x", "x"]
    

def test_any_element():
    vertical_mid = [["x", "o", "x", None, None, ],
                    ["o", "x", "x", None, None, ],
                    ["x", "o", "x", "o", None, ],
                    ["x", "o", "x", "x", None, ],
                    ["o", "x", "o", None, None, ],]
    
    assert any_element(vertical_mid, 0) == ["x", "o", "x", "x", "o"]
    assert any_element(vertical_mid, 1) == ["o", "x", "o", "o", "x"]
    assert any_element(vertical_mid, 2) == ["x", "x", "x", "x", "o"]
    assert any_element(vertical_mid, 3) == [None, None, "o", "x", None]
    assert any_element(vertical_mid, 4) == [None, None, None, None, None]
    
def test_transpose():
    original = [["x", "o", "x", None, None, ],
                ["o", "x", "x", None, None, ],
                ["x", "o", "x", "o", None, ],
                ["x", "o", "x", "x", None, ],
                ["o", "x", "o", None, None, ],]
    
    another = [[0, 7 , 3], 
                [4,0,1]]
    
    assert transpose(original) == [["x", "o", "x", "x", "o", ],
                                    ["o", "x", "o", "o", "x", ],
                                    ["x", "x", "x", "x", "o", ],
                                    [None, None, "o", "x", None, ],
                                    [None, None, None, None, None, ],]
    
    assert transpose(another) == [[0, 4],
                                  [7, 0],
                                  [3, 1]]
    assert transpose(transpose(original)) == original
    assert transpose(transpose(another)) == another
        
def test_zero_distance_displace():
    l1 = [1, 2, 3, 4, 5, 6]
    l2 = [1]
    l3 = [[4, 5]], ["x", "o", "c"]
    
    assert displace([], 0) == []
    assert displace(l1, 0) == l1
    assert displace(l2, 0) == l2
    assert displace(l3, 0) == l3
    
def test_positive_distance_displace():
    l1 = [1, 2, 3, 4, 5, 6]
    l2 = [1]
    l3 = [[4, 5], ["x", "o", "c"]]
    l4 = [9, 6, 5]
    
    assert displace([], 2) == []
    assert displace(l1, 2) == [None, None, 1, 2, 3, 4]
    assert displace(l2, 3, "-") == ["-"]
    assert displace(l3, 1, "#") == ["#", [4, 5]]
    assert displace(l4, 3, 0) == [0, 0, 0]  
    
    
def test_negative_distance_displace():
    l1 = [1, 2, 3, 4, 5, 6]
    l2 = [1]
    l3 = [[4, 5], ["x", "o", "c"]]
    l4 = [9, 6, 5]
    
    assert displace([], -2) == []
    assert displace(l1, -2) == [3, 4, 5, 6, None, None]
    assert displace(l2, -3, "-") == ["-"]
    assert displace(l3, -1, "#") == [["x", "o", "c"], "#"]
    assert displace(l4, -3, 0) == [0, 0, 0]    
    
def test_reverse_list():
    assert reverse_list([]) == []
    assert reverse_list([1, 2, 3, 4, 5, 6]) == [6, 5, 4, 3, 2, 1]
    
def test_reverse_matrix():
    assert reverse_matrix([]) == []
    assert reverse_matrix([[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]]) == [[6, 5, 4, 3, 2, 1], [6, 5, 4, 3, 2, 1]]
    
    
def test_all_same():
    l = [1,1,1,1,1,1,1,1]
    k = [1,2,3,4,5,6]
    assert all_same(l) == True
    assert all_same(k) == False    
    assert all_same([[], [], []])
    assert all_same([])
    
    assert all_same([ColumnRecommendation(0, ColumnClassification.WIN),
                     ColumnRecommendation(2, ColumnClassification.WIN)])
    
    assert all_same([ColumnRecommendation(0, ColumnClassification.WIN),
                     ColumnRecommendation(0, ColumnClassification.MAYBE)]) == False

    
    