from typing import List

import token_types
from basic_token import Tokens


class AstNode:
    def __init__(self, type: str):
        self.type = type


class ConfigBlockNode(AstNode):
    def __init__(self, lines: list):
        super().__init__("ConfigBlockNode")
        self.lines = lines


class CodeBlockNode(AstNode):
    def __init__(self, lines: list):
        super().__init__("CodeBlockNode")
        self.lines = lines


class LineNode(AstNode):
    def __init__(self, chars: list):
        super().__init__("CodeBlockNode")
        self.chars = chars


class CharBlockNode(AstNode):
    def __init__(self, chars: list):
        super().__init__("CharBlockNode")
        self.chars = list


class BasicParser:
    def __init__(self):
        self.tokens = None
        self.root = []

    def set_tokens(self, tokens: Tokens):
        self.tokens = tokens

    def parse_line(self) -> LineNode:
        chars = []
        while token := self.tokens.pop_token():
            if token.type == token_types.newline:
                break
            chars.append(token)

        if chars:
            return LineNode(chars)
        else:
            return None

    def parse_config_block(self) -> ConfigBlockNode:
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

    def parse_code_block(self) -> CodeBlockNode:
        lines = []
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

    def parse_char_block(self) -> CharBlockNode:
        chars = []
        while token := self.tokens.peek_token():
            if token.type == token_types.code_comment or token.type == token_types.config_comment:
                break
            chars.append(token)

        if chars:
            return LineNode(chars)
        else:
            return None

    def do_parse(self) -> List[AstNode]:
        root = []
        while self.tokens.peek_token():
            if node := self.parse_config_block():
                root.append(node)
            elif node := self.parse_code_block():
                root.append(node)
            elif node := self.parse_char_block():
                root.append(node)
            else:
                raise Exception("Parse error")
        return root
