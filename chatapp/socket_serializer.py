import json


async def serialize_json(self, text_data):
    """
    this is to ensure that the data coming in is in json format
    it ensures that the data coming in has the "data" property
    """
    try:
        message_data = json.loads(text_data)
        message_processed = True

    except Exception:
        await self.send(
            text_data=json.dumps(
                {"type": "error", "message": "data should be of type json"}
            )
        )
        message_processed = False

    if message_processed:
        if type(message_data) == dict:
            await self.send(
                text_data=json.dumps(
                    {"type": "error", "message": "data should be of type json"}
                )
            )

        else:
            data_keys = list(message_data.keys())

            notification_data = {}
            for key in data_keys:
                if key != "type":
                    notification_data[key] = message_data[key]

            await self.channel_layer.group_send(
                self.room_group_name, {"type": "notification"} | notification_data
            )
