from channels.generic.websocket import AsyncJsonWebsocketConsumer

class EmployeeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return
        await self.channel_layer.group_add("employees", self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard("employees", self.channel_name)

    async def employee_event(self, event):
        await self.send_json({"message": event["message"]})