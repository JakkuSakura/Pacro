import argparse

from pacro import Pacro


def get_args():
    arg_parser = argparse.ArgumentParser(description='Pacro commandline utility')
    arg_parser.add_argument('files', type=str, nargs='*', help='input files: stdin (default) | '
                                                               'project root directory | single file | '
                                                               'multiple files.', default=['stdin'])
    arg_parser.add_argument('-o', '--output', type=str,
                            help='The type you want to output the result: '
                                 'stdout (default) | overwrite | filename | path ',
                            default='stdout')

    arg_parser.add_argument('-v', '--verbose', nargs='?',
                            help='The type you want to output the result: '
                                 'stdout (default) | filename | path ')

    return arg_parser.parse_args()


def main():
    Pacro(get_args(), verbose=True).run()


if __name__ == '__main__':
    main()
