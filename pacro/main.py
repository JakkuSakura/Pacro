import argparse

from pacro import Pacro


def get_args():
    arg_parser = argparse.ArgumentParser(description='Pacro commandline utility')
    arg_parser.add_argument('files', type=str, nargs='*', help='input files: stdin (default) | '
                                                               'project root directory | single file | '
                                                               'multiple files.', default='stdin')
    arg_parser.add_argument('-o', '--output', type=str,
                            help='the files you want to output the result: '
                                 'stdout (default) | filename | path ',
                            default='stdout')
    arg_parser.add_argument('--overwrite', help='overwrite source files', action='store_true')
    arg_parser.add_argument('-v', '--verbose', help='detailed output', action='store_true')

    return arg_parser.parse_args()


def main():
    args = get_args()
    Pacro(args).run()


if __name__ == '__main__':
    main()
