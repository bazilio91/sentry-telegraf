# coding: utf-8
import logging

from django import forms
from django.utils.translation import ugettext_lazy as _
from sentry.constants import STATUS_UNRESOLVED
from sentry.models.activity import Activity

from sentry.plugins.bases import notify
from telegraf import TelegrafClient

from datetime import timedelta
from django.utils import timezone

from . import __version__, __doc__ as package_doc


class TelegrafOptionsForm(notify.NotificationConfigurationForm):
    host = forms.CharField(
        label=_('Host'),
        widget=forms.TextInput(attrs={'placeholder': '127.0.0.1'}),
    )
    port = forms.CharField(
        label=_('Port'),
        widget=forms.TextInput(attrs={'port': '8094'}),
    )


class TelegrafPlugin(notify.NotificationPlugin):
    title = 'Telegraf stats'
    slug = 'sentry_telegraf'
    description = package_doc
    version = __version__
    author = 'Vasiliy Ostanin'
    author_url = 'https://github.com/bazilio91/sentry-telegraf'
    resource_links = [
        ('Bug Tracker', 'https://github.com/bazilio91/sentry-telegraf/issues'),
        ('Source', 'https://github.com/bazilio91/sentry-telegraf'),
    ]

    conf_key = 'sentry_telegraf'
    conf_title = title

    project_conf_form = TelegrafOptionsForm

    logger = logging.getLogger('sentry.plugins.sentry_telegraf')

    def is_configured(self, project, **kwargs):

        return bool(self.get_option('host', project) and self.get_option('port', project))

    def get_config(self, project, **kwargs):
        return [
            {
                'name': 'host',
                'label': 'Host',
                'type': 'text',
                'placeholder': '127.0.0.1',
                'validators': [],
                'required': True,
            },
            {
                'name': 'port',
                'label': 'Port',
                'placeholder': '8094',
                'type': 'text',
                'validators': [],
                'required': True,
            },
        ]

    def post_process(self, group, event, is_new, is_sample, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        host = self.get_option('host', group.project)
        port = int(self.get_option('port', group.project))

        resolve_age = group.project.get_option('sentry:resolve_age', None)

        client = TelegrafClient(host=host, port=port)

        template = 'sentry.error'

        groups = group.project.group_set.filter(status=STATUS_UNRESOLVED)

        if resolve_age:
            oldest = timezone.now() - timedelta(hours=int(resolve_age))
            groups = groups.filter(last_seen__gt=oldest)

        num_errors = groups.filter(level=group.level).count()

        self.logger.info('will send %s:%s=%s to telegraf', template, group.project, num_errors)

        tags = {'project': group.project.slug}
        tags.update(event.tags)

        client.metric(template, num_errors, tags=tags)

    def notify_users(self, *args, **kwargs):
        pass

    def notify_about_activity(self, activity):
        if activity.type not in (Activity.SET_RESOLVED, Activity.SET_UNRESOLVED):
            return

        self.logger.info('got activity type %s for group %s', activity.type, activity.group)
        self.post_process(group=activity.group, event=None, is_new=False, is_sample=False)
