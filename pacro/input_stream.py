import sys


class InputStream:
    def read(self) -> str:
        pass

    def close(self):
        pass

    def __str__(self):
        return 'InputStream'


class FileInputStream(InputStream):
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'r')

    def read(self) -> str:
        return self.file.read()

    def close(self):
        self.file.close()

    def __str__(self):
        return f'FileInputStream(file={self.filename})'


class StdinStream(InputStream):
    def read(self) -> str:
        return sys.stdin.read()

    def close(self):
        sys.stdin.close()

    def __str__(self):
        return 'StdinStream'
