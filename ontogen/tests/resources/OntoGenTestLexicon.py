{
    "A": {
        "A-ART1": {
            "CAT": "ART",
            "DEF": "indicates no coreference",
            "EX": "A cat walked in the room",
            "COMMENTS": "",
            "TMR-HEAD": "$VAR1",
            "SYN-STRUC": {
                "ART": {"ROOT": "$VAR0", "CAT": "ART"},
                "ROOT": "$VAR1",
                "CAT": "N",
            },
            "SEM-STRUC": "",
            "OUTPUT-SYNTAX": "NP",
            "MEANING-PROCEDURES": [
                ["BLOCK-REFERENCE", ["TARGET", "^$VAR1"], ["DETERMINATE", "NO"]]
            ],
            "EXAMPLE-BINDINGS": ["YOU", "HAVE", "A-0", "DOG-1"],
            "EXAMPLE-DEPS": [["DET", "$VAR1", "$VAR0"]],
            "SYNONYMS": ["AN"],
            "HYPONYMS": "NIL",
        }
    },
    "AFTER": {
        "AFTER-PREP601": {
            "CAT": "PREP",
            "EX": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "V": {"ROOT": "$VAR1", "ROOT-WORD": ["TURN", "STOP"], "CAT": "V"},
                "ROOT": "$VAR0",
                "CAT": "PREP",
                "N": {"ROOT": "$VAR2", "CAT": "N"},
            },
            "SEM-STRUC": {"^$VAR1": {"AFTER": {"VALUE": "^$VAR2"}}},
            "EXAMPLE-BINDINGS": [
                "THE",
                "MAN",
                "TURNED-1",
                "AFTER-0",
                "THE",
                "BRIDGE-2",
            ],
        }
    },
    "AND": {
        "AND-CONJ601": {
            "CAT": "CONJ",
            "DEF": "'and' when it joins 2 imperatives with no shared objects; temporal ordering assumed;\nsynonym is \u2018and_then\u2019 or just \u2018then\u2019",
            "EX": "Turn left now and turn right at the corner.\nTurn right after the restaurant and then immediately turn left. \nTurn right then go left at the corner.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "V": {"ROOT": "$VAR1", "CAT": "V"},
                "ROOT": "$VAR0",
                "CAT": "CONJ",
                "ADV": {"ROOT": "$VAR3", "ROOT-WORD": "THEN", "CAT": "ADV", "OPT": "+"},
                "V-1": {"ROOT": "$VAR2", "CAT": "V"},
            },
            "SEM-STRUC": {
                "^$VAR1": {"BEFORE": {"VALUE": "^$VAR2"}},
                "^$VAR3": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": [
                "TURN-1",
                "LEFT",
                "AND-0",
                "THEN-3",
                "TURN-2",
                "RIGHT",
                "AT",
                "THE",
                "CORNER",
            ],
            "SYNONYMS": ["AND_THEN", "THEN"],
        },
        "AND-CONJ602": {
            "CAT": "CONJ",
            "COMMENTS": "NEED SPECIAL ENTRY WHEN FIRST VERB IS ",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "N": {"ROOT": "$VAR1", "ROOT-WORD": "CROSS", "CAT": "N"},
                "ROOT": "$VAR0",
                "CAT": "CONJ",
                "ADV": {"ROOT": "$VAR3", "ROOT-WORD": "THEN", "CAT": "ADV", "OPT": "+"},
                "V": {"ROOT": "$VAR2", "CAT": "V"},
            },
            "SEM-STRUC": {
                "^$VAR1": {"BEFORE": {"VALUE": "^$VAR2"}},
                "^$VAR3": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": [
                "CROSS-1",
                "THE",
                "RIVER",
                "AND-0",
                "THEN-3",
                "TURN-2",
                "AT",
                "THE",
                "CORNER",
            ],
            "SYNONYMS": ["AND_THEN", "THEN"],
        },
    },
    "APPRECIATE": {
        "APPRECIATE-V510": {
            "CAT": "V",
            "DEF": "",
            "EX": "I would (really) appreciate it if you (could/would) X...",
            "COMMENTS": "indirect speech act",
            "TMR-HEAD": "NIL",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "N": {"ROOT": "$VAR1", "CAT": "N"},
                "AUX": {"ROOT": "$VAR2", "ROOT-WORD": ["WILL", "WOULD"], "CAT": "AUX"},
                "ADV": {
                    "ROOT": "$VAR3",
                    "ROOT-WORD": "REALLY",
                    "CAT": "ADV",
                    "OPT": "+",
                },
                "ROOT": "$VAR0",
                "CAT": "V",
                "N-1": {"ROOT": "$VAR4", "ROOT-WORD": "IT", "CAT": "N"},
                "PREP": {"ROOT": "$VAR5", "ROOT-WORD": "IF", "CAT": "PREP"},
                "N-2": {"ROOT": "$VAR8", "CAT": "N"},
                "AUX-1": {
                    "ROOT": "$VAR6",
                    "ROOT-WORD": ["COULD", "WOULD"],
                    "CAT": "AUX",
                    "OPT": "+",
                },
                "V": {"ROOT": "$VAR7", "CAT": "V"},
            },
            "SEM-STRUC": {
                "REQUEST-ACTION": {
                    "FORMALITY": "OBSEQUIOUS",
                    "AGENT": {"VALUE": "^$VAR1"},
                    "THEME": {"VALUE": "^$VAR7", "BENEFICIARY": {"VALUE": "^$VAR8"}},
                },
                "^$VAR7": {"AGENT-1": {"VALUE": "^$VAR8"}},
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR3": {"NULL-SEM": "+"},
                "^$VAR4": {"NULL-SEM": "+"},
                "^$VAR5": {"NULL-SEM": "+"},
                "^$VAR6": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": [
                "I-1",
                "WOULD-2",
                "REALLY-3",
                "APPRECIATE-0",
                "IT-4",
                "IF-5",
                "YOU-8",
                "WOULD-6",
                "HIT-7",
                "THE",
                "BUILDING",
            ],
            "MEANING-PROCEDURES": [["FIX-CASE-ROLE", "^$VAR7", "^$VAR8", "AGENT"]],
            "SYNONYMS": "NIL",
            "HYPONYMS": "NIL",
        }
    },
    "AT": {
        "AT-PREP601": {
            "CAT": "PREP",
            "EX": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "V": {"ROOT": "$VAR1", "ROOT-WORD": ["TURN", "STOP"], "CAT": "V"},
                "ROOT": "$VAR0",
                "CAT": "PREP",
                "N": {"ROOT": "$VAR2", "CAT": "N"},
            },
            "SEM-STRUC": {"^$VAR1": {"LOCATION": {"VALUE": "^$VAR2"}}},
            "EXAMPLE-BINDINGS": ["THE", "MAN", "TURNED-1", "AT-0", "THE", "BRIDGE-2"],
            "SYNONYMS": ["ON", "ONTO"],
        },
        "AT-PREP602": {
            "CAT": "PREP",
            "EX": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "V": {"ROOT": "$VAR1", "ROOT-WORD": ["MAKE", "HANG"], "CAT": "V"},
                "ADJ": {"ROOT": "$VAR2", "CAT": "ADJ", "OPT": "+"},
                "N": {"ROOT": "$VAR3", "CAT": "N", "OPT": "+"},
                "ROOT": "$VAR0",
                "CAT": "PREP",
                "N-1": {"ROOT": "$VAR4", "CAT": "N"},
            },
            "SEM-STRUC": {"^$VAR1": {"LOCATION": {"VALUE": "^$VAR4"}}},
            "EXAMPLE-BINDINGS": ["MAKE-1", "A", "LEFT-2", "AT-0", "THE", "BRIDGE-4"],
            "SYNONYMS": ["ON", "ONTO"],
        },
    },
    "BEACH": {
        "BEACH-N1": {
            "CAT": "N",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "N",
                "N": {
                    "ROOT": "$VAR1",
                    "ROOT-WORD": ["STREET", "ST*PERIOD*"],
                    "CAT": "N",
                    "OPT": "+",
                },
            },
            "SEM-STRUC": {"STREET": {"HAS-NAME": "BEACH"}},
            "EXAMPLE-BINDINGS": ["THE", "MAN", "TURNED", "AT", "BEACH-0", "STREET-1"],
            "SYNONYMS": ["BEACH_STREET", "BEACH_ST*PERIOD*"],
        }
    },
    "BRIDGE": {
        "BRIDGE-N600": {
            "CAT": "N",
            "SYN-STRUC": {"ROOT": "$VAR0", "CAT": "N"},
            "SEM-STRUC": "BRIDGE",
        }
    },
    "CAN": {
        "CAN-AUX510": {
            "CAT": "AUX",
            "DEF": "",
            "EX": "Can you please hit the building?",
            "COMMENTS": "Indirect speech act",
            "TMR-HEAD": "NIL",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "AUX",
                "N": {"ROOT": "$VAR1", "CAT": "N"},
                "V": {"ROOT": "$VAR2", "ROOT-WORD": "PLEASE", "CAT": "V"},
                "V-1": {"ROOT": "$VAR3", "CAT": "V"},
                "PUNCT": {
                    "ROOT": "$VAR4",
                    "ROOT-WORD": "*QUESTION_MARK*",
                    "CAT": "PUNCT",
                },
            },
            "SEM-STRUC": {
                "REQUEST-ACTION": {
                    "FORMALITY": "POLITE",
                    "AGENT": "*SPEAKER*",
                    "THEME": {"VALUE": "^$VAR3"},
                    "BENEFICIARY": {"VALUE": "^$VAR1"},
                },
                "^$VAR3": {"AGENT-1": {"VALUE": "^$VAR1"}},
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR4": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": [
                "CAN-0",
                "YOU-1",
                "PLEASE-2",
                "HIT-3",
                "THE",
                "BUILDING",
                "?-4",
            ],
            "MEANING-PROCEDURES": [["FIX-CASE-ROLE", "^$VAR3", "^$VAR1", "AGENT"]],
            "SYNONYMS": ["WOULD"],
            "HYPONYMS": "NIL",
        },
        "CAN-AUX511": {
            "CAT": "AUX",
            "DEF": "",
            "EX": "Can you hit the building?",
            "COMMENTS": "Indirect speech act; need this one without the PLEASE",
            "TMR-HEAD": "NIL",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "AUX",
                "N": {"ROOT": "$VAR1", "CAT": "N"},
                "V": {"ROOT": "$VAR3", "CAT": "V"},
                "PUNCT": {
                    "ROOT": "$VAR4",
                    "ROOT-WORD": "*QUESTION_MARK*",
                    "CAT": "PUNCT",
                },
            },
            "SEM-STRUC": {
                "REQUEST-ACTION": {
                    "FORMALITY": "INFORMAL",
                    "AGENT": "*SPEAKER*",
                    "THEME": {"VALUE": "^$VAR3"},
                    "BENEFICIARY": {"VALUE": "^$VAR1"},
                },
                "^$VAR3": {"AGENT-1": {"VALUE": "^$VAR1"}},
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR4": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["CAN-0", "YOU-1", "HIT-3", "THE", "BUILDING", "?-4"],
            "MEANING-PROCEDURES": [["FIX-CASE-ROLE", "^$VAR3", "^$VAR1", "AGENT"]],
            "SYNONYMS": ["WOULD"],
            "HYPONYMS": "NIL",
        },
    },
    "CORNER": {
        "CORNER-N600": {
            "CAT": "N",
            "DEF": "a street corner, corner of a room, etc.",
            "EX": "",
            "COMMENTS": "[D]",
            "TMR-HEAD": "NIL",
            "SYN-STRUC": {"ROOT": "$VAR0", "CAT": "N"},
            "SEM-STRUC": "CORNER",
            "OUTPUT-SYNTAX": "NIL",
            "MEANING-PROCEDURES": "NIL",
            "EXAMPLE-BINDINGS": "NIL",
            "EXAMPLE-DEPS": "NIL",
            "SYNONYMS": ["ANGLE"],
            "HYPONYMS": "NIL",
        }
    },
    "COULD": {
        "COULD-AUX510": {
            "CAT": "AUX",
            "DEF": "",
            "EX": "Could you please hit the building?",
            "COMMENTS": "Indirect speech act",
            "TMR-HEAD": "NIL",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "AUX",
                "N": {"ROOT": "$VAR1", "CAT": "N"},
                "V": {"ROOT": "$VAR2", "ROOT-WORD": "PLEASE", "CAT": "V"},
                "V-1": {"ROOT": "$VAR3", "CAT": "V"},
                "PUNCT": {
                    "ROOT": "$VAR4",
                    "ROOT-WORD": "*QUESTION_MARK*",
                    "CAT": "PUNCT",
                },
            },
            "SEM-STRUC": {
                "REQUEST-ACTION": {
                    "FORMALITY": "POLITE",
                    "AGENT": "*SPEAKER*",
                    "THEME": {"VALUE": "^$VAR3"},
                    "BENEFICIARY": {"VALUE": "^$VAR1"},
                },
                "^$VAR3": {"AGENT-1": {"VALUE": "^$VAR1"}},
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR4": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": [
                "COULD-0",
                "YOU-1",
                "PLEASE-2",
                "HIT-3",
                "THE",
                "BUILDING",
                "?-4",
            ],
            "MEANING-PROCEDURES": [["FIX-CASE-ROLE", "^$VAR3", "^$VAR1", "AGENT"]],
            "SYNONYMS": ["WOULD"],
            "HYPONYMS": "NIL",
        },
        "COULD-AUX511": {
            "CAT": "AUX",
            "DEF": "",
            "EX": "Could you hit the building?",
            "COMMENTS": "Indirect speech act; need this one without the PLEASE",
            "TMR-HEAD": "NIL",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "AUX",
                "N": {"ROOT": "$VAR1", "CAT": "N"},
                "V": {"ROOT": "$VAR3", "CAT": "V"},
                "PUNCT": {
                    "ROOT": "$VAR4",
                    "ROOT-WORD": "*QUESTION_MARK*",
                    "CAT": "PUNCT",
                },
            },
            "SEM-STRUC": {
                "REQUEST-ACTION": {
                    "FORMALITY": "NEUTRAL",
                    "AGENT": "*SPEAKER*",
                    "THEME": {"VALUE": "^$VAR3"},
                    "BENEFICIARY": {"VALUE": "^$VAR1"},
                },
                "^$VAR3": {"AGENT-1": {"VALUE": "^$VAR1"}},
                "^$VAR4": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["COULD-0", "YOU-1", "HIT-3", "THE", "BUILDING", "?-4"],
            "MEANING-PROCEDURES": [["FIX-CASE-ROLE", "^$VAR3", "^$VAR1", "AGENT"]],
            "SYNONYMS": ["WOULD"],
            "HYPONYMS": "NIL",
        },
    },
    "CROSS": {
        "CROSS-V600": {
            "CAT": "V",
            "SYN-STRUC": {
                "SUBJECT": {"ROOT": "$VAR1", "CAT": "N"},
                "ROOT": "$VAR0",
                "CAT": "V",
                "DIRECTOBJECT": {"ROOT": "$VAR2", "CAT": "N"},
            },
            "SEM-STRUC": {
                "CROSS": {"AGENT": {"VALUE": "^$VAR1"}, "THEME": {"VALUE": "^$VAR2"}}
            },
        },
        "CROSS-N600": {
            "CAT": "N",
            "COMMENTS": "Stanford thinks the imperative form is a noun",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "N",
                "N": {"ROOT": "$VAR2", "CAT": "N"},
            },
            "SEM-STRUC": {
                "CROSS": {"AGENT": {"VALUE": "*HEARER*"}, "THEME": {"VALUE": "^$VAR2"}}
            },
            "EXAMPLE-BINDINGS": ["CROSS-0", "THE", "RIVER-1"],
        },
    },
    "DESTINATION": {
        "DESTINATION-N600": {
            "CAT": "N",
            "DEF": "DRIVING DOMAIN",
            "EX": "YOUR DESTINATION IS ON THE LEFT.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "DET": {"ROOT": "$VAR1", "ROOT-WORD": "YOUR", "CAT": "DET"},
                "ROOT": "$VAR0",
                "CAT": "N",
                "V": {"ROOT": "$VAR2", "ROOT-WORD": "*BE*", "CAT": "V"},
                "PREP": {"ROOT": "$VAR3", "ROOT-WORD": "ON", "CAT": "PREP"},
                "ART": {"ROOT": "$VAR4", "ROOT-WORD": "THE", "CAT": "ART"},
                "ADJ": {"ROOT": "$VAR5", "ROOT-WORD": "LEFT", "CAT": "ADJ"},
            },
            "SEM-STRUC": {
                "PLACE": {"DESTINATION-OF": {"VALUE": "REFSEM1"}, "SIDE-RL": "LEFT"},
                "REFSEM1": {
                    "DRIVE": {
                        "AGENT": {"VALUE": "*HEARER*"},
                        "SCOPE-OF": {"VALUE": "REFSEM2"},
                    }
                },
                "REFSEM2": {"MODALITY": {"TYPE": "VOLATIVE", "VALUE": 1}},
            },
            "EXAMPLE-BINDINGS": [
                "YOUR-1",
                "DESTINATION-0",
                "IS-2",
                "ON-3",
                "THE-4",
                "LEFT-5",
            ],
        },
        "DESTINATION-N601": {
            "CAT": "N",
            "DEF": "DRIVING DOMAIN",
            "EX": "YOUR DESTINATION IS ON THE RIGHT.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "DET": {"ROOT": "$VAR1", "ROOT-WORD": "YOUR", "CAT": "DET"},
                "ROOT": "$VAR0",
                "CAT": "N",
                "V": {"ROOT": "$VAR2", "ROOT-WORD": "*BE*", "CAT": "V"},
                "PREP": {"ROOT": "$VAR3", "ROOT-WORD": "ON", "CAT": "PREP"},
                "ART": {"ROOT": "$VAR4", "ROOT-WORD": "THE", "CAT": "ART"},
                "ADJ": {"ROOT": "$VAR5", "ROOT-WORD": "RIGHT", "CAT": "ADJ"},
            },
            "SEM-STRUC": {
                "PLACE": {"DESTINATION-OF": {"VALUE": "REFSEM1"}, "SIDE-RL": "RIGHT"},
                "REFSEM1": {
                    "DRIVE": {
                        "AGENT": {"VALUE": "*HEARER*"},
                        "SCOPE-OF": {"VALUE": "REFSEM2"},
                    }
                },
                "REFSEM2": {"MODALITY": {"TYPE": "VOLATIVE", "VALUE": 1}},
            },
            "EXAMPLE-BINDINGS": [
                "YOUR-1",
                "DESTINATION-0",
                "IS-2",
                "ON-3",
                "THE-4",
                "RIGHT-5",
            ],
        },
    },
    "FOURTH": {
        "FOURTH-ADJ600": {
            "CAT": "ADJ",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "ADJ",
                "N": {"ROOT": "$VAR1", "CAT": "N"},
            },
            "SEM-STRUC": {
                "^$VAR1": {"ORDINALITY": 4, "MEMBER-OF": {"VALUE": "REFSEM1"}},
                "REFSEM1": ["SET"],
            },
            "EXAMPLE-BINDINGS": [
                "THE",
                "MAN",
                "TURNED",
                "AT",
                "THE",
                "SECOND-0",
                "STREET-1",
            ],
        }
    },
    "I": {
        "I-N1": {
            "CAT": "N",
            "DEF": "the first person singular pronoun",
            "EX": "I fell asleep.",
            "COMMENTS": "",
            "TMR-HEAD": "NIL",
            "SYN-STRUC": {"ROOT": "$VAR0", "CAT": "N", "TYPE": "PRO"},
            "SEM-STRUC": "HUMAN",
            "OUTPUT-SYNTAX": "NIL",
            "MEANING-PROCEDURES": [["TRIGGER-REFERENCE", ["SG-1-ALGORITHM"]]],
            "EXAMPLE-BINDINGS": "NIL",
            "EXAMPLE-DEPS": "NIL",
            "SYNONYMS": "NIL",
            "HYPONYMS": "NIL",
        }
    },
    "IMMEDIATELY": {
        "IMMEDIATELY-ADV600": {
            "CAT": "ADV",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "V": {"ROOT": "$VAR1", "CAT": "V"},
                "ROOT": "$VAR0",
                "CAT": "ADV",
            },
            "SEM-STRUC": {
                "MODALITY": {
                    "TYPE": "URGENCY",
                    "VALUE": 1,
                    "SCOPE": {"VALUE": "^$VAR1"},
                }
            },
            "EXAMPLE-BINDINGS": [
                "THE",
                "MAN",
                "TURNED-1",
                "IMMEDIATELY-0",
                "AFTER",
                "THE",
                "LIGHT",
            ],
        },
        "IMMEDIATELY-ADV601": {
            "CAT": "ADV",
            "SYN-STRUC": {"USE-EXAMPLE-BINDING": "T", "ROOT": "$VAR0", "CAT": "ADV"},
            "V": [["ROOT", "$VAR1"], ["CAT", "V"]],
            "SEM-STRUC": {
                "MODALITY": {
                    "TYPE": "URGENCY",
                    "VALUE": 1,
                    "SCOPE": {"VALUE": "^$VAR1"},
                }
            },
            "EXAMPLE-BINDINGS": [
                "THE",
                "MAN",
                "IMMEDIATELY-0",
                "TURNED-1",
                "AFTER",
                "THE",
                "LIGHT",
            ],
        },
    },
    "IN": {
        "IN-PREP600": {
            "CAT": "PREP",
            "DEF": "DRIVING DOMAIN",
            "EX": "IN X METERS/KM/MILES, TURN LEFT.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "PREP",
                "NUM": {"ROOT": "$VAR1", "CAT": "NUM"},
                "N": {
                    "ROOT": "$VAR2",
                    "ROOT-WORD": ["MILE", "KILOMETER", "METER"],
                    "CAT": "N",
                },
                "PUNCT": {
                    "ROOT": "$VAR3",
                    "ROOT-WORD": "*COMMA*",
                    "CAT": "PUNCT",
                    "OPT": "+",
                },
                "V": {
                    "ROOT": "$VAR4",
                    "ROOT-WORD": ["STOP", "TURN", "STAY", "YIELD"],
                    "CAT": "V",
                },
            },
            "SEM-STRUC": {
                "^$VAR4": {"DISTANCE": {"VALUE": "^$VAR2"}},
                "^$VAR3": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDING": ["IN-0", 1, -1, "MILE-2", "*COMMA*-3", "TURN-4", "LEFT"],
        }
    },
    "LEAVE": {
        "LEAVE-V601": {
            "CAT": "V",
            "DEF": "phrasal: <left + PP> meaning <turn left> at the place indicated by PP",
            "EX": "LEFT AT THE INTERSECTION.",
            "COMMENTS": "Note the checking condition \u2013 there cannot be a verb in this structure, otherwise it can mean <exactly + PP> (e.g. <Turn right right at the intersection>)",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "PREP": {
                    "ROOT": "$VAR1",
                    "ROOT-WORD": [
                        "AT",
                        "NEAR",
                        "BY",
                        "BESIDE",
                        "NEXT_TO",
                        "IN_FRONT_OF",
                        "BEFORE",
                        "AFTER",
                    ],
                    "CAT": "PREP",
                    "OPT": "+",
                },
                "ART": {"ROOT": "$VAR2", "ROOT-WORD": "THE", "CAT": "ART", "OPT": "+"},
                "N": {"ROOT": "$VAR3", "CAT": "N", "OPT": "+"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-LEFT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "LOCATION": {"VALUE": "^$VAR3"},
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR1": {"NULL-SEM": "+"},
            },
            "MEANING-PROCEDURES": [["SEEK-SPECIFICATION", "LOCATION", "AT", "^$VAR3"]],
            "EXAMPLE-BINDINGS": ["LEFT-0", "AT-1", "THE-2", "CORNER-3"],
        },
        "LEAVE-V602": {
            "CAT": "V",
            "DEF": "phrasal: <slight left + PP> meaning <turn slight left> at the place indicated by PP",
            "EX": "SLIGHT LEFT AT THE INTERSECTION.",
            "COMMENTS": "Note the checking condition \u2013 there cannot be a verb in this structure, otherwise it can mean <exactly + PP> (e.g. <Turn right right at the intersection>)",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ADJ": {"ROOT": "$VAR4", "ROOT-WORD": "SLIGHT", "CAT": "ADJ"},
                "ROOT": "$VAR0",
                "CAT": "V",
                "PREP": {
                    "ROOT": "$VAR1",
                    "ROOT-WORD": [
                        "AT",
                        "NEAR",
                        "BY",
                        "BESIDE",
                        "NEXT_TO",
                        "IN_FRONT_OF",
                        "BEFORE",
                        "AFTER",
                    ],
                    "CAT": "PREP",
                },
                "ART": {"ROOT": "$VAR2", "ROOT-WORD": "THE", "CAT": "ART"},
                "N": {"ROOT": "$VAR3", "CAT": "N"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-SLIGHT-LEFT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "LOCATION": {"VALUE": "^$VAR3"},
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR4": {"NULL-SEM": "+"},
                "^$VAR1": {"NULL-SEM": "+"},
            },
            "MEANING-PROCEDURES": [["SEEK-SPECIFICATION", "LOCATION", "AT", "^$VAR3"]],
            "EXAMPLE-BINDINGS": ["SLIGHT-4", "LEFT-0", "AT-1", "THE-2", "CORNER-3"],
        },
    },
    "LEFT": {
        "LEFT-N600": {
            "CAT": "N",
            "EX": "TAKE THE SECOND LEFT",
            "COMMENTS": "Used when  modified by an adjective, like 'second left'.  Then Stanford thinks it's a noun.\n              Note that the STREET REFSEM comes first, so that any modifiers like 'second' will get applied to it.",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "V": {"ROOT": "$VAR1", "ROOT-WORD": "TAKE", "CAT": "V"},
                "ROOT": "$VAR0",
                "CAT": "N",
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-LEFT": {
                    "AGENT": "*HEARER*",
                    "LOCATION": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": ["STREET"],
                "^$VAR1": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["TAKE-1", "THE", "SECOND", "LEFT-0"],
        },
        "LEFT-N601": {
            "CAT": "N",
            "EX": "Turn at THE SECOND LEFT",
            "COMMENTS": "Used when  modified by an adjective, like 'second left'.  Then Stanford thinks it's a noun.\n              Note that the STREET REFSEM comes first, so that any modifiers like 'second' will get applied to it.",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "V": {"ROOT": "$VAR1", "ROOT-WORD": "TURN", "CAT": "V"},
                "PREP": {"ROOT": "$VAR2", "ROOT-WORD": "AT", "CAT": "PREP"},
                "ROOT": "$VAR0",
                "CAT": "N",
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-LEFT": {
                    "AGENT": "*HEARER*",
                    "LOCATION": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": ["STREET"],
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR2": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["TURN-1", "AT-2", "THE", "SECOND", "LEFT-0"],
        },
        "LEFT-N602": {
            "CAT": "N",
            "EX": "TAKE THE SECOND LEFT",
            "COMMENTS": "Used when  modified by an adjective, like 'second left'.  Then Stanford thinks it's a noun.\n              Note that the STREET REFSEM comes first, so that any modifiers like 'second' will get applied to it.",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ADJ": {"ROOT": "$VAR1", "CAT": "ADJ"},
                "ROOT": "$VAR0",
                "CAT": "N",
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-LEFT": {
                    "AGENT": "*HEARER*",
                    "LOCATION": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": ["STREET"],
            },
            "EXAMPLE-BINDINGS": ["SECOND-1", "LEFT-0"],
        },
    },
    "LIGHT": {
        "LIGHT-N600": {
            "CAT": "N",
            "DEF": "DRIVING DOMAIN",
            "EX": "STOP AT THE NEXT LIGHT.",
            "COMMENTS": "",
            "SYN-STRUC": {"ROOT": "$VAR0", "CAT": "N"},
            "SEM-STRUC": "TRAFFIC-LIGHT",
        }
    },
    "MAKE": {
        "MAKE-V601": {
            "CAT": "V",
            "DEF": "phrasal: \u2018make a right turn\u2019; imperative verb and DO 'right turn'; I assume that PPs and adverbs can be compositionally added to this structure",
            "EX": "MAKE A RIGHT TURN. MAKE A RIGHT TURN AT THE CORNER. MAKE A RIGHT TURN\n    AFTER THE RESTAURANT. MAKE A RIGHT TURN IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "TENSE": ["INFINITIVE", "PROGRESSIVE"],
                "ART": {"ROOT": "$VAR1", "ROOT-WORD": "A", "CAT": "ART"},
                "ADJ": {"ROOT": "$VAR2", "ROOT-WORD": "RIGHT", "CAT": "ADJ"},
                "N": {"ROOT": "$VAR3", "ROOT-WORD": "TURN", "CAT": "N"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-RIGHT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR3": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["MAKE-0", "A-1", "RIGHT-2", "TURN-3"],
        },
        "MAKE-V602": {
            "CAT": "V",
            "DEF": "phrasal: \u2018make a left turn\u2019",
            "EX": "MAKE A LEFT TURN. MAKE A LEFT TURN AT THE CORNER. MAKE A LEFT TURN\n    AFTER THE RESTAURANT. MAKE A LEFT TURN IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "TENSE": ["INFINITIVE", "PROGRESSIVE"],
                "ART": {"ROOT": "$VAR1", "ROOT-WORD": "A", "CAT": "ART"},
                "ADJ": {"ROOT": "$VAR2", "ROOT-WORD": "LEFT", "CAT": "ADJ"},
                "N": {"ROOT": "$VAR3", "ROOT-WORD": "TURN", "CAT": "N"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-LEFT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR3": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["MAKE-0", "A-1", "LEFT-2", "TURN-3"],
        },
        "MAKE-V603": {
            "CAT": "V",
            "DEF": "phrasal: \u2018make a slight right turn\u2019",
            "EX": "MAKE A SLIGHT RIGHT TURN. MAKE A SLIGHT RIGHT TURN AT THE CORNER. MAKE\n    A SLIGHT RIGHT TURN AFTER THE RESTAURANT. MAKE A SLIGHT RIGHT TURN\n    IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "TENSE": ["INFINITIVE", "PROGRESSIVE"],
                "ART": {"ROOT": "$VAR1", "ROOT-WORD": "A", "CAT": "ART"},
                "ADJ": {"ROOT": "$VAR4", "ROOT-WORD": "SLIGHT", "CAT": "ADJ"},
                "N": {"ROOT": "$VAR2", "ROOT-WORD": "RIGHT", "CAT": ["ADJ", "N"]},
                "N-1": {"ROOT": "$VAR3", "ROOT-WORD": "TURN", "CAT": "N"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-SLIGHT-RIGHT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR3": {"NULL-SEM": "+"},
                "^$VAR4": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["MAKE-0", "A-1", "SLIGHT-4", "RIGHT-2", "TURN-3"],
        },
        "MAKE-V604": {
            "CAT": "V",
            "DEF": "phrasal: \u2018make a slight left turn\u2019",
            "EX": "MAKE A SLIGHT LEFT TURN. MAKE A SLIGHT LEFT TURN AT THE CORNER. MAKE A\n    SLIGHT LEFT TURN AFTER THE RESTAURANT. MAKE A SLIGHT LEFT TURN\n    IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "TENSE": ["INFINITIVE", "PROGRESSIVE"],
                "ART": {"ROOT": "$VAR1", "ROOT-WORD": "A", "CAT": "ART"},
                "ADJ": {"ROOT": "$VAR4", "ROOT-WORD": "SLIGHT", "CAT": "ADJ"},
                "N": {"ROOT": "$VAR2", "ROOT-WORD": "LEFT", "CAT": ["ADJ", "N"]},
                "N-1": {"ROOT": "$VAR3", "ROOT-WORD": "TURN", "CAT": "N"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-SLIGHT-LEFT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR3": {"NULL-SEM": "+"},
                "^$VAR4": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["MAKE-0", "A-1", "SLIGHT-4", "LEFT-2", "TURN-3"],
        },
        "MAKE-V605": {
            "CAT": "V",
            "DEF": "phrasal: \u2018make a u-turn\u2019",
            "EX": "MAKE A U-TURN. MAKE A U-TURN AT THE CORNER. MAKE A U-TURN AFTER THE\n    RESTAURANT. MAKE A U-TURN IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "TENSE": ["INFINITIVE", "PROGRESSIVE"],
                "ART": {"ROOT": "$VAR1", "ROOT-WORD": "A", "CAT": "ART"},
                "N": {
                    "ROOT": "$VAR3",
                    "ROOT-WORD": ["U-TURN", "UIE", "YUUWEE"],
                    "CAT": "N",
                },
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-UTURN": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR3": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["MAKE-0", "A-1", "U-TURN-3"],
            "SYNONYMS": ["PULL", "FLIP"],
        },
        "MAKE-V610": {
            "CAT": "V",
            "DEF": "phrasal: \u2018make a right'",
            "EX": "MAKE A RIGHT. MAKE A RIGHT AT THE CORNER. MAKE A RIGHT AFTER THE\n    RESTAURANT. MAKE A RIGHTIMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "TENSE": ["INFINITIVE", "PROGRESSIVE"],
                "ART": {"ROOT": "$VAR1", "ROOT-WORD": "A", "CAT": "ART"},
                "N": {"ROOT": "$VAR2", "ROOT-WORD": "RIGHT", "CAT": "N"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-RIGHT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR2": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["MAKE-0", "A-1", "RIGHT-2"],
            "SYNONYMS": ["TAKE"],
        },
        "MAKE-V611": {
            "CAT": "V",
            "DEF": "phrasal: \u2018make a left'",
            "EX": "MAKE A LEFT. MAKE A LEFT AT THE CORNER. MAKE A LEFT AFTER THE\n    RESTAURANT. MAKE A LEFT IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "TENSE": ["INFINITIVE", "PROGRESSIVE"],
                "ART": {"ROOT": "$VAR1", "ROOT-WORD": "A", "CAT": "ART"},
                "N": {
                    "ROOT": "$VAR2",
                    "ROOT-WORD": ["LEAVE", "LEFT"],
                    "CAT": ["V", "N"],
                },
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-LEFT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR2": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["MAKE-0", "A-1", "LEFT-2"],
            "SYNONYMS": ["TAKE"],
        },
        "MAKE-V612": {
            "CAT": "V",
            "DEF": "phrasal: \u2018make a left at the corner'",
            "EX": "MAKE A LEFT. MAKE A LEFT AT THE CORNER. MAKE A LEFT AFTER THE\n    RESTAURANT. MAKE A LEFT IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "TENSE": ["INFINITIVE", "PROGRESSIVE"],
                "ART": {"ROOT": "$VAR1", "ROOT-WORD": "A", "CAT": "ART"},
                "N": {
                    "ROOT": "$VAR2",
                    "ROOT-WORD": ["LEAVE", "LEFT"],
                    "CAT": ["V", "N"],
                },
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-LEFT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR2": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["MAKE-0", "A-1", "LEFT-2", "AT", "THE", "CORNER"],
            "SYNONYMS": ["TAKE"],
        },
        "MAKE-V613": {
            "CAT": "V",
            "DEF": "phrasal: \u2018make a slight right'",
            "EX": "MAKE A SLIGHT RIGHT. MAKE A SLIGHT RIGHT AT THE CORNER. MAKE A SLIGHT\n    RIGHT AFTER THE RESTAURANT. MAKE A SLIGHT RIGHT IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "TENSE": ["INFINITIVE", "PROGRESSIVE"],
                "ART": {"ROOT": "$VAR1", "ROOT-WORD": "A", "CAT": "ART"},
                "ADJ": {"ROOT": "$VAR3", "ROOT-WORD": "SLIGHT", "CAT": "ADJ"},
                "N": {"ROOT": "$VAR2", "ROOT-WORD": "RIGHT", "CAT": "N"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-SLIGHT-RIGHT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR2": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["MAKE-0", "A-1", "SLIGHT-3", "RIGHT-2"],
            "SYNONYMS": ["TAKE"],
        },
        "MAKE-V614": {
            "CAT": "V",
            "DEF": "phrasal: \u2018make a slight left'",
            "EX": "MAKE A SLIGHT LEFT. MAKE A SLIGHT LEFT AT THE CORNER. MAKE A SLIGHT\n    LEFT AFTER THE RESTAURANT. MAKE A SLIGHT LEFT IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "TENSE": ["INFINITIVE", "PROGRESSIVE"],
                "ART": {"ROOT": "$VAR1", "ROOT-WORD": "A", "CAT": "ART"},
                "ADJ": {"ROOT": "$VAR3", "ROOT-WORD": "SLIGHT", "CAT": "ADJ"},
                "N": {"ROOT": "$VAR2", "ROOT-WORD": "LEFT", "CAT": "N"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-SLIGHT-LEFT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR2": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["MAKE-0", "A-1", "SLIGHT-3", "LEFT-2"],
            "SYNONYMS": ["TAKE"],
        },
        "MAKE-V615": {
            "CAT": "V",
            "DEF": "phrasal: \u2018make a u-turn'",
            "EX": "MAKE A U-TURN. MAKE A U-TURN AT THE CORNER. MAKE A U-TURN AFTER THE\n    RESTAURANT. MAKE A U-TURN IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "TENSE": ["INFINITIVE", "PROGRESSIVE"],
                "ART": {"ROOT": "$VAR1", "ROOT-WORD": "A", "CAT": "ART"},
                "N": {
                    "ROOT": "$VAR2",
                    "ROOT-WORD": ["U-TURN", "UIE", "YUUWEE"],
                    "CAT": "N",
                },
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-UTURN": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR2": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["MAKE-0", "A-1", "U-TURN-2"],
            "SYNONYMS": ["TAKE", "PULL", "FLIP"],
        },
    },
    "MAN": {
        "MAN-N600": {
            "CAT": "N",
            "SYN-STRUC": {"ROOT": "$VAR0", "CAT": "N"},
            "SEM-STRUC": {"HUMAN": {"GENDER": "MALE"}},
        }
    },
    "MIND": {
        "MIND-V510": {
            "CAT": "AUX",
            "DEF": "",
            "EX": "Would you mind hitting the building?",
            "COMMENTS": "Indirect speech act",
            "TMR-HEAD": "NIL",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "AUX": {"ROOT": "$VAR1", "ROOT-WORD": "WOULD", "CAT": "AUX"},
                "N": {"ROOT": "$VAR2", "CAT": "N"},
                "ROOT": "$VAR0",
                "CAT": "V",
                "V": {"ROOT": "$VAR3", "CAT": "V"},
                "PUNCT": {
                    "ROOT": "$VAR4",
                    "ROOT-WORD": "*QUESTION_MARK*",
                    "CAT": "PUNCT",
                    "OPT": "+",
                },
            },
            "SEM-STRUC": {
                "REQUEST-ACTION": {
                    "FORMALITY": "POLITE",
                    "AGENT": "*SPEAKER*",
                    "BENEFICIARY": {"VALUE": "^$VAR2"},
                    "THEME": {"VALUE": "^$VAR3"},
                },
                "^$VAR3": {"AGENT-1": {"VALUE": "^$VAR2"}},
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR4": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": [
                "WOULD-1",
                "YOU-2",
                "MIND-0",
                "HITTING-3",
                "THE",
                "BUILDING",
                "?-4",
            ],
            "MEANING-PROCEDURES": [["FIX-CASE-ROLE", "^$VAR3", "^$VAR2", "AGENT"]],
            "SYNONYMS": "NIL",
            "HYPONYMS": "NIL",
        }
    },
    "NEXT": {
        "NEXT-ADJ600": {
            "CAT": "ADJ",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "ADJ",
                "N": {"ROOT": "$VAR1", "CAT": "N"},
            },
            "SEM-STRUC": {
                "^$VAR1": {"ORDINALITY": 1, "MEMBER-OF": {"VALUE": "REFSEM1"}},
                "REFSEM1": ["SET"],
            },
            "EXAMPLE-BINDINGS": [
                "THE",
                "MAN",
                "TURNED",
                "AT",
                "THE",
                "SECOND-0",
                "STREET-1",
            ],
        }
    },
    "NORTH": {
        "NORTH-N600": {
            "CAT": "N",
            "SYN-STRUC": {"ROOT": "$VAR0", "CAT": "N"},
            "SEM-STRUC": "NORTH",
        },
        "NORTH-N601": {
            "CAT": "N",
            "EX": "(GO TRAVEL DRIVE) NORTH ON BEACH STREET.",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "V": {
                    "ROOT": "$VAR1",
                    "ROOT-WORD": ["GO", "TRAVEL", "DRIVE"],
                    "CAT": "V",
                    "OPT": "+",
                },
                "ROOT": "$VAR0",
                "CAT": "N",
                "PREP": {"ROOT": "$VAR2", "ROOT-WORD": "ON", "CAT": "PREP", "OPT": "+"},
                "N": {"ROOT": "$VAR3", "CAT": "N", "OPT": "+"},
            },
            "SEM-STRUC": {
                "REQUEST-ACTION": {
                    "AGENT": "*SPEAKER*",
                    "BENEFICIARY": "*HEARER*",
                    "THEME": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {"DRIVE-VEHICLE": {"PATH": {"VALUE": "^$VAR3"}}},
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR2": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["DRIVE-1", "NORTH-0", "ON-2", "BEACH-3", "STREET"],
        },
    },
    "RIGHT": {
        "RIGHT-ADV601": {
            "CAT": "ADV",
            "DEF": "phrasal: \u2018right + PP\u2019 meaning \u2018turn right\u2019 at the place indicated by PP",
            "EX": "RIGHT AT THE INTERSECTION.",
            "COMMENTS": "Note the checking condition \u2013 there cannot be a verb in this structure, otherwise it can mean \u2018exactly + PP\u2019 (e.g., Turn right right at the intersection\u2019)",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "ADV",
                "PREP": {
                    "ROOT": "$VAR1",
                    "ROOT-WORD": [
                        "AT",
                        "NEAR",
                        "BY",
                        "BESIDE",
                        "NEXT_TO",
                        "IN_FRONT_OF",
                        "BEFORE",
                        "AFTER",
                    ],
                    "CAT": "PREP",
                    "OPT": "+",
                },
                "ART": {"ROOT": "$VAR2", "ROOT-WORD": "THE", "CAT": "ART", "OPT": "+"},
                "N": {"ROOT": "$VAR3", "CAT": "N", "OPT": "+"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-RIGHT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "LOCATION": {"VALUE": "^$VAR3"},
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR1": {"NULL-SEM": "+"},
            },
            "MEANING-PROCEDURES": [["SEEK-SPECIFICATION", "LOCATION", "AT", "^$VAR3"]],
            "EXAMPLE-BINDINGS": ["RIGHT-0", "AT-1", "THE-2", "CORNER-3"],
        },
        "RIGHT-N602": {
            "CAT": "N",
            "DEF": "phrasal: \u2018slight right + PP\u2019 meaning \u2018turn slight right\u2019 at the place indicated by PP",
            "EX": "SLIGHT RIGHT AT THE INTERSECTION.",
            "COMMENTS": "Note the checking condition \u2013 there cannot be a verb in this structure, otherwise it can mean \u2018exactly + PP\u2019 (e.g., Turn right right at the intersection\u2019)",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ADJ": {"ROOT": "$VAR4", "ROOT-WORD": "SLIGHT", "CAT": "ADJ"},
                "ROOT": "$VAR0",
                "CAT": "N",
                "PREP": {
                    "ROOT": "$VAR1",
                    "ROOT-WORD": [
                        "AT",
                        "NEAR",
                        "BY",
                        "BESIDE",
                        "NEXT_TO",
                        "IN_FRONT_OF",
                        "BEFORE",
                        "AFTER",
                    ],
                    "CAT": "PREP",
                },
                "ART": {"ROOT": "$VAR2", "ROOT-WORD": "THE", "CAT": "ART"},
                "N": {"ROOT": "$VAR3", "CAT": "N"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-SLIGHT-RIGHT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "LOCATION": {"VALUE": "^$VAR3"},
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR4": {"NULL-SEM": "+"},
                "^$VAR1": {"NULL-SEM": "+"},
            },
            "MEANING-PROCEDURES": [["SEEK-SPECIFICATION", "LOCATION", "AT", "^$VAR3"]],
            "EXAMPLE-BINDINGS": ["SLIGHT-4", "RIGHT-0", "AT-1", "THE-2", "CORNER-3"],
        },
        "RIGHT-N603": {
            "CAT": "N",
            "EX": "TAKE THE SECOND RIGHT",
            "COMMENTS": "Used when  modified by an adjective, like 'second left'.  Then Stanford thinks it's a noun.\n              Note that the STREET REFSEM comes first, so that any modifiers like 'second' will get applied to it.",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "V": {"ROOT": "$VAR1", "ROOT-WORD": "TAKE", "CAT": "V"},
                "ROOT": "$VAR0",
                "CAT": "N",
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-RIGHT": {
                    "AGENT": "*HEARER*",
                    "LOCATION": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": ["STREET"],
                "^$VAR1": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["TAKE-1", "THE", "SECOND", "RIGHT-0"],
        },
        "RIGHT-N604": {
            "CAT": "N",
            "EX": "Turn at THE SECOND LEFT",
            "COMMENTS": "Used when  modified by an adjective, like 'second left'.  Then Stanford thinks it's a noun.\n              Note that the STREET REFSEM comes first, so that any modifiers like 'second' will get applied to it.",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "V": {"ROOT": "$VAR1", "ROOT-WORD": "TURN", "CAT": "V"},
                "PREP": {"ROOT": "$VAR2", "ROOT-WORD": "AT", "CAT": "PREP"},
                "ROOT": "$VAR0",
                "CAT": "N",
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-RIGHT": {
                    "AGENT": "*HEARER*",
                    "LOCATION": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": ["STREET"],
                "^$VAR1": {"NULL-SEM": "+"},
                "^$VAR2": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["TURN-1", "AT-2", "THE", "SECOND", "RIGHT-0"],
        },
        "RIGHT-N605": {
            "CAT": "N",
            "EX": "SECOND RIGHT",
            "COMMENTS": "Used when  modified by an adjective, like 'second left'.  Then Stanford thinks it's a noun.\n              Note that the STREET REFSEM comes first, so that any modifiers like 'second' will get applied to it.",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ADJ": {"ROOT": "$VAR1", "CAT": "ADJ"},
                "ROOT": "$VAR0",
                "CAT": "N",
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-RIGHT": {
                    "AGENT": "*HEARER*",
                    "LOCATION": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": ["STREET"],
            },
            "EXAMPLE-BINDINGS": ["SECOND-1", "RIGHT-0"],
        },
    },
    "RIVER": {
        "RIVER-N600": {
            "CAT": "N",
            "SYN-STRUC": {"ROOT": "$VAR0", "CAT": "N"},
            "SEM-STRUC": "RIVER",
        }
    },
    "SECOND": {
        "SECOND-ADJ600": {
            "CAT": "ADJ",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "ADJ",
                "N": {"ROOT": "$VAR1", "CAT": "N"},
            },
            "SEM-STRUC": {
                "^$VAR1": {"ORDINALITY": 2, "MEMBER-OF": {"VALUE": "REFSEM1"}},
                "REFSEM1": ["SET"],
            },
            "EXAMPLE-BINDINGS": [
                "THE",
                "MAN",
                "TURNED",
                "AT",
                "THE",
                "SECOND-0",
                "STREET-1",
            ],
        }
    },
    "STOP": {
        "STOP-V600": {
            "CAT": "V",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "PREP": {
                    "ROOT": "$VAR1",
                    "ROOT-WORD": [
                        "AT",
                        "NEAR",
                        "BY",
                        "BESIDE",
                        "NEXT_TO",
                        "IN_FRONT_OF",
                        "BEFORE",
                        "AFTER",
                    ],
                    "CAT": "PREP",
                },
                "ART": {"ROOT": "$VAR2", "ROOT-WORD": "THE", "CAT": "ART"},
                "N": {"ROOT": "$VAR3", "CAT": "N"},
            },
            "SEM-STRUC": {
                "STOP-VEHICLE": {"AGENT": {"VALUE": "*HEARER*"}},
                "^$VAR2": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["STOP-0", "AT-1", "THE-2", "CORNER-3"],
        }
    },
    "STREET": {
        "STREET-N1": {
            "CAT": "N",
            "SYN-STRUC": {"ROOT": "$VAR0", "CAT": "N"},
            "SEM-STRUC": "STREET",
        }
    },
    "THE": {
        "THE-ART1": {
            "CAT": "ART",
            "DEF": "often indicates coreference",
            "EX": "The reason for the failure is clear",
            "COMMENTS": "",
            "TMR-HEAD": "$VAR1",
            "SYN-STRUC": {
                "ART": {"ROOT": "$VAR0", "CAT": "ART"},
                "ROOT": "$VAR1",
                "CAT": "N",
                "NUMBER": "SING",
            },
            "SEM-STRUC": "",
            "OUTPUT-SYNTAX": "NP",
            "MEANING-PROCEDURES": [["RESOLVE-REFERENCE", "^$VAR1"]],
            "EXAMPLE-BINDINGS": ["THE-0", "MAN-1", "HIT", "THE", "BUILDING"],
            "EXAMPLE-DEPS": [["DET", "$VAR1", "$VAR0"]],
            "SYNONYMS": "NIL",
            "HYPONYMS": "NIL",
        },
        "THE-ART2": {
            "CAT": "ART",
            "DEF": "with a plural, often refers to the complete set",
            "EX": "pick up the toys",
            "COMMENTS": "",
            "TMR-HEAD": "NIL",
            "SYN-STRUC": {
                "ART": {"ROOT": "$VAR0", "CAT": "ART"},
                "ROOT": "$VAR1",
                "CAT": "N",
                "NUMBER": "PL",
            },
            "SEM-STRUC": {
                "SET": {"MEMBER-TYPE": {"VALUE": "^$VAR1"}, "COMPLETE": "YES"}
            },
            "OUTPUT-SYNTAX": "NIL",
            "MEANING-PROCEDURES": "NIL",
            "EXAMPLE-BINDINGS": ["THE-0", "MEN-1", "HIT", "THE", "BUILDING"],
            "EXAMPLE-DEPS": [["DET", "$VAR1", "$VAR0"]],
            "SYNONYMS": "NIL",
            "HYPONYMS": "NIL",
        },
    },
    "THIRD": {
        "THIRD-ADJ600": {
            "CAT": "ADJ",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "ADJ",
                "N": {"ROOT": "$VAR1", "CAT": "N"},
            },
            "SEM-STRUC": {
                "^$VAR1": {"ORDINALITY": 3, "MEMBER-OF": {"VALUE": "REFSEM1"}},
                "REFSEM1": ["SET"],
            },
            "EXAMPLE-BINDINGS": [
                "THE",
                "MAN",
                "TURNED",
                "AT",
                "THE",
                "SECOND-0",
                "STREET-1",
            ],
        }
    },
    "TURN": {
        "TURN-V601": {
            "CAT": "V",
            "DEF": "phrasal: \u2018turn right\u2019; imperative verb and adverb \u2018right\u2019; I assume that PPs and adverbs can be compositionally added to this structure",
            "EX": "TURN RIGHT. TURN RIGHT AT THE CORNER. TURN RIGHT AFTER THE RESTAURANT.\n    TURN RIGHT IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "ADV": {"ROOT": "$VAR1", "ROOT-WORD": "RIGHT", "CAT": "ADV"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-RIGHT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR1": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["TURN-0", "RIGHT-1", "AT", "THE", "LIGHT"],
            "SYNONYMS": ["GO"],
        },
        "TURN-V602": {
            "CAT": "V",
            "DEF": "phrasal: \u2018turn left\u2019",
            "EX": "TURN LEFT. TURN LEFT AT THE CORNER. TURN LEFT AFTER THE RESTAURANT.\n    TURN LEFT IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "V": {"ROOT": "$VAR1", "ROOT-WORD": ["LEFT", "LEAVE"], "CAT": "V"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-LEFT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR1": {"NULL-SEM": "+"},
            },
            "SYNONYMS": ["GO"],
            "EXAMPLE-BINDINGS": ["TURN-0", "LEFT-1", "AT", "THE", "LIGHT"],
        },
        "TURN-V603": {
            "CAT": "V",
            "DEF": "phrasal: \u2018turn slight right\u2019",
            "EX": "TURN SLIGHT RIGHT. TURN SLIGHT RIGHT AT THE CORNER. TURN SLIGHT RIGHT\n    AFTER THE RESTAURANT. TURN SLIGHT RIGHT IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "TENSE": ["INFINITIVE", "PROGRESSIVE"],
                "ADJ": {"ROOT": "$VAR2", "ROOT-WORD": "SLIGHT", "CAT": "ADJ"},
                "N": {"ROOT": "$VAR1", "ROOT-WORD": "RIGHT", "CAT": "N"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-SLIGHT-RIGHT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR1": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["TURN-0", "SLIGHT-2", "RIGHT-1", "AT", "THE", "LIGHT"],
            "SYNONYMS": ["GO"],
        },
        "TURN-V604": {
            "CAT": "V",
            "DEF": "phrasal: \u2018turn slight left\u2019",
            "EX": "TURN SLIGHT LEFT. TURN SLIGHT LEFT AT THE CORNER. TURN SLIGHT LEFT\n    AFTER THE RESTAURANT. TURN SLIGHT LEFT IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "V",
                "TENSE": ["INFINITIVE", "PROGRESSIVE"],
                "ADJ": {"ROOT": "$VAR2", "ROOT-WORD": "SLIGHT", "CAT": "ADJ"},
                "N": {
                    "ROOT": "$VAR1",
                    "ROOT-WORD": ["LEAVE", "LEFT"],
                    "CAT": ["N", "ADV", "V"],
                },
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-SLIGHT-LEFT": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR1": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": ["TURN-0", "SLIGHT-2", "LEFT-1", "AT", "THE", "LIGHT"],
            "SYNONYMS": ["GO"],
        },
        "TURN-V605": {
            "CAT": "V",
            "DEF": "phrasal: \u2018turn \u2019; imperative verb; I assume that PPs and adverbs can be compositionally added to this structure",
            "EX": "TURN. TURN AT THE CORNER. TURN AFTER THE RESTAURANT.\n    TURN RIGHT IMMEDIATELY.",
            "COMMENTS": "",
            "SYN-STRUC": {"ROOT": "$VAR0", "CAT": "V"},
            "SEM-STRUC": {
                "TURN-VEHICLE": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
            },
            "SYNONYMS": ["GO"],
        },
    },
    "U-TURN": {
        "U-TURN-N601": {
            "CAT": "N",
            "DEF": "phrasal: \u2018u-turn + PP\u2019 meaning \u2018turn left\u2019 at the place indicated by PP",
            "EX": "U-TURN AT THE INTERSECTION.",
            "COMMENTS": "Note the checking condition \u2013 there cannot be a verb in this structure, otherwise it can mean \u2018exactly + PP\u2019 (e.g., Turn right right at the intersection\u2019)",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "ROOT": "$VAR0",
                "CAT": "N",
                "PREP": {
                    "ROOT": "$VAR1",
                    "ROOT-WORD": [
                        "AT",
                        "NEAR",
                        "BY",
                        "BESIDE",
                        "NEXT_TO",
                        "IN_FRONT_OF",
                        "BEFORE",
                        "AFTER",
                    ],
                    "CAT": "PREP",
                },
                "ART": {"ROOT": "$VAR2", "ROOT-WORD": "THE", "CAT": "ART"},
                "N": {"ROOT": "$VAR3", "CAT": "N"},
            },
            "SEM-STRUC": {
                "TURN-VEHICLE-UTURN": {
                    "AGENT": "*INTERLOCUTOR*",
                    "THEME": "*VEHICLE-IN-QUESTION*",
                    "LOCATION": {"VALUE": "^$VAR3"},
                    "THEME-OF": {"VALUE": "REFSEM1"},
                },
                "REFSEM1": {
                    "REQUEST-ACTION": {
                        "AGENT-1": "*SPEAKER*",
                        "BENEFICIARY": "*INTERLOCUTOR*",
                    }
                },
                "^$VAR2": {"NULL-SEM": "+"},
            },
            "MEANING-PROCEDURES": [["SEEK-SPECIFICATION", "LOCATION", "AT", "^$VAR3"]],
            "EXAMPLE-BINDINGS": ["U-TURN-0", "AT-1", "THE-2", "CORNER-3"],
            "SYNONYMS": ["UIE", "YUUWEE"],
        }
    },
    "WANT": {
        "WANT-V510": {
            "CAT": "V",
            "DEF": "",
            "EX": "I want you to hit the building",
            "COMMENTS": "indirect speech act. ",
            "TMR-HEAD": "NIL",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "N": {"ROOT": "$VAR1", "CAT": "N"},
                "ROOT": "$VAR0",
                "CAT": "V",
                "N-1": {"ROOT": "$VAR3", "CAT": "N"},
                "INFO": [["ROOT", "$VAR4"], ["ROOT", "TO"], ["CAT", "INF"]],
                "V": {"ROOT": "$VAR5", "CAT": "V"},
            },
            "SEM-STRUC": {
                "REQUEST-ACTION": {
                    "FORMALITY": "NEUTRAL",
                    "AGENT": {"VALUE": "^$VAR1"},
                    "BENEFICIARY": {"VALUE": "^$VAR3"},
                    "THEME": {"VALUE": "^$VAR5"},
                },
                "^$VAR5": {"AGENT-1": {"VALUE": "^$VAR3"}},
                "^$VAR4": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": [
                "I-1",
                "WANT-0",
                "YOU-3",
                "TO-4",
                "HIT-5",
                "THE",
                "BUILDING",
            ],
            "MEANING-PROCEDURES": [["FIX-CASE-ROLE", "^$VAR5", "^$VAR3", "AGENT"]],
            "SYNONYMS": "NIL",
        }
    },
    "WONDER": {
        "WONDER-V511": {
            "CAT": "V",
            "DEF": "",
            "EX": "I wonder if X",
            "COMMENTS": "indirect speech act. ",
            "TMR-HEAD": "NIL",
            "SYN-STRUC": {
                "USE-EXAMPLE-BINDING": "T",
                "N": {"ROOT": "$VAR1", "CAT": "N"},
                "ROOT": "$VAR0",
                "CAT": "V",
                "PREP": {
                    "ROOT": "$VAR2",
                    "ROOT-WORD": ["IF", "WHETHER"],
                    "CAT": "PREP",
                },
                "N-1": {"ROOT": "$VAR5", "CAT": "N"},
                "AUX": {"ROOT": "$VAR3", "ROOT-WORD": ["COULD", "WOULD"], "CAT": "AUX"},
                "V": {"ROOT": "$VAR4", "CAT": "V"},
            },
            "SEM-STRUC": {
                "REQUEST-ACTION": {
                    "FORMALITY": "POLITE",
                    "AGENT": {"VALUE": "^$VAR1"},
                    "BENEFICIARY": {"VALUE": "^$VAR5"},
                    "THEME": {"VALUE": "^$VAR4"},
                },
                "^$VAR4": {"AGENT-1": {"VALUE": "^$VAR5"}},
                "^$VAR2": {"NULL-SEM": "+"},
                "^$VAR3": {"NULL-SEM": "+"},
            },
            "EXAMPLE-BINDINGS": [
                "I-1",
                "WONDER-0",
                "IF-2",
                "YOU-5",
                "COULD-3",
                "HIT-4",
                "THE",
                "BUILDING",
            ],
            "MEANING-PROCEDURES": [["FIX-CASE-ROLE", "^$VAR4", "^$VAR5", "AGENT"]],
        }
    },
    "YOU": {
        "YOU-N1": {
            "CAT": "N",
            "DEF": "the pronoun 'you', which can have sg., pl., or indefinite referent",
            "EX": "you're too lazy (specific); when you're lazy, you can't expect to achieve much generalized or specific, depending on context.",
            "COMMENTS": "'you' most often refers to humans, domestic pets and god(s). however, it  can actually refer to anything anyone cares to talk to - a car that won't start,  a frying pan that burns you as if in spite, plants that you want to encourage  to grow. the question: how much do we want to get into this? shall we assume that  our texts will have few domestic pets, gods and unwieldy objects and forget about  them or do we want to really get this 'right'? (btw, we have 'pet-food' but we   don't have pet, so there's no quick way to have a sem-struc for pet). also, we have   the same situation with 'generalized 'you'' as we have with 'generalized 'they''. we   need to search for a really good antecedent. if we don't find one, we use the   generalized meaning. we need corpus work for this. I don't have a good feel for what   the heuristics will be - I'm setting most to .5 till we do some corpus work.  The hyponyms can't have sg. or indef. reference - should be split apart later.  ",
            "TMR-HEAD": "NIL",
            "SYN-STRUC": {"ROOT": "$VAR0", "CAT": "N", "TYPE": "PRO"},
            "SEM-STRUC": "HUMAN",
            "OUTPUT-SYNTAX": "NIL",
            "MEANING-PROCEDURES": [["TRIGGER-REFERENCE"]],
            "EXAMPLE-BINDINGS": "NIL",
            "EXAMPLE-DEPS": "NIL",
            "SYNONYMS": "NIL",
            "HYPONYMS": ["YOU_GUYS", "|y'all|"],
        }
    },
}
