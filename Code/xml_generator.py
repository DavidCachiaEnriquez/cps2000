from Parser import NTerminalNode

# XML CLASS
class XMLGeneration:
    def __init__(self, tree):
        self.AST = tree
        self.stack = []
        self.space = ""

        print("\nX M L   G E N E R A T I O N")
        xmlFull = self.createXML(self.AST)
        xmlMin = self.createXMLMinimized(self.AST)

        self.printXML(xmlFull, xmlMin)
        print("Printed XML Full and XML Minimized")       

    # CREATE FULL XML AND MINIMIZED XML
    def createXML(self, tree):
        temp = []
        if isinstance(tree, NTerminalNode):
            temp.append(self.space + "<" + tree.name + ">")

            self.stack.append(tree.name); self.space += "  "

            for child in tree.children:
                temp.append(self.createXML(child))
                temp = self.flatten(temp)
            
            self.space = self.space[:-2]
            temp.append(self.space + "</" + self.stack[-1] + ">")
            
            self.stack.pop(); 
        else:
            temp.append(self.space + "<" + str(tree.name) + "> " + str(tree.value) + " </" + tree.name + ">")

        return temp

    def createXMLMinimized(self, tree):
        temp = []
        if isinstance(tree, NTerminalNode):
            if len(tree.children) != 1 or tree.name == "PROGRAM":
                temp.append(self.space + "<" + tree.name + ">")

                self.stack.append(tree.name); self.space += "  "

                for child in tree.children:
                    temp.append(self.createXMLMinimized(child))
                    temp = self.flatten(temp)
                
                self.space = self.space[:-2]
                temp.append(self.space + "</" + self.stack[-1] + ">")

                self.stack.pop(); 
            else:
                for child in tree.children:
                    temp.append(self.createXMLMinimized(child))
                    temp = self.flatten(temp)       
        else:
            temp.append(self.space + "<" + str(tree.name) + "> " + str(tree.value) + " </" + tree.name + ">")
        return temp

    def flatten(self, temp):
        flattened = []
        for item in temp:
            if isinstance(item, list):
                flattened.extend(self.flatten(item))
            else:
                flattened.append(item)
        return flattened

    # SAVE AST IN XML FORMAT
    def printXML(self, xmlFull, xmlMin):
        f1 = open("Code/OutputFiles/xmlFull.txt", "w"); f1.write(""); f1.close()
        f2 = open("Code/OutputFiles/xmlFull.txt", "a")
        for line in xmlFull:
            f2.write(line); f2.write("\n")
        f2.close()

        f1 = open("Code/OutputFiles/xmlMinimized.txt", "w"); f1.write(""); f1.close()
        f2 = open("Code/OutputFiles/xmlMinimized.txt", "a")
        for line in xmlMin:
            f2.write(line); f2.write("\n")
        f2.close()

