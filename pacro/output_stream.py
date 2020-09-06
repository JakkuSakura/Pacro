import sys

from formatter import Formatter


class OutputStream:
    def __init__(self, write_and_flush_func):
        assert not isinstance(write_and_flush_func, str)
        self.write_func = write_and_flush_func
        self.formatter = Formatter()
        self.buf = []

    def set_formatter(self, formatter: Formatter):
        self.buf.append(self.formatter.format())
        self.formatter = formatter

    def write(self, data: str):
        self.formatter.append(data)

    def to_string(self) -> str:
        return ''.join(self.buf) + self.formatter.format()

    def flush(self):
        self.write_func(self.to_string())
        self.buf.clear()


class BufferedOutputStream(OutputStream):
    def __init__(self, upper_stream):
        super().__init__(upper_stream.write)


class FileOutputStream(OutputStream):
    def __init__(self, filename):
        super().__init__(self.file_flush)
        self.filename = filename

    def file_flush(self, s):
        file = open(self.filename, 'w')
        file.write(s)
        file.close()


class StdoutStream(OutputStream):
    def __init__(self):
        super().__init__(sys.stdout.write)
