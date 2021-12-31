from typing import Any
import sys

from .parser import FileParser
from .render_template import TemplateEngine


def filter_builtins(d: dict[str, Any]):
    to_remove = []
    for key, val in d.items():
        if key.startswith('_'):
            to_remove.append(key)
    for rm in to_remove:
        del d[rm]


def main():
    source_file = sys.argv[1]
    source = open(source_file).read()
    env_file = sys.argv[2]
    globals_dict = {}
    locals_dict = {}
    exec(open(env_file).read(), globals_dict, locals_dict)
    filter_builtins(locals_dict)
    parsed = FileParser().parse_file(source)
    rendered = TemplateEngine().render_template(parsed, **locals_dict)
    print(rendered)


if __name__ == '__main__':
    main()
