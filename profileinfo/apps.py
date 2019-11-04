from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ProfileinfoConfig(AppConfig):
    name = 'profileinfo'
    verbose_name = _('profileinfos')

    def ready(self):
        import profileinfo.signals