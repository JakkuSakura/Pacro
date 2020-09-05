from typing import List, Optional, Any

from lexer_token import Token, Tokens
from lexer_config import config_comment, code_comment, newline
import token_types
from utils import is_prefix, equals


class Buffer:
    def __init__(self, buf: str):
        self.buf = buf
        self.ptr = 0

    def peek_char(self) -> Optional[str]:
        if self.ptr >= len(self.buf):
            return None
        return self.buf[self.ptr]

    def pop_char(self) -> Optional[str]:
        if char := self.peek_char():
            self.ptr += 1
            return char

        return None

    def match(self, pat: Any) -> Optional[str]:
        if isinstance(pat, list):
            for p in pat:
                if m := self.match(p):
                    return m
            return None
        else:
            assert isinstance(pat, str)

            if self.ptr + len(pat) >= len(self.buf):
                return None
            s = self.buf[self.ptr:self.ptr + len(pat)]
            if s == pat:
                return s

        return None

    def match_forward(self, pat: Any) -> Optional[str]:
        if s := self.match(pat):
            self.ptr += len(pat)
            return s

        return None


class BasicLexer:
    def __init__(self):
        self.tokens = Tokens()
        self.col = 1
        self.row = 1
        self.saved_row = 1
        self.saved_col = 1

    def process_char(self, chars: str):
        for ch in chars:
            if ch == '\n':
                self.col = 1
                self.row += 1
            else:
                self.col += 1

    def reset(self):
        self.tokens.clear()
        self.col = 1
        self.row = 1

        self.saved_row = 1
        self.saved_col = 1

    def save_pos(self):
        self.saved_row = self.row
        self.saved_col = self.col

    # noinspection PyShadowingBuiltins
    def new_token(self, type: str, content):
        self.tokens.append(Token(row=self.saved_row, col=self.saved_col, type=type, content=content))

    def do_lexer(self, buf: List[str]):
        assert self.tokens.is_empty(), "You should not call do_lexer() twice on the same lexer object"
        self.reset()
        buf = Buffer(buf)

        while buf.peek_char():
            self.save_pos()
            if matched := buf.match_forward(config_comment):
                self.new_token(type=token_types.config_comment, content=matched)
            elif matched := buf.match_forward(code_comment):
                self.new_token(type=token_types.code_comment, content=matched)
            elif matched := buf.match_forward(newline):
                self.new_token(type=token_types.newline, content=matched)
            else:
                matched = buf.pop_char()
                self.new_token(type=token_types.char, content=matched)

            self.process_char(matched)

        return self.take_tokens()

    def take_tokens(self) -> Tokens:
        t = self.tokens
        self.tokens = Tokens()
        return t


def main(mute=False):
    lexer = BasicLexer()
    tokens = lexer.do_lexer('''//% Lang: Python
//$ for i in range(10):
//$     code(f"int foo_{i}()"+"{}")
//$ 

/* topic */
int main() {

}''')
    if not mute:
        while token := tokens.pop_token():
            print(token)

    return tokens


if __name__ == '__main__':
    main()
