def blackmagic(ty):
    from jinja2 import Template

    return Template("""\
{% for name in names %}
fn get_{{ name }}(val: {{ ty }}) -> &str {
    "{{ name }}"
}
{% endfor %}
""").render(ty=ty, names=['1', '2', '3'])
