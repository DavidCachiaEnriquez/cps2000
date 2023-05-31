from Semantic_Analysis import symbolTable

# CODE GENERATOR CLASS
class codeGeneration:
    def __init__(self, tree):
        self.tree = tree
        self.functionsList = []
        self.symbols = symbolTable()

        self.P = []
        
        print("\nC O D E   G E N E R A T I O N")
        self.traverse(self.tree, None)

        for function in self.functionsList:
            for line in function:
                self.P.append(line)

        self.printCode()
        print("PixIr code generated")

    # CREATE CODE
    def traverse(self, tree, list):    
        if tree.name == "ASSIGNMENT":
            varName = tree.children[0].value
            varValue = tree.children[2]
            
            if list == None:
                value = self.getVarValue(varValue)
                self.symbols.variables[-1][varName][0] = value

                self.addPush(self.symbols.variables[-1][varName][1][0])
                self.addPush(self.symbols.variables[-1][varName][1][1])
                self.P.append("st")
            
            else:
                value = self.getVarValueNP(varValue)

                if type(value) != type(list):
                    value = [value]
                value = self.flatten(value)

                for i in value:
                    list.append(i)

                loc = ()
                for i in self.symbols.variables:
                    if varName in i:
                        loc = i[varName][1]
                        break

                list.append("push " + str(loc[0]))
                list.append("push " + str(loc[1]))
                list.append("st")

        if tree.name == "VARIABLEDECL":
            if list == None:
                self.P.append("push 1")
                
                if len(self.symbols.variables[-1]) < 1:
                    self.P.append("oframe")
                else:
                    self.P.append("alloc")

                if "tempNameToRemoveDoNotNameAVariableThis" in self.symbols.variables[-1]:
                    self.symbols.variables[-1].pop("tempNameToRemoveDoNotNameAVariableThis")

                varName = tree.children[0].value
                varValue = tree.children[3]

                value = self.getVarValue(varValue)
                self.symbols.variables[-1][varName] = [value, ((len(self.symbols.variables[-1])), 0)]
                self.addPush(self.symbols.variables[-1][varName][1][0])
                self.addPush(self.symbols.variables[-1][varName][1][1])
                self.P.append("st")

            else:
                list.append("push 1")

                if len(self.symbols.variables[-1]) < 1:
                    list.append("oframe")
                else:
                    list.append("alloc")

                if "tempNameToRemoveDoNotNameAVariableThis" in self.symbols.variables[-1]:
                    self.symbols.variables[-1].pop("tempNameToRemoveDoNotNameAVariableThis")

                varName = tree.children[0].value
                varValue = tree.children[3]

                temp = self.getVarValueNP(varValue)

                if type(temp) != type(list):
                    temp = [temp]
                temp = self.flatten(temp)
                
                for i in temp:
                    list.append(i)
                
                self.symbols.variables[-1][varName] = [list[-1][5:], ((len(self.symbols.variables[-1])), 0)]
                list.append("push " + str(self.symbols.variables[-1][varName][1][0]))
                list.append("push " + str(self.symbols.variables[-1][varName][1][1]))
                list.append("st")

        if tree.name == "PRINTSTATEMENT":
            if list == None:
                self.getVarValue(tree.children[0])
                self.P.append("print")
            
            else:
                list.append(self.getVarValueNP(tree.children[0]))
                list.append("print")
                return list

        if tree.name == "DELAYSTATEMENT":
            if list == None:
                self.getVarValue(tree.children[0])
                self.P.append("delay")
            
            else:
                list.append(self.getVarValueNP(tree.children[0]))
                list.append("delay")

        if tree.name == "PIXELSTATEMENT":   
            if tree.children[0].name == "__PIXEL":
                
                if list == None:
                    self.getVarValue(tree.children[-1])
                
                    for i in tree.children[1:-1]:
                        self.getVarValue(i)
                    self.P.append("pixel")
                
                else:
                    list.append(self.getVarValueNP(tree.children[-1]))
                    
                    for i in tree.children[1:-1]:
                        list.append(self.getVarValueNP(i))
                    list.append("pixel")

            if tree.children[0].name == "__PIXELR":
                
                if list == None:
                    self.getVarValue(tree.children[-1])
                
                    for i in tree.children[1:-1]:
                        self.getVarValue(i)
                    self.P.append("pixelr")
               
                else:
                    list.append(self.getVarValueNP(tree.children[-1]))
                
                    for i in tree.children[1:-1]:
                        list.append(self.getVarValueNP(i))
                    list.append("pixelr")

        if tree.name == "RTRNSTATEMENT":
            temp = self.getVarValueNP(tree.children[0])
            
            if type(temp) != type(list):
                temp = [temp]
            temp = self.flatten(temp)
            
            for i in temp:
                list.append(i)
                
            list.append("ret")

        if tree.name == "IFSTATEMENT":
            tempList = []
            self.symbols.variables.append({}); self.symbols.functions.append({})

            for i in self.symbols.variables[:-1]:
                for j in i:
                    if j != "tempNameToRemoveDoNotNameAVariableThis":
                        i[j][1] = (i[j][1][0], i[j][1][1]+1)


            tempList.append("push #PC+")
            count1_1 = len(tempList)-1

            tempList.append(self.getVarValueNP(tree.children[0]))
            tempList = self.flatten(tempList)
            
            tempList.append("cjmp")

            if len(tree.children) == 3:
                self.traverse(tree.children[2], tempList)
                tempList = self.flatten(tempList)
            
            tempList.append("push #PC+")
            count2_1 = len(tempList)-1

            tempList.append("jmp")
            count1_2 = len(tempList)
            
            self.symbols.variables[-1]["tempNameToRemoveDoNotNameAVariableThis"] = [None, (None, None)]
            
            self.traverse(tree.children[1], tempList)
            if "tempNameToRemoveDoNotNameAVariableThis" in self.symbols.variables[-1]:
                    self.symbols.variables[-1].pop("tempNameToRemoveDoNotNameAVariableThis")
            tempList = self.flatten(tempList)
            

            count2_2 = len(tempList)

            values = [count1_2-count1_1, count2_2-count2_1]
            
            for i in range(len(tempList)):
                if tempList[i] == "push #PC+":
                    tempList[i] = tempList[i] + str(values[0])
                    values.pop(0)

            tempList = ["oframe"] + tempList

            if list == None:
                for i in tempList:
                    self.P.append(i)
            else:                                
                for i in tempList:
                    list.append(i)

            for i in self.symbols.variables[:-1]:
                for j in i:
                    if j != "tempNameToRemoveDoNotNameAVariableThis":
                        i[j][1] = (i[j][1][0], i[j][1][1]-1)

            self.symbols.variables.pop(-1); self.symbols.functions.pop(-1)

            if list == None:
                self.P.append("cframe")
            else:
                list.append("cframe")

        if tree.name == "FORSTATEMENT":            
            tempList = []
            self.symbols.variables.append({}); self.symbols.functions.append({})

            for i in self.symbols.variables[:-1]:
                for j in i:
                    if j != "tempNameToRemoveDoNotNameAVariableThis":
                        i[j][1] = (i[j][1][0], i[j][1][1]+1)

            if len(tree.children)-1 == 3:
                # VARDECL
                self.traverse(tree.children[0], tempList)
                tempList = self.flatten(tempList)

                tempList.append("push #PC+")
                count1_1 = len(tempList)-1
                count3_2 = len(tempList)-1


                # EXPR
                tempList.append(self.getVarValueNP(tree.children[1]))
                tempList = self.flatten(tempList)

                tempList.append("cjmp")

                tempList.append("push #PC+")
                count2_1 = len(tempList)-1
                tempList.append("jmp")
                count1_2 = len(tempList)


                # BLOCK
                self.symbols.variables[-1]["tempNameToRemoveDoNotNameAVariableThis"] = [None, (None, None)]
                self.traverse(tree.children[3], tempList)
                if "tempNameToRemoveDoNotNameAVariableThis" in self.symbols.variables[-1]:
                    self.symbols.variables[-1].pop("tempNameToRemoveDoNotNameAVariableThis")
                tempList = self.flatten(tempList)

                
                # ASSIGNMENT
                self.traverse(tree.children[2], tempList)
                tempList = self.flatten(tempList)

                tempList.append("push #PC-")
                count3_1 = len(tempList)-1
                tempList.append("jmp")
                count2_2 = len(tempList)-1

                values = [count1_2-count1_1, count2_2-count2_1+1, count3_1-count3_2]

                for i in range(len(tempList)):
                    if tempList[i] == "push #PC+" or tempList[i] == "push #PC-":
                        tempList[i] = tempList[i] + str(values[0])
                        values.pop(0)

                if list == None:
                    for i in tempList:
                        self.P.append(i)
                else:
                    for i in tempList:
                        list.append(i)

            elif len(tree.children)-1 == 2:
                if tree.children[0].name == "EXPR":
                    tempList.append("push #PC+")
                    count1_1 = len(tempList)-1
                    count3_2 = len(tempList)-1

                    # EXPR
                    tempList.append(self.getVarValueNP(tree.children[0]))
                    tempList = self.flatten(tempList)

                    tempList.append("cjmp")

                    tempList.append("push #PC+")
                    count2_1 = len(tempList)-1
                    tempList.append("jmp")
                    count1_2 = len(tempList)

                    # BLOCK
                    self.symbols.variables[-1]["tempNameToRemoveDoNotNameAVariableThis"] = [None, (None, None)]
                    self.traverse(tree.children[2], tempList)
                    if "tempNameToRemoveDoNotNameAVariableThis" in self.symbols.variables[-1]:
                        self.symbols.variables[-1].pop("tempNameToRemoveDoNotNameAVariableThis")
                    tempList = self.flatten(tempList)

                    # ASSIGNMENT
                    self.traverse(tree.children[1], tempList)
                    tempList = self.flatten(tempList)

                    tempList.append("push #PC-")
                    count3_1 = len(tempList)-1
                    tempList.append("jmp")
                    count2_2 = len(tempList)-1

                    values = [count1_2-count1_1, count2_2-count2_1+1, count3_1-count3_2]

                    for i in range(len(tempList)):
                        if tempList[i] == "push #PC+" or tempList[i] == "push #PC-":
                            tempList[i] = tempList[i] + str(values[0])
                            values.pop(0)

                    if list == None:
                        for i in tempList:
                            self.P.append(i)
                    else:
                        for i in tempList:
                            list.append(i)
                            
                else:
                    # VARDECL
                    self.traverse(tree.children[0], tempList)
                    tempList = self.flatten(tempList)

                    tempList.append("push #PC+")
                    count1_1 = len(tempList)-1
                    count3_2 = len(tempList)-1

                    # EXPR
                    tempList.append(self.getVarValueNP(tree.children[1]))
                    tempList = self.flatten(tempList)

                    tempList.append("cjmp")

                    tempList.append("push #PC+")
                    count2_1 = len(tempList)-1
                    tempList.append("jmp")
                    count1_2 = len(tempList)

                    # BLOCK
                    self.symbols.variables[-1]["tempNameToRemoveDoNotNameAVariableThis"] = [None, (None, None)]
                    self.traverse(tree.children[2], tempList)
                    if "tempNameToRemoveDoNotNameAVariableThis" in self.symbols.variables[-1]:
                        self.symbols.variables[-1].pop("tempNameToRemoveDoNotNameAVariableThis")
                    tempList = self.flatten(tempList)

                    tempList.append("push #PC-")
                    count3_1 = len(tempList)-1
                    tempList.append("jmp")
                    count2_2 = len(tempList)-1

                    values = [count1_2-count1_1, count2_2-count2_1+1, count3_1-count3_2]

                    for i in range(len(tempList)):
                        if tempList[i] == "push #PC+" or tempList[i] == "push #PC-":
                            tempList[i] = tempList[i] + str(values[0])
                            values.pop(0)

                    if list == None:
                        for i in tempList:
                            self.P.append(i)
                    else:
                        for i in tempList:
                            list.append(i)
            
            else:
                tempList.append("push #PC+")
                count1_1 = len(tempList)-1
                count3_2 = len(tempList)-1

                # EXPR
                tempList.append(self.getVarValueNP(tree.children[0]))
                tempList = self.flatten(tempList)

                tempList.append("cjmp")

                tempList.append("push #PC+")
                count2_1 = len(tempList)-1
                tempList.append("jmp")
                count1_2 = len(tempList)

                # BLOCK
                self.symbols.variables[-1]["tempNameToRemoveDoNotNameAVariableThis"] = [None, (None, None)]
                self.traverse(tree.children[1], tempList)
                if "tempNameToRemoveDoNotNameAVariableThis" in self.symbols.variables[-1]:
                        self.symbols.variables[-1].pop("tempNameToRemoveDoNotNameAVariableThis")
                tempList = self.flatten(tempList)

                tempList.append("push #PC-")
                count3_1 = len(tempList)-1
                tempList.append("jmp")
                count2_2 = len(tempList)-1

                values = [count1_2-count1_1, count2_2-count2_1+1, count3_1-count3_2]

                for i in range(len(tempList)):
                    if tempList[i] == "push #PC+" or tempList[i] == "push #PC-":
                        tempList[i] = tempList[i] + str(values[0])
                        values.pop(0)

                if list == None:
                    for i in tempList:
                        self.P.append(i)
                else:
                    for i in tempList:
                        list.append(i)

            for i in self.symbols.variables[:-1]:
                for j in i:
                    if j != "tempNameToRemoveDoNotNameAVariableThis":
                        i[j][1] = (i[j][1][0], i[j][1][1]-1)

            self.symbols.variables.pop(-1); self.symbols.functions.pop(-1)

            if list == None:
                self.P.append("cframe")
            else:
                list.append("cframe")

        if tree.name == "WHILESTATEMENT":
            tempList = []
            self.symbols.variables.append({}); self.symbols.functions.append({})

            for i in self.symbols.variables[:-1]:
                for j in i:
                    if j != "tempNameToRemoveDoNotNameAVariableThis":
                        i[j][1] = (i[j][1][0], i[j][1][1]+1)
            
            tempList.append("push #PC+")
            count1_1 = len(tempList)-1

            tempList.append(self.getVarValueNP(tree.children[0]))
            tempList = self.flatten(tempList)

            tempList.append("cjmp")

            tempList.append("push #PC+")
            count2_1 = len(tempList)-1
            tempList.append("jmp")

            count1_2 = len(tempList)

            for i in tree.children[1].children:
                self.getVarValueNP(i)


            self.symbols.variables[-1]["tempNameToRemoveDoNotNameAVariableThis"] = [None, (None, None)]
            self.traverse(tree.children[1], tempList)
            if "tempNameToRemoveDoNotNameAVariableThis" in self.symbols.variables[-1]:
                self.symbols.variables[-1].pop("tempNameToRemoveDoNotNameAVariableThis")
            tempList = self.flatten(tempList)


            tempList.append("push #PC-")
            count3_1 = len(tempList)-1
            tempList.append("jmp")
            count2_2 = len(tempList)-1

            values = [count1_2-count1_1, count2_2-count2_1+1, count3_1]

            for i in range(len(tempList)):
                if tempList[i] == "push #PC+" or tempList[i] == "push #PC-":
                    tempList[i] = tempList[i] + str(values[0])
                    values.pop(0)

            tempList = ["oframe"] + tempList

            if list == None:
                for i in tempList:
                    self.P.append(i)
            else:
                for i in tempList:
                    list.append(i)

            for i in self.symbols.variables[:-1]:
                for j in i:
                    if j != "tempNameToRemoveDoNotNameAVariableThis":
                        i[j][1] = (i[j][1][0], i[j][1][1]-1)

            self.symbols.variables.pop(-1); self.symbols.functions.pop(-1)

            if list == None:
                self.P.append("cframe")
            else:
                list.append("cframe")

        if tree.name == "FUNCTIONDECL":
            list = []
            functionCode = []
            functionCode.append("." + tree.children[0].value)

            # no params
            if tree.children[1].name == "ARROW":
                self.traverse(tree.children[3], functionCode)
            #yes params
            else:
                params = []

                for i in tree.children[1].children:
                    params = [i] + params

                block = tree.children[4]

                self.symbols.variables.append({}); self.symbols.functions.append({})
            
                if params != None:
                    for param in params:
                        vName = param.children[0].value
                        self.symbols.variables[-1][vName] = ["0", ((len(self.symbols.variables[-1])), 0)]

                for child in block.children:
                    self.traverse(child, functionCode)

                self.symbols.variables.pop(-1); self.symbols.functions.pop(-1)

            self.functionsList.append(functionCode)

        if tree.name == "STATEMENT":
            if list == None:
                self.traverse(tree.children[0], None)
            else:
                return self.traverse(tree.children[0], list)

        if tree.name == "BLOCK":
            for child in tree.children:
                self.traverse(child, list)

        if tree.name == "PROGRAM":
            self.P.append(".main")
            self.symbols.variables.append({}); self.symbols.functions.append({})
            
            for child in tree.children:
                self.traverse(child, None)
            
            self.symbols.variables.pop(-1); self.symbols.functions.pop(-1)
            self.P.append("halt")


    def addPush(self, toPush):
        if toPush in ["height", "width"]:
            self.P.append(toPush)
        elif type(toPush) == type(tuple()):
            self.P.append("push [" + str(toPush[0]) + ":" + str(toPush[1]) + "]")
        else:
            self.P.append("push " + str(toPush))

    def getVarValue(self, value):

        if value.name == "BOOLEANLITERAL":
            if value.value == "true":
                self.addPush(1)
                return 1
            else:
                self.addPush(0)
                return 0            

        if value.name == "INTEGERLITERAL":
            self.addPush(value.value)
            return value.value
        
        if value.name == "FLOATLITERAL":
            self.addPush(value.value)            
            return value.value
        
        if value.name == "COLOURLITERAL":
            self.addPush(value.value)            
            return value.value

        if value.name == "PADWIDTH":
            self.P.append("width")
            return 36

        if value.name == "PADHEIGHT":
            self.P.append("height")
            return 36
        
        if value.name == "PADRANDI":
            self.getVarValue(value.children[1])
            
            self.P.append("irnd")

        if value.name == "LITERAL":
            return self.getVarValue(value.children[0])

        if value.name == "IDENTIFIER":
            for scope in self.symbols.variables:
                if value.value in scope:
                    self.addPush(scope[value.value][1])
                    return scope[value.value][0]

        if value.name == "FUNCTIONCALL":
            if len(value.children) == 1:
                self.P.append("push 0")
                self.P.append("push ." + value.children[0].value)
                self.P.append("call")
            else:  
                aParms = value.children[1].children
                for i in aParms:
                    self.getVarValue(i)

                self.P.append("push " + str(len(aParms)))
                self.P.append("push ." + value.children[0].value)
                self.P.append("call")

        if value.name == "UNARY":
            temp = "push " + str(value.children[0].name)
            val = self.getVarValue(value.children[1])
            self.P.pop(-1)
            temp += val
            self.P.append(temp)

        if value.name == "SUBEXPR":
            self.getVarValue(value.children[0])

        if value.name == "EXPR":
            if len(value.children) > 1:
                counter = 0
                
                while counter < len(value.children)-1:
                    self.getVarValue(value.children[counter + 2])

                    if counter == 0:
                        temp = self.getVarValue(value.children[counter])

                    op = value.children[counter + 1].value
                    if op == "<": self.P.append("lt")
                    elif op == "<=": self.P.append("le")
                    elif op == ">": self.P.append("gt")
                    elif op == ">=": self.P.append("ge")
                    elif op == "==": self.P.append("eq")

                    counter += 2
                return temp
                                
            else:
                return self.getVarValue(value.children[0])

        if value.name == "SIMPLEEXPR":
            if len(value.children) > 1:
                counter = 0
                
                while counter < len(value.children)-1:
                    self.getVarValue(value.children[counter + 2])

                    if counter == 0:
                        temp = self.getVarValue(value.children[counter])

                    op = value.children[counter + 1].value
                    if op == "+": self.P.append("add")
                    elif op == "-": self.P.append("sub")

                    counter += 2
                return temp
                            
            else:
                return self.getVarValue(value.children[0])

        if value.name == "TERM":
            if len(value.children) > 1:
                counter = 0
                
                while counter < len(value.children)-1:
                    self.getVarValue(value.children[counter + 2])

                    if counter == 0:
                        temp = self.getVarValue(value.children[counter])

                    op = value.children[counter + 1].value
                    if op == "*": self.P.append("mul")
                    elif op == "/": self.P.append("div")

                    counter += 2
                return temp
            
            else:
                return self.getVarValue(value.children[0])

        if value.name == "FACTOR":
            return self.getVarValue(value.children[0])
        
    def getVarValueNP(self, value):
        tempMain = []

        if value.name == "PADRANDI":
            tempMain.append(self.getVarValueNP(value.children[1]))
            tempMain.append("irnd")
            return tempMain

        if value.name == "FUNCTIONCALL":
            if len(value.children) == 1:
                tempMain.append("push 0")
                tempMain.append("push ." + value.children[0].value)
                tempMain.append("call")
                return tempMain
    
            else:  
                aParms = value.children[1].children
                for i in aParms:
                    tempMain.append(self.getVarValueNP(i))

                tempMain.append("push " + str(len(aParms)))
                tempMain.append("push ." + value.children[0].value)
                tempMain.append("call")
                return tempMain

        if value.name == "UNARY":
            temp = "push " + str(value.children[0].name)
            temp += self.getVarValueNP(value.children[1])[5:]
            return temp

        if value.name == "SUBEXPR":
            return self.getVarValueNP(value.children[0])

        if value.name == "EXPR":
            if len(value.children) > 1:
                counter = 0
                
                while counter < len(value.children)-1:
                    temp1 = self.getVarValueNP(value.children[counter + 2])
                    tempMain.append(temp1)

                    if counter == 0:
                        temp = self.getVarValueNP(value.children[counter])
                        tempMain.append(temp)

                    op = value.children[counter + 1].value
                    if op == "<": tempMain.append("lt")
                    elif op == "<=": tempMain.append("le")
                    elif op == ">": tempMain.append("gt")
                    elif op == ">=": tempMain.append("ge")
                    elif op == "==": tempMain.append("eq")

                    counter += 2
                return tempMain
                                
            else:
                return self.getVarValueNP(value.children[0])

        if value.name == "SIMPLEEXPR":
            if len(value.children) > 1:
                counter = 0
                
                while counter < len(value.children)-1:
                    temp1 = self.getVarValueNP(value.children[counter + 2])
                    tempMain.append(temp1)

                    if counter == 0:
                        temp = self.getVarValueNP(value.children[counter])
                        tempMain.append(temp)

                    op = value.children[counter + 1].value
                    if op == "+": tempMain.append("add")
                    elif op == "-": tempMain.append("sub")

                    counter += 2
                return tempMain
                            
            else:
                return self.getVarValueNP(value.children[0])

        if value.name == "TERM":
            if len(value.children) > 1:
                counter = 0
                
                while counter < len(value.children)-1:
                    temp1 = self.getVarValueNP(value.children[counter + 2])
                    tempMain.append(temp1)

                    if counter == 0:
                        temp = self.getVarValueNP(value.children[counter])
                        tempMain.append(temp)

                    op = value.children[counter + 1].value
                    if op == "*": tempMain.append("mul")
                    elif op == "/": tempMain.append("div")

                    counter += 2
                return tempMain
            else:
                return self.getVarValueNP(value.children[0])

        if value.name == "FACTOR":
            return self.getVarValueNP(value.children[0])
    
        if value.name == "LITERAL":
            return self.getVarValueNP(value.children[0])

        if value.name == "BOOLEANLITERAL":
            if value.value == "true":
                return "push 1"
            else:
                return "push 0"

        if value.name == "INTEGERLITERAL":
            return "push " + value.value
        
        if value.name == "FLOATLITERAL":
            return "push " + value.value
        
        if value.name == "COLOURLITERAL":
           return "push " + value.value

        if value.name == "IDENTIFIER":
            for scope in self.symbols.variables:
                if value.value in scope:
                    locations = (scope[value.value][1])
                    return ("push [" + str(locations[0]) + ":" + str(locations[1]) + "]")

        if value.name == "PADHEIGHT":
            return "height"
        
        if value.name == "PADWIDTH":
            return "width"
        
    def flatten(self, temp):
        flattened = []
        for item in temp:
            if isinstance(item, list):
                flattened.extend(self.flatten(item))
            else:
                flattened.append(item)
        return flattened  

    # PRINT/SAVE CODE
    def printCode(self):
        f = open("Code/OutputFiles/pixIrCode.txt", "w"); f.write(""); f.close()

        f = open("Code/OutputFiles/pixIrCode.txt", "w")
        self.P = self.flatten(self.P)
        for line in self.P:
            f.write(line); f.write("\n")
            if line == "halt" or line == "ret":
                f.write("\n")
        f.close()

