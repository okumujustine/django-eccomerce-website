from __future__ import unicode_literals

from django import template
from django.templatetags.static import static
from django.utils.html import format_html, mark_safe, conditional_escape

from .. import Icon
from ..app_settings import get_css


css = get_css()
register = template.Library()


@register.simple_tag
def fa5_icon(*args, **kwargs):
    return Icon(*args, **kwargs).as_html()


@register.simple_tag
def fontawesome_5_static():
    staticfiles = []

    for stylesheet in css:
        staticfiles.append(format_html(
            '<link href="{}" rel="stylesheet" media="all">', stylesheet))

    staticfiles.append(format_html(
        '<script type="text/javascript" src="{}"></script>', static('fontawesome_5/js/django-fontawesome.js')
    ))

    return mark_safe(conditional_escape('\n').join(staticfiles))
