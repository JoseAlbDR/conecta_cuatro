def explode_string(string):
    return list(string)

def explode_string_list(string_list):
    return [explode_string(string) for string in string_list]
    