import json


async def serialize_json(self, text_data, callback=None):
    message_processed = False
    try:
        message_data = json.loads(text_data)
        message_processed = True
    except Exception:
        await self.send(
            text_data=json.dumps(
                {"type": "error", "message": "data should be of type json"}
            )
        )

    if message_processed:
        if type(message_data) != dict:
            await self.send(
                text_data=json.dumps(
                    {"type": "error", "message": "data should be of type json"}
                )
            )

        else:
            data_keys = list(message_data.keys())

            if callback is not None:
                callbackResponse = await callback(data_keys)

                if callbackResponse is not None:
                    await self.send(text_data=json.dumps(callbackResponse))

                else:
                    message_data.pop("type", None)

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {"type": "notification"} | message_data,
                    )

            else:
                message_data.pop("type", None)

                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "notification"} | message_data
                )
