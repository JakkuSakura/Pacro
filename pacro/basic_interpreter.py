from typing import List, Dict, Any, Optional
from ast_nodes import ConfigBlockNode, CodeBlockNode, TextBlockNode, AstNode
import basic_parser
import utils
import lexer_config
from output_stream import OutputStream


class Config:
    def __init__(self, args):
        self.args = args


def code_output_print(*args, **kwargs):
    if 'end' not in kwargs:
        kwargs['end'] = ''

    print(*args, **kwargs)


def code_output_file(file, *args, **kwargs):
    if 'end' not in kwargs:
        kwargs['end'] = ''

    file.write(*args, **kwargs)


# noinspection PyMethodMayBeStatic
class BasicInterpreter:
    def __init__(self, config: Optional[Config] = None):
        self.config = config
        self.code_output = code_output_print

    def set_code_output(self, code_output_fn):
        self.code_output = code_output_fn

    def execute_code_block(self, code_block: CodeBlockNode) -> OutputStream:
        code = code_block.to_string()
        config_block = code_block.config
        if not config_block or config_block['Lang'] == 'Python':
            output = OutputStream(self.code_output)
            globals_parameters: Dict[Any, Any] = {'code': output.write}
            locals_parameters: Dict[Any, Any] = {}
            exec(code, globals_parameters, locals_parameters)
            return output
        else:
            raise NotImplementedError()

    def do_interpret(self, root: List[AstNode]):
        index_iter = iter(range(len(root)))
        for i in index_iter:
            node = root[i]
            if isinstance(node, ConfigBlockNode):
                raise NotImplementedError()
            elif isinstance(node, CodeBlockNode):
                config = ''
                if node.config:
                    self.code_output(node.config.to_string(prefix=lexer_config.config_comment + ' '))
                    config = node.config.to_string()
                self.code_output(node.to_string(prefix=lexer_config.code_comment + ' '))

                code = node.to_string()
                result = node.generated_code.to_string()
                if node.generated_code.hash != utils.white_hash(config + code + result):
                    output = self.execute_code_block(node)
                    result = output.to_string()
                    self.code_output(lexer_config.generated_code_comment, 'end:',
                                     utils.white_hash(config + code + result),
                                     end='\n')
                else:
                    self.code_output(result)
                    self.code_output(lexer_config.generated_code_comment, 'end:', node.generated_code.hash,
                                     end='\n')

            elif isinstance(node, TextBlockNode):
                self.code_output(node.to_string())
            else:
                raise Exception("Interpret error " + str(node))


def main():
    interpreter = BasicInterpreter()
    root = basic_parser.main(mute=True)
    interpreter.do_interpret(root)


if __name__ == '__main__':
    main()
