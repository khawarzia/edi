from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class LoginConfig(AppConfig):
    name = 'login'
    verbose_name = _('information')

    def ready(self):
        import login.signals 