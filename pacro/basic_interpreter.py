from typing import List, Dict, Any, Optional
from ast_nodes import ConfigBlockNode, CodeBlockNode, TextBlockNode, AstNode
import basic_parser
import utils
import lexer_config
from formatter import IndentFormatter, Formatter
from output_stream import OutputStream, StdoutStream, BufferedOutputStream


class Config:
    def __init__(self, args):
        self.args = args


# noinspection PyMethodMayBeStatic
class BasicInterpreter:
    def __init__(self, config: Optional[Config] = None):
        self.config = config
        self.output: OutputStream = StdoutStream()

    def set_code_output(self, code_output):
        self.output = code_output

    def execute_code_block(self, code_block: CodeBlockNode, output_stream: OutputStream):
        code = code_block.to_string()
        config_block = code_block.config
        if not config_block or config_block['Lang'] == 'Python':
            globals_parameters: Dict[Any, Any] = {'code': output_stream.write}
            locals_parameters: Dict[Any, Any] = {}
            exec(code, globals_parameters, locals_parameters)
        else:
            raise NotImplementedError()

    def do_interpret(self, root: List[AstNode]):
        for node in root:
            self.output.set_formatter(Formatter())
            if isinstance(node, ConfigBlockNode):
                raise NotImplementedError()
            elif isinstance(node, CodeBlockNode):
                indent = node.indent
                config = ''
                if node.config:
                    self.output.write(node.config.to_string(indent=indent, prefix=lexer_config.config_comment + ' '))
                    config = node.config.to_string()

                self.output.write(node.to_string(indent=indent, prefix=lexer_config.code_comment + ' '))

                code = node.to_string()
                result = node.generated_code.to_string() if node.generated_code else ''
                if not node.generated_code or node.generated_code.hash != utils.white_hash(config + code + result):
                    output_stream = BufferedOutputStream(self.output)
                    output_stream.set_formatter(IndentFormatter(indent=indent))
                    self.execute_code_block(node, output_stream)
                    result = output_stream.to_string()
                    output_stream.flush()

                    self.output.set_formatter(
                        IndentFormatter(prefix=lexer_config.generated_code_comment + ' ',
                                        indent=indent))

                    self.output.write('end: ' + utils.white_hash(config + code + result) + '\n')
                else:
                    self.output.set_formatter(IndentFormatter(indent=indent))
                    self.output.write(result)

                    self.output.set_formatter(
                        IndentFormatter(prefix=lexer_config.generated_code_comment + ' ',
                                        indent=indent))
                    self.output.write('end: ' + node.generated_code.hash + '\n')

            elif isinstance(node, TextBlockNode):
                self.output.set_formatter(Formatter())
                self.output.write(node.to_string())
            else:
                raise Exception("Interpret error " + str(node))
        self.output.flush()


def main():
    interpreter = BasicInterpreter()
    root = basic_parser.main(mute=True)
    interpreter.do_interpret(root)


if __name__ == '__main__':
    main()
