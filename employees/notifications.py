from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def broadcast(message):
    async_to_sync(get_channel_layer().group_send)(
        "employees", {"type": "employee_event", "message": message}
    )