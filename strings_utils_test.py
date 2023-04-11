from string_utils import explode_string, explode_string_list
def test_explode_string():
    assert explode_string("Han") == ["H", "a", "n"]
    assert explode_string("") == []
    
def test_explode_string_list():
    assert explode_string_list(["Han", "Solo"]) == [["H", "a", "n"], ["S", "o", "l", "o"]]
    assert explode_string_list(["", "", ""]) == [[], [], []]
    assert explode_string_list([]) == []