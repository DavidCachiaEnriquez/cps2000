# TERMINAL NODE CLASS
class TerminalNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value


# NON-TERMINAL NODE CLASS
class NTerminalNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        

# PARSER CLASS
class Parser:
    def __init__(self, tokens):

        self.tokenList = tokens
        self.tree = None

        print("\nP A R S E R")
        self.parseCode()
        print("Code Accepted by Parser")       


    # PARSE GIVEN CODE
    def parseCode(self):
        self.program()
        
    # GET NEXT TOKEN FROM LEXER
    def getNextToken(self):
        self.tokenList.pop(0)

    # FOR EACH RULE
    def padRead(self, tree):
        # creates a new PADREAD node
        nTree = NTerminalNode("PADREAD")
        nTree.children.append(TerminalNode("__READ", self.tokenList[0][1])); self.getNextToken()
        self.expr(nTree)

        # checks if the next token is a comma
        if self.tokenList[0][0] == ",":
            self.getNextToken()
            self.expr(nTree)
            tree.children.append(nTree)            
        else:
            raise Exception ("Error: missing ','")

    def padRandI(self, tree):
        nTree = NTerminalNode("PADRANDI")
        nTree.children.append(TerminalNode("__RANDI", self.tokenList[0][1])); self.getNextToken()
        self.expr(nTree)
        tree.children.append(nTree)

    def literal(self, tree):
        nTree = NTerminalNode("LITERAL")
        nTree.children.append(TerminalNode(self.tokenList[0][0], self.tokenList[0][1])); self.getNextToken()
        tree.children.append(nTree)

    def actualParams(self, tree):
        nTree = NTerminalNode("ACTUALPARAMS")
        self.expr(nTree)

        # loops till it reaches the end of the COMMAN, EXPR pairs
        while self.tokenList and self.tokenList[0][0] == ",":
            self.getNextToken()
            self.expr(nTree)
        
        tree.children.append(nTree)

    def functionCall(self, tree):
        nTree = NTerminalNode("FUNCTIONCALL")
        nTree.children.append(TerminalNode("IDENTIFIER", self.tokenList[0][1])); self.getNextToken()
        self.getNextToken()
    
        # if there are parameters
        if self.tokenList[0][0] != ")":
            self.actualParams(nTree)

            if self.tokenList[0][0] == ")":
                self.getNextToken()
                tree.children.append(nTree)
            else:
                raise Exception ("Error: missing ')'")
                
        # if there are no parameters
        elif self.tokenList[0][0] == ")":
            self.getNextToken()
            tree.children.append(nTree)     

    def subExpr(self, tree):
        nTree = NTerminalNode("SUBEXPR")
        self.getNextToken()
        self.expr(nTree)

        if self.tokenList[0][0] == ")":
            self.getNextToken()
            tree.children.append(nTree)
        else:
            raise Exception ("Error: missing ')'")

    def unary(self, tree):
        nTree = NTerminalNode("UNARY")
        nTree.children.append(TerminalNode(self.tokenList[0][0], self.tokenList[0][1])); self.getNextToken()
        self.expr(nTree)
        tree.children.append(nTree)

    def factor(self, tree):
        nTree = NTerminalNode("FACTOR")

        # LITERAL
        if self.tokenList[0][0] in ["BOOLEANLITERAL", "INTEGERLITERAL", "FLOATLITERAL", "COLOURLITERAL"]:
            self.literal(nTree)

        # IDENTIFIER & FUNCTIONCALL
        elif self.tokenList[0][0] == "IDENTIFIER":   
            if len(self.tokenList) > 1:
                if self.tokenList[1][0] == "(":
                    self.functionCall(nTree)
                else:
                    nTree.children.append(TerminalNode("IDENTIFIER", self.tokenList[0][1])); self.getNextToken()
            else:
                nTree.children.append(TerminalNode("IDENTIFIER", self.tokenList[0][1])); self.getNextToken()

        # SUBEXPR
        elif self.tokenList[0][0] == "(":
            self.subExpr(nTree)

        # UNARY
        elif self.tokenList[0][0] == "-" or self.tokenList[0][0] == "NOT":
            self.unary(nTree)

        # PADRANDI
        elif self.tokenList[0][0] == "__RANDI":
            self.padRandI(nTree)

        # PADWIDTH
        elif self.tokenList[0][0] == "PADWIDTH":
            nTree.children.append(TerminalNode("PADWIDTH", self.tokenList[0][1])); self.getNextToken()

        # PADHEIGHT
        elif self.tokenList[0][0] == "PADHEIGHT":
            nTree.children.append(TerminalNode("PADHEIGHT", self.tokenList[0][1])); self.getNextToken()

        #PADREAD
        elif self.tokenList[0][0] == "__READ":
            self.padRead(nTree)

        else:
            raise Exception ("Error: factor not recognised")
        
        tree.children.append(nTree)
    
    def term(self, tree):
        nTree = NTerminalNode("TERM")
        self.factor(nTree)
        
        if len(self.tokenList) > 0:
            while  self.tokenList[0][0] == "MULTIPLICATIVEOP":
                nTree.children.append(TerminalNode("MULTIPLICATIVEOP", self.tokenList[0][1])); self.getNextToken()
                self.factor(nTree)
        
        tree.children.append(nTree)
        
    def simpleExpr(self, tree):
        nTree = NTerminalNode("SIMPLEEXPR")
        self.term(nTree)
        
        if len(self.tokenList) > 0:
            while self.tokenList[0][0] == "ADDITIVEOP" or self.tokenList[0][1] == "-":
                nTree.children.append(TerminalNode("ADDITIVEOP", self.tokenList[0][1])); self.getNextToken()
                self.term(nTree)
        
        tree.children.append(nTree)

    def expr(self, tree):
        nTree = NTerminalNode("EXPR")
        self.simpleExpr(nTree)
        
        if len(self.tokenList) > 0:
            while self.tokenList[0][0] == "RELATIONALOP":
                nTree.children.append(TerminalNode("RELATIONALOP", self.tokenList[0][1])); self.getNextToken()
                self.simpleExpr(nTree)

        tree.children.append(nTree)

    def assignment(self, tree):
        nTree = NTerminalNode("ASSIGNMENT")

        if self.tokenList[0][0] == "IDENTIFIER":
            nTree.children.append(TerminalNode("IDENTIFIER", self.tokenList[0][1])); self.getNextToken()

            if self.tokenList[0][0] == "=":
                nTree.children.append(TerminalNode("EQUALS", self.tokenList[0][1])); self.getNextToken()

                self.expr(nTree)
                tree.children.append(nTree)
            
            else:
                raise Exception ("Error: missing '='")
        else:
            raise Exception ("Error: missing IDENTIFIER")

    def variableDecl(self, tree):
        nTree = NTerminalNode("VARIABLEDECL")

        if self.tokenList[0][0] == "LET":
            self.getNextToken()
            
            if self.tokenList[0][0] == "IDENTIFIER":
                nTree.children.append(TerminalNode("IDENTIFIER", self.tokenList[0][1])); self.getNextToken()
                
                if self.tokenList[0][0] == ":":
                    self.getNextToken()

                    if self.tokenList[0][0] == "TYPE":
                        nTree.children.append(TerminalNode("TYPE", self.tokenList[0][1])); self.getNextToken()

                        if self.tokenList[0][0] == "=":
                            nTree.children.append(TerminalNode("EQUALS", self.tokenList[0][1])); self.getNextToken()
                            self.expr(nTree)
                            tree.children.append(nTree)

                        else:
                            raise Exception ("Error: missing '='")
                    else:
                        raise Exception ("Error: missing TYPE")
                else:
                    raise Exception ("Error: missing ':'")
            else:
                raise Exception ("Error: missing 'IDENTIFIER'")
        else:
            raise Exception ("Error: missing LET keyword")

    def printStatement(self, tree):
        nTree = NTerminalNode("PRINTSTATEMENT")

        if self.tokenList[0][0] == "__PRINT":
            self.getNextToken()            
            self.expr(nTree)
            tree.children.append(nTree)
        
        else:
            raise Exception ("Error in Parser")

    def delayStatement(self, tree):
        nTree = NTerminalNode("DELAYSTATEMENT")

        if self.tokenList[0][0] == "__DELAY":
            self.getNextToken()            
            self.expr(nTree)
            tree.children.append(nTree)

        else:
            raise Exception ("Error in Parser")

    def pixelStatement(self, tree):
        nTree = NTerminalNode("PIXELSTATEMENT")

        if self.tokenList[0][0] == "__PIXELR":
            nTree.children.append(TerminalNode("__PIXELR", self.tokenList[0][1])); self.getNextToken()
            self.expr(nTree)

            if self.tokenList[0][0] == ",":
                self.getNextToken()
                self.expr(nTree)

                if self.tokenList[0][0] == ",":
                    self.getNextToken()
                    self.expr(nTree)

                    if self.tokenList[0][0] == ",":
                        self.getNextToken()
                        self.expr(nTree)

                        if self.tokenList[0][0] == ",":
                            self.getNextToken()
                            self.expr(nTree)

                            tree.children.append(nTree)
                        
                        else:
                            raise Exception ("Error in Parser")
                    else:
                        raise Exception ("Error in Parser")
                else:
                    raise Exception ("Error in Parser")
            else:
                raise Exception ("Error in Parser")
        
        elif self.tokenList[0][0] == "__PIXEL":
            nTree.children.append(TerminalNode("__PIXEL", self.tokenList[0][1])); self.getNextToken()
            self.expr(nTree)

            if self.tokenList[0][0] == ",":
                self.getNextToken()
                self.expr(nTree)

                if self.tokenList[0][0] == ",":
                    self.getNextToken()
                    self.expr(nTree)

                    tree.children.append(nTree)
                
                else:
                    raise Exception ("Error in Parser")
            else:
                raise Exception ("Error in Parser")
        else:
            raise Exception ("Error in Parser")

    def rtrnStatement(self, tree):
        nTree = NTerminalNode("RTRNSTATEMENT")

        if self.tokenList[0][0] == "RETURN":
            self.getNextToken()
            self.expr(nTree)
            tree.children.append(nTree)

    def ifStatement(self, tree):
        nTree = NTerminalNode("IFSTATEMENT")

        if self.tokenList[0][0] == "IF":
            self.getNextToken()

            if self.tokenList[0][0] == "(":
                self.getNextToken()
                self.expr(nTree)
                
                if self.tokenList[0][0] == ")":
                    self.getNextToken()
                    self.block(nTree)
                    
                    if self.tokenList and self.tokenList[0][0] == "ELSE":
                        self.getNextToken()
                        self.block(nTree)
                        tree.children.append(nTree)

                    else:
                        tree.children.append(nTree)
                
                else:
                    raise Exception ("Error: missing ')'")
            else:
                raise Exception ("Error: missing '('")
        else:
            raise Exception ("Error: missing IF keyword")                

    def forStatement(self, tree):
        nTree = NTerminalNode("FORSTATEMENT")

        if self.tokenList[0][0] == "FOR":
            self.getNextToken()

            if self.tokenList[0][0] == "(":
                self.getNextToken()

                if self.tokenList[0][0] == "LET":
                    self.variableDecl(nTree)

                    if self.tokenList[0][0] == ";":
                        self.getNextToken()
                        self.expr(nTree)
                        self.getNextToken()

                        if self.tokenList[0][0] == "IDENTIFIER":
                            self.assignment(nTree)
                            
                            if self.tokenList[0][0] == ")":
                                self.getNextToken()
                                self.block(nTree)
                                tree.children.append(nTree)
                            
                            else:
                                raise Exception ("Error: missing ')'")
                            
                        elif self.tokenList[0][0] == ")":
                            self.getNextToken()
                            self.block(nTree)
                            tree.children.append(nTree)
                        
                        else:
                            raise Exception ("Error: missing ')'")
                    else:
                        raise Exception ("Error: missing ';'")
                        
                elif self.tokenList[0][0] == ";":
                    self.getNextToken()
                    self.expr(nTree)
                    self.getNextToken()

                    if self.tokenList[0][0] == "IDENTIFIER":
                        self.assignment(nTree)
                        
                        if self.tokenList[0][0] == ")":
                            self.getNextToken()
                            self.block(nTree)
                            tree.children.append(nTree)
                        
                        else:
                            raise Exception ("Error: missing ')")
                        
                    elif self.tokenList[0][0] == ")":
                        self.getNextToken()
                        self.block(nTree)
                        tree.children.append(nTree)
                    
                    else:
                        raise Exception ("Error: missing ')'")
                else:
                    raise Exception ("Error: missing LET keyword")
            else:
                raise Exception ("Error: missing '('")
        else:
            raise Exception ("Error: missing FOR keyword")

    def whileStatement(self, tree):
        nTree = NTerminalNode("WHILESTATEMENT")
        self.getNextToken()

        if self.tokenList[0][0] == "(":
            self.getNextToken()
            self.expr(nTree)

            if self.tokenList[0][0] == ")":
                self.getNextToken()
                self.block(nTree)
                tree.children.append(nTree)
            
            else:
                raise Exception ("Error: missing ')'")
        
        else:
            raise Exception ("Error: missing '('")

    def formalParam(self, tree):
        nTree = NTerminalNode("FORMALPARAM")

        if self.tokenList[0][0] == "IDENTIFIER":
            nTree.children.append(TerminalNode("IDENTIFIER", self.tokenList[0][1])); self.getNextToken()

            if self.tokenList[0][0] == ":":
                self.getNextToken()

                if self.tokenList[0][0] == "TYPE":
                    nTree.children.append(TerminalNode("TYPE", self.tokenList[0][1])); self.getNextToken()
                    
                    tree.children.append(nTree)
                
                else:
                    raise Exception ("Error: missing TYPE")
            
            else:
                raise Exception ("Error: missin ':")
        
        else:
            raise Exception ("Error: missing parameter")

    def formalParams(self, tree):
        nTree = NTerminalNode("FORMALPARAMS")

        self.formalParam(nTree)

        while self.tokenList and self.tokenList[0][0] == ",":
            self.getNextToken()
            self.formalParam(nTree)

        tree.children.append(nTree)

    def functionDecl(self,tree):
        nTree = NTerminalNode("FUNCTIONDECL")
        self.getNextToken()
        
        if self.tokenList[0][0] == "IDENTIFIER":
            nTree.children.append(TerminalNode("IDENTIFIER", self.tokenList[0][1])); self.getNextToken()

            if self.tokenList[0][0] == "(":
                self.getNextToken()

                # if the function has parameters
                if self.tokenList[0][0] == "IDENTIFIER":
                    self.formalParams(nTree)

                    if self.tokenList[0][0] == ")":
                        self.getNextToken()
                            
                        if self.tokenList[0][0] == "->":
                            nTree.children.append(TerminalNode("ARROW", self.tokenList[0][1])); self.getNextToken()

                            if self.tokenList[0][0] == "TYPE":
                                nTree.children.append(TerminalNode("TYPE", self.tokenList[0][1])); self.getNextToken()
                                self.block(nTree)
                                tree.children.append(nTree)
                            
                            else:
                                raise Exception ("Error: invalid type")
                            
                        else:
                            raise Exception ("Error: missing arrow")
                        
                    else:
                        raise Exception ("Error: missing ')'")      
                
                # if the function doesnt have parameters
                elif self.tokenList[0][0] == ")":
                    self.getNextToken()
                        
                    if self.tokenList[0][0] == "->":
                        nTree.children.append(TerminalNode("ARROW", self.tokenList[0][1])); self.getNextToken()

                        if self.tokenList[0][0] == "TYPE":
                            nTree.children.append(TerminalNode("TYPE", self.tokenList[0][1])); self.getNextToken()
                            self.block(nTree)
                            tree.children.append(nTree)
                        
                        else:
                            raise Exception ("Error: missing type")
                        
                    else:
                        raise Exception ("Error: missing ARROW")
                
                else:
                    raise Exception ("Error: missing PARAMETERS")
            
            else:
                raise Exception ("Error: missing '('")
            
        else:
            raise Exception ("Error: invalid function name")
                            
    def statement(self, tree): 
        nTree = NTerminalNode("STATEMENT")

        # VARIABLEDECL
        if self.tokenList[0][0] == "LET":
            self.variableDecl(nTree)

            if len(self.tokenList) > 0:
                if self.tokenList[0][0] == ";":
                    self.getNextToken()
                else:
                    raise Exception ("Error: missing semi-colon")
            else:
                raise Exception ("Error: missing semi-colon")

        # ASSIGNMENT
        elif self.tokenList[0][0] == "IDENTIFIER":
            self.assignment(nTree)
            
            if len(self.tokenList) > 0:
                if self.tokenList[0][0] == ";":
                    self.getNextToken()
                else:
                    raise Exception ("Error: missing semi-colon")
            else:
                raise Exception ("Error: missing semi-colon")

        # PRINTSTATEMENT
        elif self.tokenList[0][0] == "__PRINT":
            self.printStatement(nTree)

            if len(self.tokenList) > 0:
                if self.tokenList[0][0] == ";":
                    self.getNextToken()
                else:
                    raise Exception ("Error: missing semi-colon")
            else:
                raise Exception ("Error: missing semi-colon")

        # DELAYSTATEMENT
        elif self.tokenList[0][0] == "__DELAY":
            self.delayStatement(nTree)

            if len(self.tokenList) > 0:
                if self.tokenList[0][0] == ";":
                    self.getNextToken()
                else:
                    raise Exception ("Error: missing semi-colon")
            else:
                raise Exception ("Error: missing semi-colon")

        # PIXELSTATEMENT
        elif self.tokenList[0][0] in ["__PIXEL", "__PIXELR"]:
            self.pixelStatement(nTree)

            if len(self.tokenList) > 0:
                if self.tokenList[0][0] == ";":
                    self.getNextToken()
                else:
                    raise Exception ("Error: missing semi-colon")
            else:
                raise Exception ("Error: missing semi-colon")

        # IFSTATEMENT
        elif self.tokenList[0][0] == "IF":
            self.ifStatement(nTree)

        # FORSTATEMENT
        elif self.tokenList[0][0] == "FOR":
            self.forStatement(nTree)

        # WHILESTATEMENT
        elif self.tokenList[0][0] == "WHILE":
            self.whileStatement(nTree)

        # RETURN
        elif self.tokenList[0][0] == "RETURN":
            self.rtrnStatement(nTree)
            
            if len(self.tokenList) > 0:
                if self.tokenList[0][0] == ";":
                    self.getNextToken()
                else:
                    raise Exception ("Error: missing semi-colon")
            else:
                raise Exception ("Error: missing semi-colon")

        # FUNCTIONDECL
        elif self.tokenList[0][0] == "FUN":
            self.functionDecl(nTree)

        # BLOCK
        elif self.tokenList[0][0] == "{":
            self.block(nTree)
            
        else:
            raise Exception ("Error: invalid STATEMENT")
        
        tree.children.append(nTree)

    def block(self, tree):
        nTree = NTerminalNode("BLOCK")
        self.getNextToken()
        
        # if block isnt empty
        if self.tokenList[0][0] != "}":
            
            # loops while there are still statements in the block
            while self.tokenList[0][0] != "}":
                (self.statement(nTree))

            self.getNextToken()

        # if block is empty
        elif self.tokenList[0][0] == "}":
            self.getNextToken()

        tree.children.append(nTree)

    def program(self):
        tree = NTerminalNode("PROGRAM")
        
        # loops for each statement in the program
        while self.tokenList:
            (self.statement(tree))

        self.tree = tree

