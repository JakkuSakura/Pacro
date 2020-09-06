import hashlib
import os
import sys
from typing import List, Any, Union, Sequence

from input_stream import InputStream, FileInputStream


def is_prefix(a: List[str], b: Any) -> bool:
    '''
        :param a: List[str], List[char] actually
        :param b: str or list of str (it actually supports recursion)
        :return: true if a is prefix of b or x (x in b)
    '''
    if isinstance(b, str):
        if len(a) > len(b):
            return False
        for i in range(len(a)):
            if a[i] != b[i]:
                return False
        return True

    elif isinstance(b, list):
        for x in b:
            if is_prefix(a, x):
                return True
        return False
    else:
        raise TypeError()


def equals(a: List[str], b: Any) -> bool:
    '''
    :param a: List[str], List[char] actually
    :param b: str or list of str (it actually supports recursion)
    :return: true if a == b, or a == x (x in b)
    '''
    if isinstance(b, str):
        return a == list(b)
    elif isinstance(b, list):
        for x in b:
            if equals(a, x):
                return True
        return False
    else:
        raise TypeError()


def open_file(filename) -> Union[InputStream, List[str], None]:
    # filename = os.path.realpath(filename)
    if os.path.isfile(filename):
        return FileInputStream(filename)
    elif os.path.isdir(filename):
        return [os.path.join(filename, x) for x in os.listdir(filename)]
    else:
        return None


def count_indent(line: str):
    for i in range(len(line)):
        if not line[i].isspace():
            return i
    return len(line)


def white_hash(s: str, number_of_digits=6) -> str:
    h = hashlib.new('md5')
    for x in s:
        if not x.isspace():
            h.update(x.encode('utf-8'))
    return h.hexdigest()[:number_of_digits]


def lines_to_string(lines: Sequence[Any], prefix='', indent='', end_of_line='\n') -> str:
    buf = []
    for line in lines:
        if not line:
            continue
        if isinstance(line, str):
            if not line.strip():
                continue

        if isinstance(indent, str):
            buf.append(indent)
        elif isinstance(indent, int):
            buf.append(' ' * indent)
        else:
            buf.append(str(indent))

        buf.append(prefix)
        if isinstance(line, str):
            buf.append(line)
            buf.append(end_of_line)
        else:
            buf.append(line.to_string(end_of_line))

    return ''.join(buf)


