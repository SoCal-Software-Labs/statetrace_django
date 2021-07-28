from django.apps import AppConfig


from django.apps import AppConfig
from django.db.models.signals import post_migrate


def my_callback(sender, **kwargs):
    from .models import Annotation

    Annotation.log_migration()


class StatetraceConfig(AppConfig):
    name = 'statetrace_django'
    
    def ready(self):
        post_migrate.connect(my_callback, sender=self)


        