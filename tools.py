from typing import Union, List


def is_prefix(a: List[str], b: Union[str, List[str]]) -> bool:
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


def equals(a: List[str], b: Union[str, List[str]]) -> bool:
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
