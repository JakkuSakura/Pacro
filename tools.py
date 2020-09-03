def is_prefix(a: list, b) -> bool:
    '''
        :param a: char list
        :param b: str or list of str
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


def equals(a: list, b) -> bool:
    '''
    :param a: char list
    :param b: str or list of str
    :return: true if a == b, or a == x (x in b)
    '''
    if isinstance(b, str):
        return a == list(b)
    elif isinstance(b, list):
        for x in b:
            if equals(a, x):
                return True
