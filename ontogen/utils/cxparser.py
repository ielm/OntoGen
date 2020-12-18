import sys

from typing import Any, List

excluded_symbols = ['-', '$', '*', '^', '"', '?', '.', '!']

def normalize_str(string: str) -> List[str]:
    str_norm = []
    last_c = None
    for c in string:  # For each character in the input string
        if c.isalnum() or c in excluded_symbols:  # If char is alphanumeric
            if last_c.isalnum() or last_c in excluded_symbols:  # If last char is alphanumeric
                str_norm[-1] += c  # Append char to last str in str_norm list
            else:  # If char is not alphanumeric
                str_norm.append(c)  # append char to str_norm list
        elif not c.isspace():  # If char is not a space
            str_norm.append(c)  # Append char to str_norm list
        last_c = c  # Set last char to current char
    return str_norm

# Generate abstract syntax tree from normalized input.
def get_ast(input_norm: List[str]) -> List[Any]:
    ast = []
    # Go through each element in the input:
    # - if it is an open parenthesis, find matching parenthesis and make recursive
    #   call for content in-between. Add the result as an element to the current list.
    # - if it is an atom, just add it to the current list.
    i = 0
    while i < len(input_norm):
        symbol = input_norm[i]
        if symbol == '(':
            list_content = []
            match_ctr = 1 # If 0, parenthesis has been matched.
            while match_ctr != 0:
                i += 1
                if i >= len(input_norm):
                    raise ValueError("Invalid input: Unmatched open parenthesis.")
                symbol = input_norm[i]
                if symbol == '(':
                    match_ctr += 1
                elif symbol == ')':
                    match_ctr -= 1
                if match_ctr != 0:
                    list_content.append(symbol)             
            ast.append(get_ast(list_content))
        elif symbol == ')':
                raise ValueError("Invalid input: Unmatched close parenthesis.")
        else:
            try:
                ast.append(int(symbol))
            except ValueError:
                ast.append(symbol)
        i += 1
    return ast

def parse_lisp(input_str):
    input_norm = normalize_str(input_str)
    lisp_constructions = get_ast(input_norm)

    for c in lisp_constructions:
    	# parse the construction into a python-readable dictionary
    	pass

    return ast