from typing import List, Optional

import token_types
from basic_lexer import BasicLexer
from basic_token import Tokens, Token


class AstNode:

    def __init__(self):
        pass

    def __str__(self):
        type_name = type(self).__name__
        return type_name


class LineNode(AstNode):
    def __init__(self, chars: List[Token]):
        super().__init__()
        self.chars = chars

    def get_string(self) -> str:
        s = []
        for c in self.chars:
            s.append(c.content)
        return ''.join(s)

    def __str__(self):
        return 'LineNode(' + self.get_string() + ')'


class CodeBlockNode(AstNode):
    def __init__(self, lines: List[LineNode]):
        super().__init__()
        self.lines = lines

    def to_string(self, newline='\n'):
        return newline.join([x.get_string() for x in self.lines]) + newline

    def __str__(self):
        return 'TextBlockNode(' + self.to_string() + ')'


class ConfigBlockNode(AstNode):
    def __init__(self, lines: List[LineNode]):
        super().__init__()
        self.lines = lines
        self.config = {}
        for line in lines:
            key, value = line.get_string().split(':')
            self.config[key.strip()] = value.strip()

    def __str__(self):
        return 'ConfigBlockNode' + str(self.config)

    def __getitem__(self, item):
        return self.config[item]

    def __setitem__(self, key, value):
        self.config[key] = value


class TextBlockNode(AstNode):
    def __init__(self, lines: List[LineNode]):
        super().__init__()
        self.lines = lines

    def to_string(self, newline='\n'):
        return newline.join([x.get_string() for x in self.lines]) + newline

    def __str__(self):
        return 'TextBlockNode(' + self.to_string() + ')'


class BasicParser:
    def __init__(self):
        self.tokens = None
        self.root = []

    def set_tokens(self, tokens: Tokens):
        self.tokens = tokens

    def parse_line(self) -> Optional[LineNode]:
        chars: List[Token] = []
        while token := self.tokens.pop_token():
            if token.type == token_types.newline:
                return LineNode(chars)
            chars.append(token)

        # EOF
        if chars:
            return LineNode(chars)

        return None

    def parse_config_block(self) -> Optional[ConfigBlockNode]:
        lines = []
        while token := self.tokens.peek_token():
            if token.type == token_types.config_comment:
                self.tokens.pop_token()
                if newline := self.parse_line():
                    lines.append(newline)
            else:
                break
        if lines:
            return ConfigBlockNode(lines)
        else:
            return None

    def parse_code_block(self) -> Optional[CodeBlockNode]:
        lines: List[LineNode] = []
        while token := self.tokens.peek_token():
            if token.type == token_types.code_comment:
                self.tokens.pop_token()
                if newline := self.parse_line():
                    lines.append(newline)
            else:
                break
        if lines:
            return CodeBlockNode(lines)
        else:
            return None

    def parse_text_block(self) -> Optional[TextBlockNode]:
        lines: List[LineNode] = []
        while line := self.parse_line():
            lines.append(line)

        if lines:
            return TextBlockNode(lines)
        else:
            return None

    def do_parse(self) -> List[AstNode]:
        root_node: List[AstNode] = []
        while self.tokens.peek_token():
            next_node: Optional[AstNode]
            if next_node := self.parse_config_block():
                root_node.append(next_node)
            elif next_node := self.parse_code_block():
                root_node.append(next_node)
            elif next_node := self.parse_text_block():
                root_node.append(next_node)
            else:
                raise Exception("Parse error")
        return root_node


def main():
    lexer = BasicLexer()
    lexer.replace('''//% Lang: Python
//$ code("int foo(){}");
int main() {

}''')
    lexer.do_lexer()
    parser = BasicParser()
    parser.set_tokens(lexer.take_tokens())
    root = parser.do_parse()
    for node in root:
        print(node)


if __name__ == '__main__':
    main()
