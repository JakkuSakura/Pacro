import os
import sys
from basic_interpreter import BasicInterpreter
from basic_lexer import BasicLexer
from basic_parser import BasicParser
import argparse


def get_args():
    arg_parser = argparse.ArgumentParser(description='Pacro commandline utility')
    arg_parser.add_argument('files', type=str, nargs='*', help='input files: stdin (default) | '
                                                               'project root directory | single file | '
                                                               'multiple files.', default=['stdin'])
    arg_parser.add_argument('-o', '--output', type=str, nargs='?', help='The type you want to output the result: '
                                                                        'stdout (default) | filename | path ',
                            default='stdout')
    return arg_parser.parse_args()


def open_file(filename):
    if filename == 'stdin':
        return sys.stdin
    elif os.path.isfile(filename):
        return open(filename, 'r')
    elif os.path.isdir(filename):
        return os.listdir(filename)
    else:
        return None


def process_single_file(file):
    lexer = BasicLexer()
    tokens = lexer.do_lexer(file.read())

    parser = BasicParser()
    root = parser.do_parse(tokens)

    interpreter = BasicInterpreter()
    interpreter.do_interpret(root)


def process_input_files(input_files, depth=1):
    for input_file in input_files:
        if files := open_file(input_file):
            if isinstance(files, list):
                process_input_files(files, depth=depth + 1)
            else:
                process_single_file(files)
        elif depth == 1:
            raise FileNotFoundError(input_file)


def main():
    args = get_args()
    input_files = args.files
    process_input_files(input_files)


if __name__ == '__main__':
    main()
