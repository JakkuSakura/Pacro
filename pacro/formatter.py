import utils


class Formatter:
    def __init__(self):
        self.buf = []

    def append(self, s: str):
        self.buf.append(s)

    def format(self) -> str:
        s = ''.join(self.buf)
        return s

    def clear(self):
        self.buf.clear()


class IndentFormatter(Formatter):
    def __init__(self, indent=0, prefix=''):
        super().__init__()
        self.indent = indent
        self.prefix = prefix

    def format(self):
        block = ''.join(self.buf)
        lines = block.split('\n')
        return utils.lines_to_string(lines, indent=self.indent, prefix=self.prefix)
