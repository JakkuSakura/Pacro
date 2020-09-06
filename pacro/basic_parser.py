from typing import List, Optional

import basic_lexer
import token_types
from ast_nodes import AstNode, LineNode, CodeBlockNode, ConfigBlockNode, TextBlockNode, GeneratedCodeNode
from lexer_token import Tokens, Token


class BasicParser:
    def __init__(self):
        self.tokens = None
        self.root = []

    def set_tokens(self, tokens: Tokens):
        self.tokens = tokens

    def parse_line(self) -> Optional[LineNode]:
        chars: List[Token] = []
        while token := self.tokens.peek_token():
            if token.type == token_types.newline:
                self.tokens.pop_token()
                return LineNode(chars)
            elif token.type == token_types.char:
                self.tokens.pop_token()
                chars.append(token)
            else:
                break
        # EOF
        if chars:
            return LineNode(chars)

        return None

    def parse_whitespace(self) -> bool:
        if token := self.tokens.peek_token():
            if token.type == token_types.char and token.content.isspace():
                self.tokens.pop_token()
                return True
            elif token.type == token_types.newline:
                self.tokens.pop_token()
                return True
        return False

    def parse_config_block(self) -> Optional[ConfigBlockNode]:
        token_ptr = self.tokens.get_pos()

        lines = []
        while self.tokens.peek_token():
            while self.parse_whitespace():
                pass

            token = self.tokens.peek_token()
            if token.type == token_types.config_comment:
                self.tokens.pop_token()
                if newline := self.parse_line():
                    lines.append(newline)
            else:
                break
        if lines:
            return ConfigBlockNode(lines)
        else:
            self.tokens.set_pos(token_ptr)
            return None

    def parse_generated_code_block(self) -> Optional[GeneratedCodeNode]:
        token_ptr = self.tokens.get_pos()

        lines = []
        while line := self.parse_line():
            lines.append(line)

        if tk := self.tokens.peek_token():
            if tk.type == token_types.generated_code_comment:
                self.tokens.pop_token()
                line = self.parse_line()
                return GeneratedCodeNode(lines, line)

        self.tokens.set_pos(token_ptr)
        return None

    def parse_code_block(self) -> Optional[CodeBlockNode]:
        config_block = self.parse_config_block()
        lines: List[LineNode] = []
        indent = None
        while self.tokens.peek_token():
            token_ptr = self.tokens.get_pos()
            while self.parse_whitespace():
                pass

            token = self.tokens.peek_token()
            if token.type == token_types.code_comment:
                if indent is None:
                    indent = token.col - 1
                self.tokens.pop_token()
                if newline := self.parse_line():
                    lines.append(newline)
            else:
                self.tokens.set_pos(token_ptr)
                break

        if lines:
            generated_code = self.parse_generated_code_block()
            return CodeBlockNode(config_block, lines, generated_code, indent or 0)
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

    def do_parse(self, tokens: Optional[Tokens] = None) -> List[AstNode]:
        if tokens:
            self.set_tokens(tokens)
        root_node: List[AstNode] = []
        while self.tokens.peek_token():
            next_node: Optional[AstNode]
            if next_node := self.parse_code_block():
                root_node.append(next_node)
            elif next_node := self.parse_config_block():
                root_node.append(next_node)
            elif next_node := self.parse_text_block():
                root_node.append(next_node)
            else:
                raise Exception("Parse error")
        return root_node


def main(mute=False):
    parser = BasicParser()
    root = parser.do_parse(basic_lexer.main(mute=True))
    if not mute:
        for node in root:
            print(node)
    return root


if __name__ == '__main__':
    main()
