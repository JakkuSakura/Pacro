from typing import List, Optional

import utils
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

    def to_string(self, end_of_line='\n') -> str:
        s = []
        for c in self.chars:
            s.append(c.content)

        s.append(end_of_line)
        return ''.join(s)

    def __str__(self):
        return 'LineNode(' + self.to_string() + ')'


class ConfigBlockNode(AstNode):
    def __init__(self, lines: List[LineNode]):
        super().__init__()
        self.lines = lines
        trim_left(self.lines)
        self.config = {}
        for line in lines:
            key, value = line.to_string().split(':')
            self.config[key.strip()] = value.strip()

    def to_string(self, *args, **kwargs) -> str:
        return lines_to_string(self.lines, *args, **kwargs)

    def __str__(self):
        return 'ConfigBlockNode' + str(self.config)

    def __getitem__(self, item):
        return self.config[item]

    def __setitem__(self, key, value):
        self.config[key] = value


class GeneratedCodeNode(AstNode):
    def __init__(self, lines: List[LineNode], comment: Optional[LineNode]):
        super().__init__()
        self.lines = lines
        trim_left(self.lines)
        try:
            self.hash = comment.to_string().split(':')[1].strip()
        except:
            self.hash = None

    def to_string(self, *args, **kwargs):
        return lines_to_string(self.lines, *args, **kwargs)

    def __str__(self):
        return 'GeneratedCodeNode{' + self.to_string() + '}'


def trim_left(lines: List[LineNode]):
    indent = 1e5
    for line in lines:
        indent = min(indent, count_intent(line.to_string()))

    for line in lines:
        line.chars = line.chars[indent:]


def lines_to_string(lines: List[LineNode], prefix='', indent='', end_of_line='\n'):
    buf = []
    for line in lines:
        if isinstance(indent, str):
            buf.append(indent)
        elif isinstance(indent, int):
            buf.append(' ' * indent)
        else:
            buf.append(str(indent))

        buf.append(prefix)
        buf.append(line.to_string(end_of_line))

    return ''.join(buf)


class CodeBlockNode(AstNode):
    def __init__(self, config: Optional[ConfigBlockNode], lines: List[LineNode],
                 generated_code: Optional[GeneratedCodeNode]):
        super().__init__()
        self.config = config
        self.lines = lines
        trim_left(self.lines)
        self.generated_code = generated_code

    def to_string(self, *args, **kwargs):
        return lines_to_string(self.lines, *args, **kwargs)

    def __str__(self):
        return 'TextBlockNode(' + self.to_string() + ')'


class TextBlockNode(AstNode):
    def __init__(self, lines: List[LineNode]):
        super().__init__()
        self.lines = lines

    def to_string(self):
        return lines_to_string(self.lines)

    def __str__(self):
        return 'TextBlockNode(' + self.to_string() + ')'
