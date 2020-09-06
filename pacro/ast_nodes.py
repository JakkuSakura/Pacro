from typing import List, Optional, Union

import utils
from lexer_token import Token
from utils import count_indent


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


def trim_left(lines: List[LineNode]):
    indent = int(1e5)
    for line in lines:
        s = line.to_string()
        if s.strip():
            indent = min(indent, count_indent(line.to_string()))

    for line in lines:
        line.chars = line.chars[indent:]


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
        return utils.lines_to_string(self.lines, *args, **kwargs)

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
        self.hash = None
        try:
            if comment:
                line = comment.to_string()
                if line:
                    self.hash = line.split(':')[1].strip()
        except:
            pass

    def to_string(self, *args, **kwargs):
        return utils.lines_to_string(self.lines, *args, **kwargs)

    def __str__(self):
        return 'GeneratedCodeNode{' + self.to_string() + '}'


class CodeBlockNode(AstNode):
    def __init__(self, config: Optional[ConfigBlockNode], lines: List[LineNode],
                 generated_code: Optional[GeneratedCodeNode], indent):
        super().__init__()
        self.config = config
        self.lines = lines
        self.indent = indent
        trim_left(self.lines)
        self.generated_code = generated_code

    def to_string(self, *args, **kwargs):
        return utils.lines_to_string(self.lines, *args, **kwargs)

    def __str__(self):
        return 'CodeBlockNode(' + self.to_string() + ')'


class TextBlockNode(AstNode):
    def __init__(self, lines: List[LineNode]):
        super().__init__()
        self.lines = lines

    def to_string(self):
        return utils.lines_to_string(self.lines)

    def __str__(self):
        return 'TextBlockNode(' + self.to_string() + ')'
