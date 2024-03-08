from accounts.models import User, Jwt
from accounts.responses import CustomSuccessResponse, CustomErrorResponse
from rest_framework.views import APIView
from accounts.serializers import LoginSerializer
from common.custom_functions import get_access_token, get_refresh_token
from django.contrib.auth import authenticate


class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        user =  User.objects.filter(email =  serializer.validated_data["email"])

        if not user.exists():
            return CustomErrorResponse({"message":"User with that email does not exist!"}, status=404)
      
        user = authenticate(request, email = serializer.validated_data["email"], password = serializer.validated_data["password"])
        if user is None:
            return CustomErrorResponse({"message":"Invalid details!"}, status=400)
        
        access = get_access_token({"user_id": str(user.uuid)})
        refresh = get_refresh_token()

        Jwt.objects.create(user = user, access = access, refresh = refresh)
        return CustomSuccessResponse({"access":access, "refresh":refresh})
    