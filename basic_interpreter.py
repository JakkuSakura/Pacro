from typing import List, Dict, Any, Optional
from ast_nodes import *
import basic_parser


class Config:
    pass


def code_output(*args, **kwargs):
    print(*args, **kwargs)


# noinspection PyMethodMayBeStatic
class BasicInterpreter:
    def __init__(self, config: Optional[Config] = None):
        self.config = config

    def execute_code_block(self, code_block: CodeBlockNode, config_block: Optional[ConfigBlockNode] = None):
        code = code_block.to_string()

        if not config_block or config_block['Lang'] == 'Python':
            globals_parameters: Dict[Any, Any] = {'code': code_output}
            locals_parameters: Dict[Any, Any] = {}
            exec(code, globals_parameters, locals_parameters)
        else:
            NotImplemented()

    def do_interpret(self, root: List[AstNode]):
        index_iter = iter(range(len(root)))
        for i in index_iter:
            node = root[i]
            if isinstance(node, ConfigBlockNode):
                if i < len(root):
                    next_node = root[i + 1]
                    if isinstance(next_node, CodeBlockNode):
                        next(index_iter, None)
                        self.execute_code_block(code_block=next_node, config_block=node)
                    else:
                        NotImplemented()
            elif isinstance(node, CodeBlockNode):
                self.execute_code_block(code_block=node, config_block=None)
            elif isinstance(node, TextBlockNode):
                code_output(node.to_string())
            else:
                raise Exception("Interpret error")


def main():
    interpreter = BasicInterpreter()
    root = basic_parser.main(mute=True)
    interpreter.do_interpret(root)


if __name__ == '__main__':
    main()
