class Token:
    def __init__(self, *args, **kwargs):
        self.row = kwargs['row']
        self.col = kwargs['col']
        self.type = kwargs['type']
        self.content = kwargs['content']

    def __str__(self):
        content = self.content.encode('unicode_escape').decode('utf-8')
        return f'Token({self.row},{self.col},{self.type},"{content}")'
