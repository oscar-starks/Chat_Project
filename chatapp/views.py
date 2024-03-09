from chatapp.imports import *

class SendMessageView(AsyncAPIView):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = MessageSerializer

    @swagger_auto_schema(request_body=serializer_class)
    async def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        receiver_id = serializer.validated_data.get("receiver_id", None)
        receiver = User.objects.filter(uuid=receiver_id)

        if await receiver.aexists():
            receiver = await receiver.aget()
        else:
            return CustomErrorResponse({'message':"invalid receiver id"},status=404)

        if receiver == user:
            return CustomErrorResponse({"message": "user cannot send message to himself"},status=400)

        chat_instance = Chat.objects.filter(Q(user1 = receiver, user2=user)|Q(user1 = user, user2 = receiver))
        if await chat_instance.aexists():
            chat_instance = await chat_instance.afirst()
        
        else:
            chat_instance = Chat(user1=user, user2=receiver)
            await chat_instance.asave()

        # this is a generic asynchronous function to complete the send message
        #  process found in the chat_message file
        await messenger(
                user = receiver, 
                serializer=serializer,
                chat=chat_instance
                )
        
        return CustomSuccessResponse({"message": "message sent"})


class GetChatsView(APIView):
    permission_classes = [IsAuthenticatedCustom]
    serializer_class = ChatSerializer
    model = Chat

    def get(self, request, page_number):
        chat = self.model.objects.only("id", "user1", "user2", "created_at").filter(Q(user1=request.user)|Q(user2=request.user))
        return customPaginator(request, self.serializer_class, chat, page_number)

    
    def post(self, request, page_number):
        serializer = GetMessagesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chat_id = serializer.validated_data["chat_id"]
        chat = self.model.objects.filter(Q(user1=request.user)|Q(user2=request.user),id = chat_id)

        if chat.exists():
            chat = chat.get()
        else:
            return CustomErrorResponse({"message":"invalid chat id"}, status=404)
        
        messages = chat.messages.all()
        return customPaginator(request, MessageSerializer, messages, page_number)

        

    

