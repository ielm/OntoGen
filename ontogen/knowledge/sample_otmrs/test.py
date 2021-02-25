import json
import ast

from pprint import pprint


if __name__ == "__main__":

    with open("TMR-results-full_2.txt", "r") as file:
        data = file.read()
        res = ast.literal_eval(data)

    for tmr in res:
        print()
        print(tmr["sentence"])
        pprint(tmr["results"][0]["TMR"])
        # pprint([{key: item} for key, item in tmr["results"][0]["TMR"].items() if key == key.upper()])
