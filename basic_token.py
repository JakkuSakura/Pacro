import copy
class Token:
    def __init__(self, *args, **kwargs):
        self.row = kwargs['row']
        self.col = kwargs['col']
        self.type = kwargs['type']
        self.content = kwargs['content']

    def __str__(self):
        content = self.content.encode('unicode_escape').decode('utf-8')
        return f'Token({self.row},{self.col},{self.type},"{content}")'


class Tokens:
    def __init__(self):
        self.tokens: list = []
        self.token_ptr: int = 0

    def peek_token(self):
        if self.token_ptr < len(self.tokens):
            return self.tokens[self.token_ptr]
        else:
            return None

    def pop_token(self):
        if self.token_ptr < len(self.tokens):
            token = self.tokens[self.token_ptr]
            self.token_ptr += 1
            return token
        else:
            return None

    def push_back_token(self, token: Token):
        if self.token_ptr < 0:
            raise Exception(f"Cannot push back token: token_ptr={self.token_ptr}")

        self.token_ptr -= 1
        self.tokens[self.token_ptr] = token

    def clear(self):
        self.tokens.clear()
        self.token_ptr = 0

    def append(self, token: Token):
        assert self.token_ptr == 0, "You should not append tokens after starting reading"
        self.tokens.append(token)
        
    def clone(self):
        return copy.copy(self)

    def is_empty(self):
        return len(self.tokens) == 0
