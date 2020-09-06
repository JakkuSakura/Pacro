class OutputStream:
    def __init__(self, write_func):
        self.buf = []
        self.write_func = write_func

    def write(self, data: str):
        self.buf.append(data)
        self.write_func(data)

    def to_string(self):
        return ''.join(self.buf)
