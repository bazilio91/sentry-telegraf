from __future__ import absolute_import
from django.conf import settings

__version__ = '0.0.1'

if settings.configured:
    from sentry.plugins import plugins, register
    from sentry_telegraf.plugin import TelegrafPlugin

    if TelegrafPlugin.slug not in [plugin.slug for plugin in plugins.all()]:
        register(TelegrafPlugin)
