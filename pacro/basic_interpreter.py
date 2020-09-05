from typing import List, Dict, Any, Optional
from ast_nodes import ConfigBlockNode, CodeBlockNode, TextBlockNode, AstNode
import basic_parser


class Config:
    pass


def code_output_print(*args, **kwargs):
    print(*args, **kwargs)


def code_output_file(file, *args, **kwargs):
    file.write(*args, **kwargs)
    file.write('\n')


# noinspection PyMethodMayBeStatic
class BasicInterpreter:
    def __init__(self, config: Optional[Config] = None):
        self.config = config
        self.code_output = code_output_print

    def set_code_output(self, code_output_fn):
        self.code_output = code_output_fn

    def execute_code_block(self, code_block: CodeBlockNode):
        code = code_block.to_string()
        config_block = code_block.config
        if not config_block or config_block['Lang'] == 'Python':
            globals_parameters: Dict[Any, Any] = {'code': self.code_output}
            locals_parameters: Dict[Any, Any] = {}
            exec(code, globals_parameters, locals_parameters)
        else:
            raise NotImplementedError()

    def do_interpret(self, root: List[AstNode]):
        index_iter = iter(range(len(root)))
        for i in index_iter:
            node = root[i]
            if isinstance(node, ConfigBlockNode):
                raise NotImplementedError()
            elif isinstance(node, CodeBlockNode):
                self.execute_code_block(node)
            elif isinstance(node, TextBlockNode):
                code_output_print(node.to_string())
            else:
                raise Exception("Interpret error " + str(node))


def main():
    interpreter = BasicInterpreter()
    root = basic_parser.main(mute=True)
    interpreter.do_interpret(root)


if __name__ == '__main__':
    main()
