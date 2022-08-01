from datetime import datetime
from background_task import background
from Library_system.models import Order


@background(schedule=600)
def delete_reservation():
    all_orders = Order.objects.all
    for order in all_orders:
        if order.action_end_time < datetime.now() and order.type == 2:
            order.delete()
