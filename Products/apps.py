from django.apps import AppConfig
import threading
import time


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Products'

    def ready(self):
        from .tasks import start_background_task
        start_background_task()
