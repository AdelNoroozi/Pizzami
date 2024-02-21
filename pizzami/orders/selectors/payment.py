from pizzami.orders.models import Payment


def create_payment(data: dict):
    Payment.objects.create(order=data["order"], is_income=data["is_income"], tracking_code=data["tracking_code"],
                           payment_data=data["payment_data"])
