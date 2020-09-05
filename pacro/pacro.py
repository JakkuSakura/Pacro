from basic_interpreter import BasicInterpreter
from basic_lexer import BasicLexer
from basic_parser import BasicParser
from utils import open_file


class Pacro:
    def __init__(self, args):
        self.output_types = args.output
        self.input_files = args.files

    def run(self):
        self.process_input_files(self.input_files)

    def process_single_file(self, file):
        lexer = BasicLexer()
        tokens = lexer.do_lexer(file.read())

        parser = BasicParser()
        root = parser.do_parse(tokens)

        interpreter = BasicInterpreter()
        interpreter.do_interpret(root)

    def process_input_files(self, input_files, depth=1):
        for input_file in input_files:
            if files := open_file(input_file):
                if isinstance(files, list):
                    self.process_input_files(files, depth=depth + 1)
                else:
                    self.process_single_file(files)
            elif depth == 1:
                raise FileNotFoundError(input_file)