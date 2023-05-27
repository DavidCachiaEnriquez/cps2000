from Parser import NTerminalNode

# SYMBOL TABLE CLASS
class symbolTable:
    def __init__(self):
        self.variables = []
        self.functions = []


# SEMANTIC ANALYSER CLASS
class semanticAnalysis:
    def __init__(self, tree):
        self.symbols = symbolTable()
        self.tree = tree

        print("\nS E M A N T I C   A N A L Y S I S")
        self.traverse(self.tree)
        print("Code passed Semantic Analysis")

    # TRAVERSING THE AST
    def traverse(self, tree):
        if tree.name == "ASSIGNMENT":
            vName = tree.children[0].value
            
            flag = False
            for scope in self.symbols.variables:
                if vName in scope:
                    flag = True
                    break

            if flag == False:
                raise Exception ("Error: variable '" + vName + "' not defined")

            vValue = tree.children[2]
            vType = self.getVarType(vValue)

            reqType = ""
            for scope in self.symbols.variables:
                if vName in scope:
                    reqType = scope[vName]

            if vType != reqType and vType != None:
                raise Exception ("Error: variable '" + vName + "' does not accept type '" + vType + "'")   

        if tree.name == "VARIABLEDECL":
            vName = tree.children[0].value
            vType = tree.children[1].value

            for scope in self.symbols.variables:
                if vName in scope:
                    raise Exception ("Error: variable '" + vName + "' already declared")
                
            vValue = tree.children[3]
            vValueType = self.getVarType(vValue)

            if vType != vValueType:
                raise Exception ("Error: variable '" + vName + "' does not accept type '" + str(vValueType) + "'")
                
            self.symbols.variables[-1][vName] = vType

        if tree.name == "PIXELSTATEMENT":        
            if tree.children[0].name == "__PIXEL":
                a = self.getVarType(tree.children[1])
                b = self.getVarType(tree.children[2])
                c = self.getVarType(tree.children[3])

                if a == "int" and b == "int" and (c == "colour" or c == "int"):
                    pass
                else:
                    raise Exception ("Error: invalid format for __PIXEL (int, int, colour)")
            else:
                a = self.getVarType(tree.children[1])
                b = self.getVarType(tree.children[2])
                c = self.getVarType(tree.children[3])
                d = self.getVarType(tree.children[4])
                e = self.getVarType(tree.children[5])

                if a == "int" and b == "int" and c == "int" and d == "int" and (e == "colour" or e == "int"):
                    pass
                else:
                    raise Exception ("Error: invalid format for __PIXELR (int, int, int, int, colour)")
            
        if tree.name == "IFSTATEMENT":
            self.symbols.variables.append({}); self.symbols.functions.append({})
            for i in tree.children:
                self.traverse(i)   
            self.symbols.variables.pop(-1); self.symbols.functions.pop(-1)    

        if tree.name == "FORSTATEMENT":
            self.symbols.variables.append({}); self.symbols.functions.append({})
            for i in tree.children:
                self.traverse(i)   
 
            self.symbols.variables.pop(-1); self.symbols.functions.pop(-1)    

        if tree.name == "WHILESTATEMENT":
            self.symbols.variables.append({}); self.symbols.functions.append({})
            for i in tree.children:
                self.traverse(i)
            self.symbols.variables.pop(-1); self.symbols.functions.pop(-1)

        if tree.name == "FUNCTIONDECL":
            funName = tree.children[0].value
            funType = ""
            
            # No Parameters
            if tree.children[1].name == "ARROW":
                funType = tree.children[2].value
                for scope in self.symbols.functions:
                    if funName in scope:
                        raise Exception ("Error: function '" + funName + "' already declared")                
                self.symbols.functions[-1][funName] = [funType, None]

                self.symbols.variables.append({}); self.symbols.functions.append({})
                self.traverse(tree.children[3])

                listOfReturns = self.getReturns(tree)

                temp = []
                for x in listOfReturns:
                    temp.append(self.getVarType(x.children[0]))
                    
                flag = True
                for x in temp:
                    if x != funType:
                        flag = False

                if flag == False:
                    raise Exception ("Error: Return values dont match function type")
                
                self.symbols.variables.pop(-1); self.symbols.functions.pop(-1)
                
            # Yes Parameters
            else:
                funType = tree.children[3].value

                for scope in self.symbols.functions:
                    if funName in scope:
                        raise Exception ("Error: function '" + funName + "' already declared")

                list = []

                for param in tree.children[1].children:
                    pName = param.children[0].value

                    for scope in self.symbols.variables:
                        if pName in scope:
                            raise Exception ("Error: variable '" + pName + "' already declared")
                    
                    pType = param.children[1].value
                    list.append((pName, pType))

                parameterTypes = []
                for i in list:
                    parameterTypes.append(i[1])

                self.symbols.functions[-1][funName] = [funType, parameterTypes]

                self.symbols.variables.append({}); self.symbols.functions.append({})
                
                for pair in list:
                    self.symbols.variables[-1][pair[0]] = pair[1]

                self.traverse(tree.children[4])

                listOfReturns = self.getReturns(tree)

                temp = []
                for x in listOfReturns:
                    temp.append(self.getVarType(x.children[0]))

                flag = True
                for x in temp:
                    if x != funType:
                        flag = False

                if flag == False:
                    raise Exception ("Error: Return values dont match function type")
                
                self.symbols.variables.pop(-1); self.symbols.functions.pop(-1)

        if tree.name == "STATEMENT":
            self.traverse(tree.children[0])

        if tree.name == "BLOCK":
            for child in tree.children:
                self.traverse(child)

        if tree.name == "PROGRAM":
            self.symbols.variables.append({}); self.symbols.functions.append({})
            for child in tree.children:
                self.traverse(child)
            self.symbols.variables.pop(-1); self.symbols.functions.pop(-1)
    
    # GETTING VALUE TYPE OF EXPRESSION
    def getVarType(self, tree):       
        if isinstance(tree, NTerminalNode):
            if tree.name == "FUNCTIONCALL":
                funName = tree.children[0].value
                reqParams = ""
                for scope in self.symbols.functions:
                    if funName in scope:
                        reqParams = scope[funName][1]

                if reqParams == "":
                    raise Exception ("Error: function '"+ funName + "' isnt declared")
                
                if reqParams == None:
                    if len(tree.children) != 1:
                        raise Exception ("Error: function '" + funName + "' doesnt take paramters")

                else:
                    if not tree.children[1] or len(tree.children[1].children) != len(reqParams):
                        raise Exception ("Error: more values than expected")

                    tempList = []
                    for i in tree.children[1].children:
                        tempList.append(self.getVarType(i))

                    for counter in range(len(tempList)):
                        if tempList[counter] != reqParams[counter]:
                            raise Exception ("Error: invalid paramters passed")
                        
                for scope in self.symbols.functions:
                    if funName in scope:
                        return scope[funName][0]

            else:                  
                types = []
                if tree.name == "EXPR":
                    for i in tree.children:
                        if i.name == "RELATIONALOP":
                            return "bool"
                        
                if tree.name == "TERM":
                    for i in tree.children:
                        if i.name == "MULTIPLICATIVEOP" and i.value == "/":
                            return "float"
                
                for child in tree.children:
                    varType = self.getVarType(child)

                    if varType != None:
                        types.append(varType)

                if len(types) == 1:
                    return types[0]
                else:
                    return self.checkTypes(types)

        else:
            if tree.name == "INTEGERLITERAL" or tree.name == "PADWIDTH" or tree.name == "PADHEIGHT":
                return ("int")
            
            elif tree.name == "FLOATLITERAL":
                return ("float")
            
            elif tree.name == "BOOLEANLITERAL":
                return ("bool")
            
            elif tree.name == "COLOURLITERAL":
                return ("colour")
            
            elif tree.name == "IDENTIFIER":
                name = tree.value
                reqType = ""

                for scope in self.symbols.variables:
                    if name in scope:
                        reqType = scope[name]

                if reqType == "":
                    raise Exception ("Error: variable '" + name + "' does not exist")

                return reqType

    def checkTypes(self, list):
        if len(list) == 0:
            return None

        elif len(list) == 1:           
            return list[0]

        elif len(list) > 2:
            while len(list) > 2:
                tempList = [list.pop(0), list.pop(0)]
                newVal = self.checkTypes(tempList)
                list.append(newVal)
            
        else:
            if list[0] == "int" and list[1] == "int":
                return "int"
            elif list[0] == "float" and list[1] == "int" or list[0] == "int" and list[1] == "float" or list[0] == "float" and list[1] == "float":
                return "float"
            elif list[0] == "colour" and list[1] == "colour":
                return "colour"
            elif list[0] == "bool" and list[1] == "bool":
                return "bool"
            else:
                raise Exception ("Error in type matching")
            
    # GETGET EACH RETURN TYPE IN A FUNCTION DECLERATION
    def getReturns(self, tree):
        num = []
        if tree.name == "RTRNSTATEMENT":
            num.append(tree)
            return num
        
        elif isinstance(tree, NTerminalNode):
            for child in tree.children:
                temp = self.getReturns(child)
                
                for i in temp:
                    num.append(i)

        return num

