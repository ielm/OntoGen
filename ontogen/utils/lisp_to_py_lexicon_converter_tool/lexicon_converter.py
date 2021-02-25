import json
from pprint import PrettyPrinter
from collections import OrderedDict


def print_obj_2(obj):
    p = PrettyPrinter(indent=2, width=75)
    p.pprint(obj)


top_level_not_nested = ["SUBJECT", "DIRECTOBJECT", "INDIRECTOBJECT"]

any_level_not_nested = [
    "NUM",
    "PREP-PART",
    "PREP",
    "CONTENT-MARKER",
    "PUNCT",
    "CONJ",
    "ADV",
    "V",
    "INF",
    "AUX",
]  # 'ART', 'ADJ',??

syn_nested = [
    "COMP",
    "XCOMP",
    "PP",
    "PP-ADJUNCT",
    "MODS",
    "OBJ",
    "NP",
    "N",
    "DET",
    "CL",
    "CONTAINS",
    "INF-CL",
    "VERB-NEG",
    "QUANTIFIER",
    "ART",
    "ADJ",
]

syn_elt_counts = {}
sem_elt_counts = {}

single_elements = ["ROOT", "SUBJECT", "DIRECTOBJECT", "INDIRECTOBJECT", "CAT", "OPT"]

range_or_sem_operators = [
    ">=<",
    "<",
    ">",
    "><",
    "<<",
    ">>",
    "<=",
    ">=",
    "=",
    "OR",
    "NOT",
    "AND",
]

mp_names = [
    "SEEK-SPECIFICSTION",
    "APPLY-MEANING",
    "FIX-CASE-ROLE",
    "DELIMIT-SCALE",
    "SPECIFY-APPROXIMATION",
    "TRIGGER-REFERENCE",
    "FIND-ANCHOR-TIME",
    "SELECT-FROM-END",
    "COMBINE-TIME",
    "FIND-ANCHOR-AMOUNT",
    "COMBINE-AMOUNT",
    "FIND-ANCHOR-SPEAKER",
    "FIND-ANCHOR-PLACE",
    "ENSURE-COREFERENCE",
    "PASS-THROUGH-MEANING",
    "DECREASE-VALUE",
    "EXPLOIT-FRONTING-ARGUMENT",
    "SEEK-EVENT",
    "FIND-PRECEDING-SET",
    "CALCULATE-QUOTIENT",
    "FIX-VARIABLES",
]

###############################################################
# takes lexicon - a list of entries in JSON format and converts
# into the needed Python format
###################################
def convert_lexicon(entries, trace=True):
    lex = {}
    count = 0
    senses = 0
    for item in entries:
        # the first item in the list is a lex concept e.g. DOG
        count += 1
        # print('entry ',count, item[0])
        lex[item[0]] = convert_lex_entry(
            item[1:], item[0], trace
        )  # one entry w/o entry name
        senses += len(lex[item[0]])

    print("\n Output Lexicon has ", count, " entries and ", senses, " senses.")
    return lex


###############################################################
# takes a list of senses from one lex entry in JSON format
# [<sense1>,[<list of attributes>,<sense2><list...>]
# and converts to the needed Python format
###################################
def convert_lex_entry(all_senses, entry_name, trace):
    senses = {}
    for one_sense in all_senses:
        if trace:
            print(
                "FROM convert_lex_entry: length=", len(one_sense), "entry=", one_sense
            )
        # the first item is a sense name
        if type(one_sense[0]) is str:
            if trace:
                print("\n     sense=", one_sense[0])  ###

            # check for duplicates, skip them if found
            if one_sense[0] in senses:
                print("\n SKIPPING DUPLICATE SENSE = ", one_sense[0])
            else:
                senses[one_sense[0]] = convert_sense(
                    one_sense[0], one_sense[1:], entry_name, trace
                )
        else:
            print("Unknown sense name, SKIPPING ", one_sense[0])
            break
    return senses


###########################################################
# processes one sense of a lexicon entry
####################################
def convert_sense(sense_name, sense_attrs, entry_name, trace):

    attr_dic = OrderedDict()
    if trace:
        print("   === sense_attrs =", sense_attrs)
    for attrs in sense_attrs:
        if trace:
            print("      attrs =", attrs)

        if attrs[0] == "SYN-STRUC":
            attr_dic[attrs[0]] = convert_syn_struc(sense_name, attrs[1], trace)
        elif attrs[0] == "SEM-STRUC":
            if len(attrs) == 1:
                attr_dic[attrs[0]] = ""
            elif attrs[1] == "NIL":
                attr_dic[attrs[0]] = ""
            elif len(attrs[1]) == 1:  # a case of <concept> or $VAR#
                if attrs[1][0].find("$VAR", 0) == 0:
                    attrs[1][0] = "^" + attrs[0]
                attr_dic[attrs[0]] = attrs[1][0]

            else:
                attr_dic[attrs[0]] = convert_sem_struc(
                    sense_name, attrs[1:], entry_name, trace
                )
            if trace:
                print("     attr_dic[attrs[0]]=", attr_dic[attrs[0]])

        elif attrs[0] == "MEANING-PROCEDURES":
            if attrs[1] == "NIL":
                attr_dic[attrs[0]] = "NIL"
            else:  # pass a list of procedures (not the first item)
                attr_dic[attrs[0]] = convert_mproc(sense_name, attrs[1:], trace)

        elif type(attrs) is list and type(attrs[0]) is str:
            if trace:
                print("------ from convert_sense, attrs=", attrs)
            attr_dic[attrs[0]] = attrs[1]
        else:
            print("sense_name:", sense_name, " Unknown item ", attrs[0])
            return False

    return attr_dic


##############################################
def convert_syn_struc(sense_name, syn_struc, trace):

    # syn_dic={}
    syn_dic = OrderedDict()

    global syn_elt_counts
    syn_elt_counts = {}  # reset

    if trace:
        print("\nConvert_syn_struc: sense_name=", sense_name, ", syn_struc=", syn_struc)

    for attrs in syn_struc:
        if trace:
            print("    FROM convert_syn_struc: syn_str attrs =", attrs)

        if attrs[0] in syn_nested:
            if trace:
                print("          ", attrs[0], "in syn_nested")
            syn_dic[create_syn_elt_name(attrs[0])] = nested(sense_name, attrs[1], trace)

        elif attrs[0] in top_level_not_nested or attrs[0] in any_level_not_nested:
            if trace:
                print("          ", attrs[0], "in NOT nested")
            syn_dic[create_syn_elt_name(attrs[0])] = not_nested(
                sense_name, attrs[1], trace
            )

        elif type(attrs[0]) is str:
            if trace:
                print("          ", attrs[0], "is a string")
            if attrs[0] == "ROOT" and (
                (type(attrs[1]) is str and attrs[1].find("$VAR", 0) < 0)
                or type(attrs[1]) is list
            ):
                syn_dic["ROOT-WORD"] = attrs[1]
            else:
                syn_dic[attrs[0]] = attrs[1]
        else:
            print("sense_name: ", sense_name, " Unknown item ", attrs[0])
            return False

    print("--- sense = ", sense_name)

    # print('===sense= ', sense_name, ' SYN_elt_count = ', syn_elt_counts)
    ## print elt counts ONLY there is at least one count>0

    ##    count = 0
    ##    for i in syn_elt_counts.keys():
    ##        if syn_elt_counts[i] >count: count = syn_elt_counts[i]
    ##    if count > 0:
    ##        syn_counts={}
    ##        for i in syn_elt_counts.keys():
    ##            if syn_elt_counts[i]>0 : syn_counts[i]=syn_elt_counts[i]
    ##        print('=sense=', sense_name, 'SYN= ', syn_counts)

    return syn_dic


############################################
## takes an element, updates syn_elt_counts dict; start numbering from 0
## creates a name in the format <element>-<count>
## UNLESS the element is in single_elements list, OR the number = 0
#############################################
def create_syn_elt_name(elt):
    global syn_elt_counts

    if elt in ("OBJ", "FORM"):
        return elt

    if elt in single_elements:
        return elt
    if elt in syn_elt_counts:
        syn_elt_counts[elt] += 1
    else:
        syn_elt_counts[elt] = 0
    if syn_elt_counts[elt] == 0:
        return elt
    else:
        return elt + "-" + str(syn_elt_counts[elt])


#############################################
##  similar to create_syn_elt_name; ignores 'NULL-SEM'
##  NOTE: the 'VALUE' notation is treated in a similar way,
##        but locally to SEM-STRUC levels
#############################################
def create_sem_elt_name(elt):
    global sem_elt_counts

    if elt in (
        "NULL-SEM",
        "DOMAIN",
        "RANGE",
        "CARDINALITY",
        "BENEFICIARY",
        "EFFECT",
        "SCOPE",
        "TYPE",
        "ATTRIBUTED-TO",
        "CONSCIOUS",
        "DEFAULT",
        "HAS-NAME",
        "HAS-SURNAME",
        "HAS-PERSONAL-NAME",
        "MONTH",
        "DAY",
        "YEAR",
        "EXPERIENCER",
        "MEASURED-IN",
        "RELATION",
        "CARDINALITY",
        "DEFAULT-MEASURE",
    ):
        return elt

    if elt in sem_elt_counts:
        sem_elt_counts[elt] += 1
    else:
        sem_elt_counts[elt] = 0
    if sem_elt_counts[elt] == 0:
        return elt
    else:
        return elt + "-" + str(sem_elt_counts[elt])


##########################################
def nested(sense_name, nested, trace):
    dic = OrderedDict()
    global syn_elt_counts

    if trace:
        print("started nested: sense_name=", sense_name, ", nested=", nested)

    for attrs in nested:
        if trace:
            print("  from nested, arg =", attrs)

        if attrs[0] in syn_nested:
            dic1 = OrderedDict()
            for one in attrs[1]:
                if one[0] in any_level_not_nested:
                    dic1[create_syn_elt_name(one[0])] = not_nested(
                        sense_name, one[1], trace
                    )
                elif one[0] in syn_nested:
                    dic2 = OrderedDict()
                    for two in one[1]:
                        if two[0] in any_level_not_nested:
                            dic2[create_syn_elt_name(two[0])] = not_nested(
                                sense_name, two[1], trace
                            )
                        elif two[0] in syn_nested:
                            dic3 = OrderedDict()
                            for three in two[1]:
                                if three[0] in any_level_not_nested:
                                    dic3[create_syn_elt_name(three[0])] = not_nested(
                                        sense_name, three[1], trace
                                    )
                                elif three[0] in syn_nested:

                                    print(
                                        "---sense_name:",
                                        sense_name,
                                        " from 3rd loop in syn_nested (What to DO???): ",
                                        "\n--- key=",
                                        two[0],
                                        " value=",
                                        two[1],
                                    )
                                    return False
                                elif type(three[0]) is str:
                                    if three[0] == "ROOT" and (
                                        (
                                            type(three[1]) is str
                                            and three[1].find("$VAR", 0) < 0
                                        )
                                        or type(three[1]) is list
                                    ):
                                        dic3["ROOT-WORD"] = three[1]
                                    else:  ###=== check if create name is needed !!!!
                                        dic3[create_syn_elt_name(three[0])] = three[1]
                                else:
                                    print(
                                        "sense_name: ",
                                        sense_name,
                                        " From loop in syn_nested : Unknown item ",
                                        three[0],
                                    )
                                    return False
                            dic2[two[0]] = dic3

                        elif type(two[0]) is str:
                            if (
                                two[0] == "ROOT"
                                and type(two[1]) is str
                                and (two[1].find("$VAR", 0) < 0)
                                or type(two[1]) is list
                            ):
                                dic2["ROOT-WORD"] = two[1]
                            else:  ###=== check if create name is needed !!!!
                                dic2[create_syn_elt_name(two[0])] = two[1]
                        else:
                            print(
                                "sense_name: ",
                                sense_name,
                                " From loop in syn_nested : Unknown item ",
                                one[0],
                            )
                            return False
                    dic1[one[0]] = dic2

                elif type(one[0]) is str:
                    if (
                        one[0] == "ROOT"
                        and type(one[1]) is str
                        and (one[1].find("$VAR", 0) < 0)
                        or type(one[1]) is list
                    ):
                        dic1["ROOT-WORD"] = one[1]
                    else:  ###=== check if create name is needed !!!!
                        dic1[create_syn_elt_name(one[0])] = one[1]
                else:
                    print(
                        "sense_name: ",
                        sense_name,
                        " From loop in syn_nested : Unknown item ",
                        one[0],
                    )
                    return False
            dic[create_syn_elt_name(attrs[0])] = dic1

        elif attrs[0] in any_level_not_nested:
            dic[create_syn_elt_name(attrs[0])] = not_nested(sense_name, attrs[1], trace)

        elif type(attrs[0]) is str:
            if attrs[0] == "ROOT" and (
                (type(attrs[1]) is str and attrs[1].find("$VAR", 0) < 0)
                or (type(attrs[1]) is not str)
            ):
                dic["ROOT-WORD"] = attrs[1]
            else:  ###=== check if create name is needed !!!!
                if trace:
                    print("   ==attrs=", attrs)
                dic[create_syn_elt_name(attrs[0])] = attrs[1]
        else:
            print("sense_name: ", sense_name, " From nested: Unknown item ", attrs[0])
            return False

    return dic


#############################################
# a simple case of one dictionary
def not_nested(sense_name, flat, trace):
    flat_dic = OrderedDict()
    global syn_elt_counts

    if trace:
        print("   From not_nested; ARG=", flat)
    for one in flat:
        if type(one[0]) is str:
            if (one[0] == "ROOT") and (
                (type(one[1]) is str and one[1].find("$VAR", 0) < 0)
                or type(one[1]) is list
            ):
                flat_dic["ROOT-WORD"] = one[1]

                ## if the first element is in syn_nested, call nested function
            elif one[0] in syn_nested:
                if trace:
                    print(
                        "   FROM not_nested: one =",
                        one,
                        "\n",
                        "       len(one)=",
                        len(one),
                        ", one[0]=",
                        one[0],
                        ", one[1]=",
                        one[1],
                    )
                res = nested(sense_name, one[1], trace)
                flat_dic[create_syn_elt_name(one[0])] = res
            else:
                flat_dic[create_syn_elt_name(one[0])] = one[1]
        else:
            print("sense_name: ", sense_name, "Unknown item ", one[0])
            return False

    return flat_dic


########################################################
# process the top level of SEM-STRUC;
#  replace $VAR# with ^$VAR#
########################################################
def convert_sem_struc(sense_name, sem_struc, entry_name, trace):
    global sem_elt_counts
    sem_elt_counts = {}  # reset
    sem_dic = OrderedDict()

    sem_struc = add_caret(sem_struc)  # add caret to $VAR#
    if trace:
        print(
            "\n\n====sense=", sense_name, " sem_str top level =", sem_struc
        )  #########

    for attrs in sem_struc:  ## top level
        if trace:
            print("\n  sem_str top item =", attrs)

        if type(attrs[0]) is str:  # the first string on the top level on sem-struc is
            # 1) a concept, (literal or ^$VAR#), 2) ASPECT, 3) REFSEM#, 4) MODALITY
            # 5) a comparison operator
            if len(attrs) == 1:  # e.g. (dog) e.g. (^$VAR3)
                sem_dic[attrs[0]] = ""

            elif attrs[0] in [
                "<",
                ">",
                "><",
                "<=",
                ">=",
                ">=<",
                "<<",
                ">>",
                "=",
                "GREATER-THAN",
                "LESS-THAN",
            ]:
                sem_dic["CONSTRAINT"] = attrs

            elif (
                len(attrs[1]) == 1
            ):  # e.g. attrs == (refsem1 (COUNTRY)) => refsem1 : COUNTRY
                sem_dic[attrs[0]] = attrs[1]

            elif len(attrs[1]) > 1:
                if (
                    attrs[1][0] in range_or_sem_operators
                    or attrs[1][0] in mp_names
                    or type(attrs[1][0]) is int
                    or type(attrs[1][0]) is float
                ):
                    sem_dic[attrs[0]] = attrs[1]
                else:
                    key = attrs[0]  # add '-#' to MODALITY and to ATTRIBUTE
                    # (a concept inside multiple AND-CONJ# senses)
                    if key in ("MODALITY", "ATTRIBUTE"):
                        key = create_sem_elt_name(key)
                        if trace:
                            print("   MODALITY, key =", key)
                    sem_dic[key] = create_sem_dict(
                        sense_name, attrs[1:], entry_name, key, trace
                    )
            else:
                print("sense_name: ", sense_name, " Unknown item", attrs)
                return False
        else:
            print("sense_name: ", sense_name, " Unknown item (non-string)", attrs[0])
            return False

    ###print('====sense= ', sense_name, ' SEM_elt_count = ', sem_elt_counts)
    ## print elt counts ONLY there is at least one count>0
    count = 0
    for i in sem_elt_counts.keys():
        if sem_elt_counts[i] > count:
            count = sem_elt_counts[i]
    if count > 0:
        sem_counts = {}
        for i in sem_elt_counts.keys():
            if sem_elt_counts[i] > 0:
                sem_counts[i] = sem_elt_counts[i]
        ##print('=sense=', sense_name, 'SEM=', sem_counts)

    return sem_dic


#############################################################################
# key is one of MODALITY, REFSEM#, etc.
#  sem-struc is a portion of sem-struc representing attributes for the key
###########################################################################
def create_sem_dict(sense_name, sem_struc, entry_name, key, trace):
    global sem_elt_counts

    sem2_dict = OrderedDict()
    if trace:
        print(
            "\n From create_sem_dic:",
            ", sense=",
            sense_name,
            " sem_str 2nd level =",
            sem_struc,
        )

    for attrs in sem_struc:  ## second level
        count_value = -1  # local to the level count; reset here
        if trace:
            print("\n     sem_str 2nd level elt attrs=", attrs)

        # print(attrs)

        if type(attrs[0]) is not str:
            print("sense_name: ", sense_name, " Unknown item (non-string)", attrs[0])
            break

        elif (
            len(attrs) == 2
            and type(attrs[1]) is list
            and (attrs[0] in ("SEM", "DEFAULT") and entry_name != "DEFAULT")
        ):
            if trace:
                print("       CASE-0 -SEM- attrs[1]=", attrs[1])

            sem2_dict[attrs[0]] = attrs[1]

        elif (
            len(attrs) == 2
            and type(attrs[1]) is list
            and attrs[0] not in ("SEM", "DEFAULT")
            and attrs[1][0] in ("SEM", "DEFAULT")
            and entry_name != "DEFAULT"
        ):
            if trace:
                print("       CASE-0~ -SEM- attrs[1]=", attrs[1])

            sem2_dict[attrs[0]] = {attrs[1][0]: attrs[1][1]}

        elif (
            len(attrs) == 2
            and type(attrs[1]) is list
            and type(attrs[1][0]) is str
            and (
                attrs[1][0] in range_or_sem_operators
                or attrs[1][0] in mp_names
                or type(attrs[1][0]) is int
                or type(attrs[1][0]) is float
            )
        ):

            if trace:
                print("       CASE-1 attrs[1]=", attrs[1])

            if attrs[0] == "VALUE":
                count_value += 1
                elt_name = "VALUE" if count_value < 1 else "VALUE-" + str(count_value)
            else:
                elt_name = create_sem_elt_name(attrs[0])

            sem2_dict[elt_name] = attrs[1]

        elif (
            len(attrs) == 2
            and type(attrs[1]) is list
            and type(attrs[1][0]) is str
            and len(attrs[1]) > 2
        ) or (len(attrs) > 2 and len(attrs[2]) > 1):
            # for cases (refsem (modality (scope...)(...)),
            #      e.g. (refsem (marry (agent (value ^$var1)(agent (value ^$var3))) -PROPOSE-V3
            #        RECALL-V5, SIMILAR-ADJ2
            # loop thru elements of the list
            if trace:
                print(" sense_name=", sense_name, " CASE-2 attrs=", attrs)
            if trace:
                print(
                    "---line 433 before calling create_sem_elt_name on attrs[0]=",
                    attrs[0],
                )

            if key.find("REFSEM") < 0:  # skip REFSEMs
                attrs[0] = create_sem_elt_name(
                    attrs[0]
                )  # PLAY-v5 (COMPETE, (AGENT, (VALUE', ^$VAR1))
                #                (AGENT, (VALUE', ^$VAR2)))

            if attrs[0] in [
                "COLOR",
                "ELEMENTS",
                "NOT-ELEMENTS",
                "MEMBER-TYPE",
                "HAS-OBJECT-AS-PART",
            ] and (
                type(attrs[1]) is str
                or (
                    attrs[1][0] not in ("VALUE", "DOMAIN", "RANGE", "SEM")
                    and attrs[1][0] not in mp_names
                )
            ):
                if type(attrs[1]) is str:
                    sem2_dict[attrs[0]] = attrs[
                        1:
                    ]  # e.g. CREME_DE_MENTHE-N1 ['COLOR', 'WHITE', 'GREEN']
                elif (
                    len(attrs) == 2
                    and type(attrs[1]) is list
                    and attrs[1][0] != "VALUE"
                ):
                    sem2_dict[attrs[0]] = attrs[
                        1
                    ]  # e.g. WILDLIFE-N1 (NOT-ELEMENTS (HUMAN,CAT,DOG...))
                elif len(attrs) == 3 and type(attrs[2]) is list:
                    sem2_dict[attrs[0]] = attrs[1]
                    sem2_dict[attrs[2][0]] = attrs[2][
                        1
                    ]  # e.g. STAPLE-N2 (ELEMENTS', (MILK, BREAD,...),
                    #                (COMPLETE, NO))
            else:
                sem2_dict[attrs[0]] = OrderedDict()
                count_value = -1  # local to the level count; reset here
                count_sem = -1  # local to the level count; reset here
                for item in attrs[1:]:
                    if trace:
                        print("        level 2 breadth, item=", item)

                    if item[0] in mp_names:
                        sem2_dict[attrs[0]][item[0]] = item[1]

                    elif item[0] in ("SEM", "DEFAULT") and entry_name != "DEFAULT":
                        # item[1] can be of any type
                        count_sem += 1
                        if item[0] == "SEM":
                            elt_name = "SEM"
                            if count_sem > 0:
                                elt_name = "SEM-" + str(count_sem)
                            sem2_dict[attrs[0]][elt_name] = item[1]
                            if trace:
                                print(
                                    " line 467: item=",
                                    item,
                                    ", count_sem=",
                                    count_sem,
                                    ", elt_name=",
                                    elt_name,
                                )
                        else:
                            sem2_dict[attrs[0]][item[0]] = item[1]

                    elif len(item) == 2 and (
                        type(item[1]) is int
                        or type(item[1]) is str
                        or type(item[1]) is float  # e.g. (VALUE REFSEM1) (VALUE ^$var1)
                    ):  #  e.g. (age 12)
                        if item[0] == "VALUE":
                            count_value += 1
                            elt_name = (
                                "VALUE"
                                if count_value < 1
                                else "VALUE-" + str(count_value)
                            )
                        else:
                            if trace:
                                print(
                                    "---line 479 before calling create_sem_elt_name on item[0]=",
                                    item[0],
                                )
                            elt_name = create_sem_elt_name(item[0])

                        sem2_dict[attrs[0]][elt_name] = item[1]

                    elif type(item[1]) is str:
                        if item[0] == "VALUE":
                            count_value += 1
                            elt_name = (
                                "VALUE"
                                if count_value < 1
                                else "VALUE-" + str(count_value)
                            )
                        else:
                            if trace:
                                print(
                                    "---line 490 before calling create_sem_elt_name on item[0]=",
                                    item[0],
                                )
                            elt_name = create_sem_elt_name(item[0])
                        if trace:
                            print(
                                "        item[0] == VALUE, item[1]=",
                                item[1],
                                "len(item)=",
                                len(item),
                            )
                            ## case of (ELELMENT (VALUE ^$VAR1 ^$VAR3 ...)
                        if len(item) == 2:
                            sem2_dict[attrs[0]][elt_name] = item[1]
                        else:
                            sem2_dict[attrs[0]][elt_name] = item[1:]

                    elif (
                        item[1][0] in range_or_sem_operators
                        or item[1][0] in mp_names
                        or type(item[1][0]) is int
                        or type(item[1][0]) is float
                    ):
                        ## and type(item[1][1]) is not list)???
                        ## print('       item[1][0] in MP etc. item[1]=',item[1])
                        if item[0] == "VALUE":
                            count_value += 1
                            elt_name = (
                                "VALUE"
                                if count_value < 1
                                else "VALUE-" + str(count_value)
                            )
                        else:
                            if trace:
                                print(
                                    "---line 509 before calling create_sem_elt_name on item[0]=",
                                    item[0],
                                )
                            elt_name = create_sem_elt_name(item[0])

                        sem2_dict[attrs[0]][elt_name] = item[1]

                    elif len(item) >= 2:
                        if trace:
                            print("-- line 516: item=", item, "(len>=2)")
                            print(
                                "-- line 516: before calling create_sem_elt_name on item[0]=",
                                item[0],
                            )
                        item[0] = create_sem_elt_name(item[0])

                        d4 = OrderedDict()
                        count_value = -1  # local to the level count; reset here
                        count_sem = -1  # local to the level count; reset here
                        for i in item[1:]:
                            if trace:
                                print("          loop item, i=", i)  ####

                            if type(i[1]) is str:
                                if i[0] == "VALUE":
                                    count_value += 1
                                    elt_name = (
                                        "VALUE"
                                        if count_value < 1
                                        else "VALUE-" + str(count_value)
                                    )
                                else:
                                    if trace:
                                        print(
                                            "-- line 532: before calling create_sem_elt_name on i[0]=",
                                            i[0],
                                        )
                                    elt_name = create_sem_elt_name(i[0])

                                d4[elt_name] = i[1]

                            elif type(i[1]) in (
                                int,
                                float,
                                str,
                            ):  #  e.g. (age 12), (value ^$var1)
                                if trace:
                                    print(" line 539: i=", i)

                                if i[0] == "VALUE":
                                    count_value += 1
                                    elt_name = (
                                        "VALUE"
                                        if count_value < 1
                                        else "VALUE-" + str(count_value)
                                    )
                                else:
                                    if trace:
                                        print(
                                            "-- line 546: before calling create_sem_elt_name on i[0]=",
                                            i[0],
                                        )
                                    elt_name = create_sem_elt_name(i[0])
                                d4[elt_name] = i[1]

                            elif i[0] == "SEM":  # i[1] can be of any type
                                if trace:
                                    print("            i[0]=", i[0], ", i[1]=", i[1])

                                count_sem += 1
                                elt_name = (
                                    "SEM"
                                    if count_value < 1
                                    else "SEM-" + str(count_sem)
                                )
                                d4[elt_name] = i[1]

                            elif (
                                i[0] == "DEFAULT" and entry_name != "DEFAULT"
                            ):  # i[1] can be of any type
                                if trace:
                                    print("            i[0]=", i[0], ", i[1]=", i[1])

                                count_sem += 1
                                elt_name = (
                                    "DEFAULT"
                                    if count_value < 1
                                    else "DEFAULT-" + str(count_sem)
                                )
                                d4[elt_name] = i[1]

                            elif (
                                i[1][0] in range_or_sem_operators
                                or i[1][0] in mp_names
                                or type(i[1][0]) is int
                                or type(i[1][0]) is float
                            ):
                                ###and type(i[1][1]) is not list) ???

                                # e.g. (age (>< 14 15)) e.g. (sem (not mental-object))
                                # e.g. (rank (12 16))
                                if i[0] == "VALUE":
                                    count_value += 1
                                    elt_name = (
                                        "VALUE"
                                        if count_value == 0
                                        else "VALUE-" + str(count_value)
                                    )
                                else:
                                    if trace:
                                        print(
                                            "-- line 575: before calling create_sem_elt_name on i[0]=",
                                            i[0],
                                        )
                                    elt_name = create_sem_elt_name(i[0])
                                d4[elt_name] = i[1]

                            elif type(i[1]) is list:
                                if type(i[1][1]) is str:
                                    # e.g.(sibling (gender male)) e.g. (agent (value ^$VAR1))
                                    if i[1][0] == "VALUE":
                                        count_value += 1
                                        elt_name = (
                                            "VALUE"
                                            if count_value < 1
                                            else "VALUE-" + str(count_value)
                                        )
                                    else:
                                        if trace:
                                            print(
                                                "-- line 587: before calling create_sem_elt_name on i[1][0]=",
                                                i[1][0],
                                            )
                                        elt_name = create_sem_elt_name(i[1][0])

                                    if i[0] == "VALUE":
                                        count_value += 1
                                        elt1_name = (
                                            "VALUE"
                                            if count_value < 1
                                            else "VALUE-" + str(count_value)
                                        )
                                    else:
                                        if trace:
                                            print(
                                                "-- line 595: before calling create_sem_elt_name on i[0]=",
                                                i[0],
                                            )
                                        elt1_name = create_sem_elt_name(i[0])
                                    d4[elt1_name] = {elt_name: i[1][1]}

                        # end loop
                        sem2_dict[attrs[0]][item[0]] = d4

            # end loop
        elif type(attrs[1]) is str:  # e.g. attrs ==(range yes)

            if trace:
                print("       CASE-3 attrs[1]=", attrs[1])

            if attrs[0] == "VALUE":
                count_value += 1
                elt_name = "VALUE" if count_value < 1 else "VALUE-" + str(count_value)
            else:
                if trace:
                    print(
                        "-- line 612: before calling create_sem_elt_name on attrs[0]=",
                        attrs[0],
                    )
                elt_name = create_sem_elt_name(attrs[0])
            sem2_dict[elt_name] = attrs[1]

        elif type(attrs[1]) is int or type(attrs[1]) is float:  #  e.g. (age 12)

            if trace:
                print("       CASE-4 attrs[1]=", attrs[1])

            sem2_dict[attrs[0]] = attrs[1]
        elif (
            attrs[1][0] in range_or_sem_operators
            or attrs[1][0] in mp_names
            or type(attrs[1][0]) is int
            or type(attrs[1][0]) is float
        ):
            ## and type(attrs[1][1]) is not list)???
            # e.g. (age (>< 14 15)) e.g. (sem (not mental-object)) e.g.(rank (12 16)

            if trace:
                print("       CASE-5 attrs[1]=", attrs[1])

            if attrs[0] == "VALUE":
                count_value += 1
                elt_name = "VALUE" if count_value < 1 else "VALUE-" + str(count_value)
            else:
                if trace:
                    print(
                        "-- line 633: before calling create_sem_elt_name on attrs[0]=",
                        attrs[0],
                    )

                elt_name = create_sem_elt_name(attrs[0])
            sem2_dict[elt_name] = attrs[1]

        elif type(attrs[1]) is list and len(attrs[1]) == 1:
            if trace:
                print("       CASE-6 attrs[1]=", attrs[1])

            if attrs[0] == "VALUE":
                count_value += 1
                elt_name = "VALUE" if count_value < 1 else "VALUE-" + str(count_value)
            else:
                if trace:
                    print(
                        "-- line 645: before calling create_sem_elt_name on attrs[0]=",
                        attrs[0],
                    )
                elt_name = create_sem_elt_name(attrs[0])
            sem2_dict[elt_name] = attrs[1][0]

        elif type(attrs[1]) is list and len(attrs[1]) > 1:
            if trace:
                print("       CASE-7 attrs[1]=", attrs[1], " attrs[0]=", attrs[0])

            if type(attrs[1][1]) is str:
                # e.g.(sibling (gender male)) e.g.(agent (value ^$VAR1))
                if attrs[1][0] == "VALUE":
                    count_value += 1
                    elt_name = (
                        "VALUE" if count_value < 1 else "VALUE-" + str(count_value)
                    )
                else:
                    if trace:
                        print(
                            "-- line 659: before calling create_sem_elt_name on attrs[1][0]=",
                            attrs[1][0],
                        )
                    elt_name = create_sem_elt_name(attrs[1][0])

                if attrs[0] == "VALUE":
                    count_value += 1
                    elt1_name = (
                        "VALUE" if count_value < 1 else "VALUE-" + str(count_value)
                    )
                else:
                    if trace:
                        print(
                            "-- line 667: before calling create_sem_elt_name on attrs[0]=",
                            attrs[0],
                        )
                    elt1_name = create_sem_elt_name(attrs[0])
                sem2_dict[elt1_name] = {elt_name: attrs[1][1]}

            elif type(attrs[1][1]) in [int, float]:
                # e.g.(human (some-attr 1))
                if trace:
                    print(
                        "-- line 674: before calling create_sem_elt_name on:",
                        attrs[1][0],
                        ", and",
                        attrs[0],
                    )
                elt_name = create_sem_elt_name(attrs[1][0])
                elt1_name = create_sem_elt_name(attrs[0])
                sem2_dict[elt1_name] = {elt_name: attrs[1][1]}

            elif type(attrs[1][1]) is list:
                # e.g. (HAS-SOCIAL-ROLE (DOMAIN (VALUE ^$VAR2)) ....)

                sem3_dict = OrderedDict()
                count_value = -1  # local to the level count; reset here
                count_sem = -1  # local to the level count; reset here
                for one in attrs[1:]:
                    if trace:
                        print("       sem_str 3rd level elt =", one)
                    if type(one[1]) is str:  # e.g. attrs ==(range yes)
                        if one[0] == "VALUE":
                            count_value += 1
                            elt_name = (
                                "VALUE"
                                if count_value < 1
                                else "VALUE-" + str(count_value)
                            )
                        else:
                            if trace:
                                print(
                                    "-- line 693: before calling create_sem_elt_name on one[0]=",
                                    one[0],
                                )
                            elt_name = create_sem_elt_name(one[0])
                        sem3_dict[elt_name] = one[1]

                    elif type(one[1]) is int or type(one[1]) is float:  #  e.g. (age 12)
                        if one[0] == "VALUE":
                            count_value += 1
                            elt_name = (
                                "VALUE"
                                if count_value < 1
                                else "VALUE-" + str(count_value)
                            )
                        else:
                            if trace:
                                print(
                                    "-- line 703: before calling create_sem_elt_name on one[0]=",
                                    one[0],
                                )
                            elt_name = create_sem_elt_name(one[0])
                        sem3_dict[elt_name] = one[1]
                    elif one[1][0] in range_or_sem_operators or one[1][0] in mp_names:
                        ## and type(one[1][1]) is not list)???

                        # e.g. (age (>< 14 15)) e.g. (sem (not mental-object))
                        if one[0] == "VALUE":
                            count_value += 1
                            elt_name = (
                                "VALUE"
                                if count_value < 1
                                else "VALUE-" + str(count_value)
                            )
                        else:
                            if trace:
                                print(
                                    "-- line 715: before calling create_sem_elt_name on one[0]=",
                                    one[0],
                                )
                            elt_name = create_sem_elt_name(one[0])
                        sem3_dict[elt_name] = one[1]

                    elif type(one[1]) is list:
                        if type(one[1][1]) in [str, int, float]:
                            if one[0] == "VALUE":
                                count_value += 1
                                elt1_name = (
                                    "VALUE"
                                    if count_value < 1
                                    else "VALUE-" + str(count_value)
                                )
                            else:
                                if trace:
                                    print(
                                        "-- line 726: before calling create_sem_elt_name on one[0]=",
                                        one[0],
                                    )
                                elt1_name = create_sem_elt_name(one[0])

                                # e.g.(sibling (gender male)) e.g. (agent (value ^$VAR1))
                            if one[1][0] == "VALUE":
                                count_value += 1
                                elt_name = (
                                    "VALUE"
                                    if count_value < 1
                                    else "VALUE-" + str(count_value)
                                )
                            else:
                                if trace:
                                    print(
                                        "-- line 735: before calling create_sem_elt_name on one[1][0]=",
                                        one[1][0],
                                    )
                                elt_name = create_sem_elt_name(one[1][0])

                            sem3_dict[elt1_name] = {elt_name: one[1][1]}

                        elif type(one[1][1]) is list:
                            if trace:
                                print(
                                    "       CASE-8 one =", one, ", attrs[1]=", attrs[1]
                                )

                            if (
                                one[1][0] in ("SEM", "DEFAULT")
                                and entry_name != "DEFAULT"
                            ):
                                sem3_dict[one[0]] = {one[1][0]: one[1][1]}
                            else:
                                sem3_dict[one[0]] = {
                                    one[1][0]: {one[1][1][0]: one[1][1][1]}
                                }

                    # print ('         sem_str 3rd level dict =',sem3_dict)
                ## end of loop
                sem2_dict[attrs[0]] = sem3_dict
        else:
            print("sense_name: ", sense_name, " Unknown item ", attrs[1])
            return False

    return sem2_dict


###########################################
# takes a list; return that list with all
# appearances of $VAR# replaced with ^$VAR#
############################################
def add_caret(sem_struc):
    res = []
    for one in sem_struc:
        if type(one) is int or type(one) is float:
            res.append(one)
        elif type(one) is str:
            if one.find("$VAR", 0) == 0:
                res.append("^" + one)
            else:
                res.append(one)
        else:  # one is list
            res.append(add_caret(one))
    return res


#############################################
# mproc is a list of lists related to ONE function call each.
# within mproc replace (VALUE ^$VAR#) with ^$VAR#;
#  replace (VALUE REFSEM#*) with REFSEM#*
#     restore '^' at the beginning of $var...
#  the resulting format is ((<fn name> <arg>* <slot name, slot value>*))
#    e.g. [[FIX-CASE-ROLE, '$VAR2', 'REFSEM1.RANGE, ['PERSON', 'FIRST']...]...]
#
####################################################################
def convert_mproc(sense_name, mproc, trace):
    mp_list = []

    for one_mp in mproc:
        if trace:
            print("   one_mp item =", one_mp)
        arg_list = [one_mp[0]]
        for arg in one_mp[1:]:  # the first item is ALWAYS a function name
            if trace:
                print("    (1) arg=", arg)
            if type(arg) is list:
                if len(arg) == 2 and arg[0] == "VALUE":
                    if type(arg[1]) is str and arg[1].find("$VAR", 0) == 0:
                        # replace (value var) with var;  add prefix '^'
                        arg_list.append("^" + arg[1])
                    elif type(arg[1]) is str and arg[1].find("REFSEM", 0) == 0:
                        arg_list.append(arg[1])
                    else:  # NOT $var or refsem - can be any value: a number or a string
                        # print('sense_name: ',sense_name,' Unknown item in MP after VALUE:', arg[1])
                        arg_list.append(arg[1])

                elif len(arg) == 2 and arg[0] != "VALUE":  # e.g. [TARGET [VALUE $VAR1]]
                    if (
                        type(arg[0]) is str
                        and type(arg[1]) is list
                        and len(arg[1]) == 2
                        and arg[1][0] == "VALUE"
                        and arg[1][1].find("$VAR") == 0
                    ):
                        arg_list.append([arg[0], "^" + arg[1][1]])
                    else:
                        arg_list.append(arg)

                elif (
                    len(arg) >= 2 and type(arg[0]) is str and arg[0] != "VALUE"
                ):  # e.g. (BLOCK-REFERENCE (TARGET (VALUE ^$VAR0))
                    arg_list2 = [arg[0]]
                    if trace:
                        print("     (2)NOT value: arg=", arg)
                    for one in arg[1:]:
                        if len(one) == 2 and one[0] == "VALUE":
                            if type(one[1]) is str and one[1].find("$VAR", 0) == 0:
                                # replace (value var) with var
                                arg_list2.append("^" + one[1])
                            elif type(one[1]) is str and one[1].find("REFSEM", 0) == 0:
                                arg_list2.append(one[1])
                            else:
                                if trace:
                                    print(
                                        "     (3) one=", one, ", arg_list2=", arg_list2
                                    )
                                arg_list2.append(one[1])
                        elif len(one) == 2:
                            if trace:
                                print(
                                    "     (4) one=",
                                    one,
                                )
                            arg_list2.append(one)
                    arg_list.append(arg_list2)

                else:
                    if trace:
                        print("     (4) arg=", arg)
                    arg_list.append(arg)
            else:
                ##print('sense_name: ',sense_name,'  CHECK TYPE of MP arg: ', arg)
                arg_list.append(arg)

        mp_list.append(arg_list)

    return mp_list


##############################################
def display_lexicon(lex, top=True, syn=True, sem=True):
    print("Lexicon has ", len(lex), "entries")
    for entry in lex.keys():
        print("{0:>18} {1} senses".format(entry, len(lex[entry])))
    for entry in lex.keys():
        print("\n", entry)
        for sense in lex[entry]:
            print("\n  ", sense)
            for one in lex[entry][sense]:
                if one == "SYN-STRUC" and syn:
                    print("    ", one)
                    for el in lex[entry][sense][one]:
                        print("      ", el, ":  ", lex[entry][sense][one][el])
                elif one == "SEM-STRUC" and sem:
                    print(
                        "    ",
                        one,
                        ": ",
                    )
                    if type(lex[entry][sense][one]) is str:
                        print("       ", lex[entry][sense][one])
                    else:
                        for i in lex[entry][sense][one]:
                            print("       ", i, ": ", lex[entry][sense][one][i])
                elif one not in ("SYN-STRUC", "SEM-STRUC") and top:
                    print("    ", one, ": ", lex[entry][sense][one])
                else:
                    pass


####################################
def get_stats(lexicon):
    top_entries = len(lexicon)
    synonyms = 0
    hyponyms = 0
    total_senses = 0
    senses = {}
    entries_w_syn = 0
    entries_w_hyp = 0
    one_sense = 0
    max_senses = [1, 0]

    for one in lexicon.keys():
        total_senses += len(lexicon[one])
        senses[one] = len(lexicon[one])
        if len(lexicon[one]) == 1:
            one_sense += 1
        if len(lexicon[one]) > max_senses[1]:
            max_senses[1] = len(lexicon[one])
            max_senses[0] = one

        for sense in lexicon[one].keys():
            if "SYNONYMS" in lexicon[one][sense]:
                syn = lexicon[one][sense]["SYNONYMS"]
                if syn != "NIL":
                    synonyms += len(syn)
                    entries_w_syn += 1
            else:
                print("  Sense ", sense, "does NOT have SYNONYMS field")

            if "HYPONYMS" in lexicon[one][sense]:
                hyp = lexicon[one][sense]["HYPONYMS"]
                if hyp != "NIL":
                    hyponyms += len(hyp)
                    entries_w_hyp += 1
            else:
                print("  Sense ", sense, "does NOT have HYPONYMS field")

    print("{0:>23} {1}".format("# top entries", top_entries))
    print(
        "{0:>23} {1} {2:>10} {3}".format(
            "# synonyms", synonyms, "# entries with synonyms:", entries_w_syn
        )
    )
    print(
        "{0:>23} {1} {2:>10} {3}".format(
            "# hyponyms", hyponyms, "# entries with hyponyms:", entries_w_hyp
        )
    )
    print("\n{0:>23} {1}".format("# senses in top entries", total_senses))
    print(
        "{0:>23} {1}".format(
            "total senses + synonyms + hyponyms", total_senses + synonyms + hyponyms
        )
    )

    print("{0:>23} {1} ".format("# entries with 1 sense", one_sense))
    print(
        "{0:>23} {1} {2:>10} {3}".format(
            "MAX senses per entry", max_senses[1], "in entry", max_senses[0]
        )
    )

    print("\n  entries with 20 and more senses: ")
    for one in sorted(senses.keys()):
        if senses[one] >= 20:
            print("{0:>18} {1}".format(one, senses[one]))


###########################################
# get data from json file; convert to Python structures,
#   format and same into a file
#
#########################################


def lexicon_converter(infile="test.json", outfile=""):
    f = open(infile, "r")
    # dump json expression into a variable
    lex = json.load(f)
    f.close()
    print(
        "--Loaded file:",
        infile,
        ". Length of json lexicon =",
        len(lex),
        "\n  starting conversion...\n",
    )

    # main conversion happens here
    lexicon = convert_lexicon(lex, trace=False)

    # save new lexicon in a file
    if not outfile:
        ind = infile.find(".")
        # output file name is the same as the input file, with extension .py
        #  e.g. infile = test.json, jfile = test.py
        outfile = infile[0:ind] + ".py"

    f = open(outfile, "w")
    # write sorted and formatted lexicon
    f.write("{")  # start main dictionary
    first = True
    for entry in sorted(lexicon.keys()):
        if first:
            first = False
        else:
            f.write(",\n")
        s = '\n"' + entry + '"' + " :\n"
        f.write(s)
        json.dump(lexicon[entry], f, indent=1)

    f.write("\n}")  # end main dictionary
    f.close()
    print("    saved lexicon in", outfile)

    ##display_lexicon (lexicon, top=False, syn=False,) # sem=False)
    # get_stats(lexicon)
