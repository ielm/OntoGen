from rs_converter import *
from lexicon_converter import *
import sys

## This top level script obtains two optional arguments:
##   a) input file name - the file must be a well formed lisp version of ONTO lexicon
##      residing in the same directory with this script
##      IF the file name is missing then 'lexicon.lisp' will be used
##   b) output file name - specifies a name for the generated python version of the lexicon.
##      If a name is not present then the input file name is used with the '.py'
##      extension (instead of '.lisp')
##       The resulting .py file (together with the intermediate .json file) will appear in this directory.
##
##  USAGE:  python3.5 run_lex_conversion.py <lex-file.lisp> <lex-file.py>
##
## IMPORTANT: the first thing you need to do is to COPY <lex-file-name>.lisp into this directory.
##
##  Conversion lexicon from Lisp into Python is a two-step process:
##  1) converting lisp expression into JSON format using RosettaStone parser which
##      requires a SINGLE lisp expression.
##
##      NOTE: make sure there is one extra set of parenthesis around all lexicon entries
##            in the input file for this parser to function properly
##
##  2) converting JSON format into Python structures
##
##  NOTE: During the conversion process there might be a need to modify the input .lisp lexicon file.
##
##  AFTER conversion is executed successfully proceed with the following steps:
##   a) copy both the final .lisp and .py lexicon versions into the SmallSem/SmallSem/data directory;
##   b) copy the final .lisp file into the SmallSem/OntoSem2LISP directory
##
##

inputfile = "driving_lexicon.lisp"
outputfile = "driving_lexicon.py"

if len(sys.argv) > 1:
    inputfile = sys.argv[1]

if len(sys.argv) > 2:
    outputfile = sys.argv[2]

# call RosettaStone parser
jfile = convert_lisp_to_json(inputfile)

# call JSON to PYTHON converter
lexicon_converter(infile=jfile, outfile=outputfile)
