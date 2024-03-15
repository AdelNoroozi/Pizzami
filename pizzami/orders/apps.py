from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pizzami.orders'

    def ready(self):
        from pizzami.core import scheduler
        from pizzami.orders.tasks import update_discount_status, delete_dead_orders
        scheduler.start(task=update_discount_status, interval=30)
        scheduler.start(task=delete_dead_orders, interval=1800)
