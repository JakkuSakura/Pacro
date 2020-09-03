from typing import List, Dict, Any

from basic_parser import *


class Config:
    pass


# noinspection PyMethodMayBeStatic
class BasicInterpreter:
    def __init__(self, config: Config):
        self.config = config

    def execute_code_block(self, code_block: CodeBlockNode, config_block: Optional[ConfigBlockNode] = None):
        code = code_block.to_string()

        if not config_block or config_block['Lang'] == 'Python':
            globals_parameters: Dict[Any, Any] = {}
            locals_parameters: Dict[Any, Any] = {}
            exec(code, globals_parameters, locals_parameters)
        else:
            NotImplemented()

    def do_interpret(self, root: List[AstNode]):
        for i in range(len(root)):
            node = root[i]
            if isinstance(node, ConfigBlockNode):
                if i < len(root):
                    next_node = root[i + 1]
                    if isinstance(next_node, CodeBlockNode):
                        self.execute_code_block(code_block=next_node, config_block=node)
                    else:
                        NotImplemented()
            elif isinstance(node, CodeBlockNode):
                pass
            elif isinstance(node, TextBlockNode):
                pass
            else:
                raise Exception("Interpret error")
