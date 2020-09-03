from typing import List

from basic_token import Token, Tokens
from lexer_config import *
import token_types
from tools import is_prefix, equals


class BasicLexer:
    def __init__(self):
        self.buf: List[str] = []
        # self.buf_ptr: int = 0
        self.tokens = Tokens()
        self.col = 1
        self.row = 1

    def process(self, ch: str):
        if ch == '\n':
            self.col = 1
            self.row += 1
        else:
            self.col += 1

    def reset(self):
        self.buf.clear()
        # self.buf_ptr = 0
        self.tokens.clear()
        self.col = 0
        self.row = 1

    def replace(self, s: str):
        self.reset()
        self.buf.extend(s)

    def push(self, s: str):
        self.buf.extend(s)

    # noinspection PyShadowingBuiltins
    def new_token(self, type: str, content):
        self.tokens.append(Token(row=self.row, col=self.col, type=type, content=content))

    def do_lexer(self):
        assert self.tokens.is_empty(), "You should not call do_lexer() twice on the same lexer object"

        temp_buf = []
        for ch in self.buf:
            temp_buf.append(ch)
            if is_prefix(temp_buf, [config_comment, code_comment, newline]):
                if equals(temp_buf, config_comment):
                    self.new_token(type=token_types.config_comment, content=''.join(temp_buf))
                    temp_buf.clear()
                elif equals(temp_buf, code_comment):
                    self.new_token(type=token_types.code_comment, content=''.join(temp_buf))
                    temp_buf.clear()
                elif equals(temp_buf, newline):
                    self.new_token(type=token_types.newline, content=''.join(temp_buf))
                    temp_buf.clear()

            else:
                self.new_token(type=token_types.char, content=ch)
                temp_buf.clear()

            self.process(ch)

    def get_tokens(self) -> Tokens:
        return self.tokens.clone()

    def take_tokens(self) -> Tokens:
        t = self.tokens
        self.tokens = Tokens()
        return t


def main():
    lexer = BasicLexer()
    lexer.replace('''//% Lang: Python
//$ code("int foo(){}");
int main() {

}''')
    lexer.do_lexer()
    tokens = lexer.take_tokens()
    while token := tokens.pop_token():
        print(token)


if __name__ == '__main__':
    main()
