from chatapp.imports import *  # noqa


class SendMessageView(AsyncAPIView):  # noqa
    permission_classes = [IsAuthenticatedCustom]  # noqa
    serializer_class = SendMessageSerializer  # noqa

    async def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        receiver_id = serializer.validated_data.get("receiver_id", None)
        receiver = User.objects.filter(uuid=receiver_id)  # noqa

        if await receiver.aexists():
            receiver = await receiver.aget()
        else:
            return CustomErrorResponse(  # noqa
                {"message": "invalid receiver id"}, status=404
            )

        if receiver == user:
            return CustomErrorResponse(  # noqa
                {"message": "user cannot send message to himself"}, status=400
            )

        chat_instance = Chat.objects.filter(  # noqa
            Q(user1=receiver, user2=user) | Q(user1=user, user2=receiver)  # noqa
        )
        if await chat_instance.aexists():
            chat_instance = await chat_instance.afirst()

        else:
            chat_instance = Chat(user1=user, user2=receiver)  # noqa
            await chat_instance.asave()

        # this is a generic asynchronous function to complete the send message
        #  process found in the chat_message file
        await messenger(  # noqa
            user=receiver, sender=user, serializer=serializer, chat=chat_instance
        )

        return CustomSuccessResponse({"message": "message sent"})  # noqa


class GetChatsView(APIView):  # noqa
    permission_classes = [IsAuthenticatedCustom]  # noqa
    serializer_class = ChatSerializer  # noqa
    model = Chat  # noqa

    def get(self, request, page_number):
        chat = self.model.objects.only("id", "user1", "user2", "created_at").filter(
            Q(user1=request.user) | Q(user2=request.user)  # noqa
        )
        return customPaginator(  # noqa
            request, self.serializer_class, chat, page_number
        )

    def post(self, request, page_number):
        serializer = GetMessagesSerializer(data=request.data)  # noqa
        serializer.is_valid(raise_exception=True)

        chat_id = serializer.validated_data["chat_id"]
        chat = self.model.objects.filter(
            Q(user1=request.user) | Q(user2=request.user), id=chat_id  # noqa
        )

        if chat.exists():
            chat = chat.get()
        else:
            return CustomErrorResponse(  # noqa
                {"message": "invalid chat id"}, status=404
            )

        messages = chat.messages.all().order_by("-created_at")
        return customPaginator(  # noqa
            request, MessageSerializer, messages, page_number  # noqa
        )
