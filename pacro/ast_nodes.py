from typing import List, Optional

from lexer_token import Token
from utils import count_intent


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


class CodeBlockNode(AstNode):
    def __init__(self, config: Optional[ConfigBlockNode], lines: List[LineNode]):
        super().__init__()
        self.config = config
        self.lines = lines
        self.trim_left()

    def trim_left(self):
        indent = 1e5
        for line in self.lines:
            indent = min(indent, count_intent(line.get_string()))

        for line in self.lines:
            line.chars = line.chars[indent:]

    def to_string(self, newline='\n'):
        return newline.join([x.get_string() for x in self.lines]) + newline

    def __str__(self):
        return 'TextBlockNode(' + self.to_string() + ')'


class TextBlockNode(AstNode):
    def __init__(self, lines: List[LineNode]):
        super().__init__()
        self.lines = lines

    def to_string(self, newline='\n'):
        return newline.join([x.get_string() for x in self.lines]) + newline

    def __str__(self):
        return 'TextBlockNode(' + self.to_string() + ')'
