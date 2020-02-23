import os
import json

from django.conf import settings


renderer = getattr(settings, 'FONTAWESOME_5_RENDERER', 'default')
path = 'icons_semantic_ui.json' if renderer == 'semantic_ui' else 'icons.json'


def get_icon_choices():

    CHOICES = [(',', '')]

    styles = {
        'brands': 'fab',
        'solid': 'fas',
        'regular': 'far',
        'light': 'fal',
    }

    with open(os.path.join(os.path.dirname(__file__), path)) as f:
        icons = json.load(f)

    for icon in icons:
        styles_len = 0
        for style in icons[icon]['styles']:
            styles_len = len(icons[icon]['styles'])
            label = icons[icon]['label']
            if styles_len > 1:
                label += " ({})".format(style)
            CHOICES.append((
                '{},{}'.format(styles[style], icon),
                label,
            ))

    return CHOICES
