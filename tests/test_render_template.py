from jinja2 import Template
from pacro.templating.parser import FileParser
from pacro.templating.render_template import TemplateEngine


def test_file_parser():
    parser = FileParser()
    parsed = parser.parse_file("""\
// @blackmagic(i32)
fn main() {
    let foo = 0;
    foo.black_magic();
}
""")
    print(parsed)
    return parsed


def black_magic(ty):
    return Template("""\
{% for name in names %}
fn get_{{ name }}(val: {{ ty }}) -> &str {
    "{{ name }}"
}
{% endfor %}
""").render(ty=ty, names=['1', '2', '3'])


def test_render_template():
    code = test_file_parser()
    data = {
        'i32': 'i32',
        'blackmagic': black_magic
    }
    rendered = TemplateEngine().render_template(code, data)
    print(rendered)
