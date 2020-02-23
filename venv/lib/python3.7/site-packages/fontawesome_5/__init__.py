from .app_settings import get_icon_renderer

renderer = get_icon_renderer()

class Icon:

    def as_html(self, **kwargs):
        return renderer().render(self)

    def __str__(self):
        return "{},{}".format(self.style_prefix, self.name)

    def __init__(self, name, style_prefix='fas', **kwargs):

        self.name = name
        self.style_prefix = style_prefix
        self.kwargs = kwargs
