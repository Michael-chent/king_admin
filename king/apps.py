from django.apps import AppConfig


class KingConfig(AppConfig):
    name = 'king'

    def ready(self):
        super(KingConfig,self).ready()
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('kg')




