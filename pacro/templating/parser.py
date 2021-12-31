from typedmodel import BaseModel


class FileParser(BaseModel):
    comment: str = "// @"
    post_comment: str = "// -"

    def parse_file(self, file_content: str) -> str:
        lines = file_content.splitlines()
        for i in range(len(lines)):
            line = lines[i]
            stripped = line.lstrip()
            leading_spaces = len(line) - len(stripped)
            if stripped.startswith(self.comment):
                content = stripped[len(self.comment):]
                lines[i] = '\n'.join([
                    ' ' * leading_spaces + '// begin ' + content,
                    ' ' * leading_spaces + '{{ ' + content + ' }}',
                    ' ' * leading_spaces + '// end ' + content,
                ])
        return '\n'.join(lines)
