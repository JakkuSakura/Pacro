from basic_token import Token, Tokens
from lexer_config import *


def prefix(a: list, b):
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
            if prefix(a, x):
                return True


def compare(a: list, b):
    '''
    :param a: char list
    :param b: str or list of str
    :return: true if a == b, or a == x (x in b)
    '''
    if isinstance(b, str):
        return a == list(b)
    elif isinstance(b, list):
        for x in b:
            if compare(a, x):
                return True


class BasicLexer:
    def __init__(self):
        self.buf: list = []
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

    def new_token(self, type: str, content):
        self.tokens.append(Token(row=self.row, col=self.col, type=type, content=content))

    def do_lexer(self):
        assert self.tokens.is_empty(), "You should not call do_lexer() twice on the same lexer object"

        temp_buf = []
        for ch in self.buf:
            temp_buf.append(ch)
            if prefix(temp_buf, [config_comment, code_comment, newline]):
                if compare(temp_buf, config_comment):
                    self.new_token(type='config_comment', content=''.join(temp_buf))
                    temp_buf.clear()
                elif compare(temp_buf, code_comment):
                    self.new_token(type='code_comment', content=''.join(temp_buf))
                    temp_buf.clear()
                elif compare(temp_buf, newline):
                    self.new_token(type='newline', content=''.join(temp_buf))
                    temp_buf.clear()

            else:
                self.new_token(type='char', content=ch)
                temp_buf.clear()

            self.process(ch)

    def get_tokens(self):
        return self.tokens.clone()

    def take_tokens(self):
        t = self.tokens
        self.tokens = Tokens()
        return t


if __name__ == '__main__':
    lexer = BasicLexer()
    lexer.replace('''//% Lang: Python
//$ code("int foo(){}");
int main() {

}''')
    lexer.do_lexer()
    tokens = lexer.get_tokens()
    while token := tokens.pop_token():
        print(token)
