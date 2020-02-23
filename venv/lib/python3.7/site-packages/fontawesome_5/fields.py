from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext as _

from . import Icon
from .app_settings import get_prefix
from .forms import IconFormField
from .shims import shims


prefix = get_prefix()


class IconField(models.Field):
    description = _('A fontawesome icon field')

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 60
        kwargs['blank'] = True
        super(IconField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    @staticmethod
    def from_db_value(value, expression, connection, *args, **kwargs):
        if value is None:
            return value
        if not ',' in value:
            value = shims.get(value, None)
        if value is None:
            return value
        values = value.split(',')
        return Icon(name=values[1], style_prefix=values[0], prefix=prefix)

    def to_python(self, value):
        if isinstance(value, Icon):
            return value
        if value is None:
            return value
        if not ',' in value:
            value = shims.get(value, None)
        if not value or value == 'None':
            return None
        values = value.split(',')
        return Icon(name=values[1], style_prefix=values[0], prefix=prefix)

    def get_prep_value(self, value):
        return str(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': IconFormField,
        }

        defaults.update(kwargs)
        return super(IconField, self).formfield(**defaults)
