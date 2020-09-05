from basic_interpreter import BasicInterpreter, code_output_print, code_output_file
from basic_lexer import BasicLexer
from basic_parser import BasicParser
from utils import open_file


class Pacro:
    def __init__(self, args):
        if args.verbose:
            print(args)
        self.output_types = args.output
        self.input_files = args.files
        self.verbose = args.verbose

    def run(self):
        self.process_input_files(self.input_files)

    def process_single_file(self, file):
        lexer = BasicLexer()
        tokens = lexer.do_lexer(file.read())

        parser = BasicParser()
        root = parser.do_parse(tokens)

        interpreter = BasicInterpreter()
        if isinstance(self.output_types, str):
            if self.output_types == 'stdout':
                interpreter.set_code_output(code_output_print)
            elif self.output_types == 'overwrite':
                file.seek(0)
                interpreter.set_code_output(lambda *args, **kwargs: code_output_file(file, *args, **kwargs))
            else:
                f = open(file, 'w')
                interpreter.set_code_output(lambda *args, **kwargs: code_output_file(f, *args, **kwargs))
        else:
            raise NotImplementedError()
        interpreter.do_interpret(root)

    def process_input_files(self, input_files_names, depth=1):
        if not isinstance(input_files_names, list):
            input_files_names = [input_files_names]

        for input_file in input_files_names:
            if file := open_file(input_file):
                if isinstance(file, list):
                    self.process_input_files(file, depth=depth + 1)
                else:
                    if self.output_types == 'stdout' and depth >= 2:
                        print("File:", input_file)
                    self.process_single_file(file)
            elif depth == 1:
                raise FileNotFoundError(input_file)
