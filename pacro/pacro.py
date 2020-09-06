from basic_interpreter import BasicInterpreter
from basic_lexer import BasicLexer
from basic_parser import BasicParser
from input_stream import InputStream, StdinStream, FileInputStream
from output_stream import StdoutStream, FileOutputStream
from utils import open_file


class ArgumentException(Exception):
    def __init__(self, message):
        super(ArgumentException, self).__init__(message)


def check_args(args):
    if args.output != 'stdout' and args.overwrite:
        raise ArgumentException("Argument conflicts: output and overwrite cannot be both set")
    if args.files == 'stdin' and args.overwrite:
        raise ArgumentException('Input should be files if you use --overwrite')


class Pacro:
    def __init__(self, args):
        if args.verbose:
            print(args)
        check_args(args)
        self.args = args

    def run(self):
        self.process_input_files(self.args.files)

    def process_single_file(self, file: InputStream):
        lexer = BasicLexer()
        tokens = lexer.do_lexer(file.read())
        parser = BasicParser()
        root = parser.do_parse(tokens)

        interpreter = BasicInterpreter()
        if self.args.overwrite:
            assert isinstance(file, FileInputStream), 'Input should be files if you use --overwrite'

            file.close()
            output = FileOutputStream(file.filename)
        elif isinstance(self.args.output, str):
            if self.args.output_types == 'stdout':
                output = StdoutStream()
            else:
                output = FileOutputStream(self.args.output)
        else:
            raise NotImplementedError()
        interpreter.set_code_output(output)
        interpreter.do_interpret(root)

    def process_input_files(self, input_files_names, depth=1):
        if input_files_names == 'stdin':
            self.process_single_file(StdinStream())
            return

        if not isinstance(input_files_names, list):
            input_files_names = [input_files_names]

        for input_file in input_files_names:
            if file := open_file(input_file):
                if isinstance(file, list):
                    self.process_input_files(file, depth=depth + 1)
                else:
                    if self.args.verbose or self.args.output == 'stdout' and depth >= 2:
                        print("File:", input_file)
                    self.process_single_file(file)
            elif depth == 1:
                raise FileNotFoundError(input_file)
