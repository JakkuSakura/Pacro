from typing import Optional, Any


class Buffer:
    def __init__(self, buf: str):
        self.buf = buf
        self.ptr = 0

    def peek_char(self) -> Optional[str]:
        if self.ptr >= len(self.buf):
            return None
        return self.buf[self.ptr]

    def pop_char(self) -> Optional[str]:
        if char := self.peek_char():
            self.ptr += 1
            return char

        return None

    def match(self, pat: Any) -> Optional[str]:
        if isinstance(pat, list):
            for p in pat:
                if m := self.match(p):
                    return m
            return None
        else:
            assert isinstance(pat, str)

            if self.ptr + len(pat) >= len(self.buf):
                return None
            s = self.buf[self.ptr:self.ptr + len(pat)]
            if s == pat:
                return s

        return None

    def match_forward(self, pat: Any) -> Optional[str]:
        if s := self.match(pat):
            self.ptr += len(s)
            return s

        return None
