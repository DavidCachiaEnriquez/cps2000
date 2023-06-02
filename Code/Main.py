from Lexer import Lexer
from Parser import Parser
from Xml_Generator import XMLGeneration
from Semantic_Analysis import semanticAnalysis
from Code_Generation import codeGeneration

programs = ["Code/InputPrograms/program1.txt", "Code/InputPrograms/program2.txt",
            "Code/InputPrograms/program3.txt", "Code/InputPrograms/program4.txt"]

f = open(programs[3], "r"); code = f.read(); f.close()  

lexer = Lexer(code)
parser = Parser(lexer.tokenList)
xml = XMLGeneration(parser.tree)
semAnalysis = semanticAnalysis(parser.tree)
codeGen = codeGeneration(parser.tree)