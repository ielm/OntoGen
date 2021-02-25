import sys

from typing import Any, List, OrderedDict
from pprint import pprint

EXCLUDED_SYMBOLS = ["-", "$", "*", "^", '"', "?", ".", "!"]
LITERAL_KEYS = ["DEF", "CAT", "TMR-HEAD", "EX", "COMMENTS", "EXAMPLE-BINDINGS"]


def normalize_str(string: str) -> List[str]:
    str_norm = []
    last_c = None
    for c in string:  # For each character in the input string
        if c.isalnum() or c in EXCLUDED_SYMBOLS:  # If char is alphanumeric
            if (
                last_c.isalnum() or last_c in EXCLUDED_SYMBOLS
            ):  # If last char is alphanumeric
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
    i = 0

    # For each element in the input structure
    while i < len(input_norm):
        symbol = input_norm[i]
        # If the element is an open parenthesis, find matching parenthesis and make
        # recursive call for content in between. Add the result as an element to the
        # current list
        if symbol == "(":
            list_content = []
            match_ctr = 1  # If 0, parenthesis has been matched
            while match_ctr != 0:
                i += 1
                if i >= len(input_norm):
                    raise ValueError("Invalid input: Unmatched open parenthesis.")
                symbol = input_norm[i]
                if symbol == "(":
                    match_ctr += 1
                elif symbol == ")":
                    match_ctr -= 1
                if match_ctr != 0:
                    list_content.append(symbol)
            ast.append(get_ast(list_content))
        elif symbol == ")":  # Element should have been closed
            raise ValueError("Invalid input: Unmatched close parenthesis.")
        else:  # If the element is an atom, just add it to the current list
            try:
                ast.append(int(symbol))
            except ValueError:
                ast.append(symbol)
        i += 1
    return ast


def build_cx(cx: List) -> OrderedDict:
    _id = cx.pop(0)
    _slots = [s for s in cx]
    cx = OrderedDict()

    cx["SENSE"] = _id

    # def build_slot(slot):
    #     pprint(slot)

    #     pass

    # print(f"\nCX ID: {_id}")
    print(f"\n{_id}")
    # print(slots)
    # print()
    for slot in _slots:
        # print(slot)
        if slot[0] in LITERAL_KEYS:
            if slot[0] == "EXAMPLE-BINDINGS":
                _str = " ".join(slot[1]).strip()
                print(f"{slot[0]}\t{_str}")
                cx[slot[0]] = _str
            else:
                _str = " ".join(slot[1:]).strip('"').strip()
                print(f"{slot[ 0]}\t{_str}")
                cx[slot[0]] = _str
        # else:
        # print(f"\n{slot[0]}\t{slot[1:]}")
        # print(f"\n{slot[0]}")
        # print(f"\n\t")
        # build_slot(slot[1])

        elif slot[0] == "SYN-STRUC":
            print(f"{slot[0]}")
            pprint(slot[1])
            # for element in slot[1]:
            #     print(element)
        elif slot[0] == "SEM-STRUC":
            print(f"{slot[0]}")
            pprint(slot[1:])

        # if the first element
    return cx


def parse_lisp(input_str) -> List[dict]:
    input_norm = normalize_str(input_str)
    lisp_cxs = get_ast(input_norm)

    cxs = []

    for c in lisp_cxs:
        # parse the construction into a python-readable dictionary
        cx = build_cx(c)
        cxs.append(cx)

    return cxs


if __name__ == "__main__":

    data = ""
    with open("../knowledge/constructions/speech-acts-lexicon.lisp", "r") as file:
        data = file.read()  # .replace('\n', '')

    a = parse_lisp(data)
