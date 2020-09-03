from basic_token import Tokens


class BasicParser:
    def __init__(self):
        self.tokens = None

    def set_tokens(self, tokens: Tokens):
        self.tokens = tokens

    def do_parse(self):
        pass