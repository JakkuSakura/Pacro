from typedmodel.models import *
from jinja2 import Template, StrictUndefined


class TemplateEngine(BaseModel):
    def render_template(self, template: str, *args, **kwargs):
        return Template(template).render(*args, **kwargs, undefined=StrictUndefined)

