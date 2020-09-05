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
        raise FileNotFoundError(filename)


def process_single_file(filename):
    lexer = BasicLexer()
    lexer.replace_buffer(filename)
    tokens = lexer.take_tokens()
    parser = BasicParser()
    root = parser.set_tokens(tokens)


def process_input_files(input_files):
    for input_file in input_files:
        files = open_file(input_file)
        if isinstance(files, list):
            process_input_files(files)
        else:
            process_single_file(files)


def main():
    args = get_args()
    input_files = args.files
    process_input_files(input_files)


if __name__ == '__main__':
    main()
