from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pizzami.orders'

    def ready(self):
        from config import scheduler
        from pizzami.orders.tasks import update_discount_status
        scheduler.start(task=update_discount_status)
