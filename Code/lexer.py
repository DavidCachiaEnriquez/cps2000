import re

# TOKEN CLASS
class Token:
    def __init__(self, inputValue, inputType):
        self.value = inputValue
        self.type = inputType


# LEXER CLASS
class Lexer:
    def __init__(self, input):
        self.code = input
        self.tokenList = []
        self.pos = 0
        self.tokenTable = [
            (r"not|let|return|if|else|for|while|fun|->", "KEYWORDS"),

            (r"\b(float|int|bool|colour)\b", "TYPE"),
            
            (r"\b(true|false)\b", "BOOLEANLITERAL"),
            (r"\d+\.\d+", "FLOATLITERAL"),
            (r"\d+", "INTEGERLITERAL"),
            (r"\#[0-9a-fA-F]{6}", "COLOURLITERAL"),

            (r"\b(__width)\b", "PADWIDTH"),
            (r"\b(__height)\b", "PADHEIGHT"),

            (r"\b(__read)\b", "__READ"),
            (r"\b(__randi)\b", "__RANDI"),

            (r"[\*/]|and|AND", "MULTIPLICATIVEOP"),
            (r"[\+]|or|OR", "ADDITIVEOP"),
            (r"==|!=|<=|>=|[\<\>]", "RELATIONALOP"),

            (r"[a-zA-Z]([a-zA-Z0-9]|_)*", "IDENTIFIER"),

            (r"\b(__print)\b", "__PRINT"),
            (r"\b(__delay)\b", "__DELAY"),
            (r"\b(__pixelr)\b", "__PIXELR"),
            (r"\b(__pixel)\b", "__PIXEL"),

            (r"[\,\(\)\-\=\:\;\{\}]", "OTHER"),
        ]
        
        print("L E X E R")
        self.scanText()
        # print("\nToken List:")
        # # print(self.tokenList)
        print("Code accepted by Lexer")

    # SCAN GIVEN CODE
    def scanText(self):
        # loops while less than size of string
        while self.pos < len(self.code):
            # ignores whitespace
            if self.code[self.pos] == " " or self.code[self.pos] == "\n":
                self.pos += 1
                
            # if not whitespace
            else:
                value, type = None, None

                # goes through table of patterns
                for pattern, tokenType in self.tokenTable:
                    match = re.match(pattern, self.code[self.pos:])

                    # if they match
                    if match is not None:
                        type = tokenType
                        value = match.group()
                        break
                
                # if value and type remained empyty
                if value == None or type == None:
                    raise Exception("Error in Syntax")
                # if both value and type have been assigned
                else:
                    if type == "KEYWORDS" or type == "OTHER":
                        self.tokenList.append((value.upper(), value))
                        # self.tokenList.append(Token(value, "<"+value+">"))
                    else:
                        self.tokenList.append((type, value))
                        # self.tokenList.append(Token(value, type))
                    self.pos += len(value)

