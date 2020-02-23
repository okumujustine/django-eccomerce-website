from __future__ import absolute_import

from django import forms

from .app_settings import get_css_admin
from .utils import get_icon_choices


css_admin = get_css_admin()
CHOICES = get_icon_choices()


class IconWidget(forms.Select):
    template_name = 'fontawesome_5/select.html'

    def __init__(self, attrs=None):
        super(IconWidget, self).__init__(attrs, choices=CHOICES)

    class Media:

        js = (
            'fontawesome_5/js/django-fontawesome.js',
        )

        css = {
            'all': css_admin
        }
