from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class SignupAPIView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email", "")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        if len(password) < 6:
            return Response({"error": "Password must be at least 6 characters."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "That username is already taken."}, status=400)

        if email and User.objects.filter(email=email).exists():
            return Response({"error": "That email is already registered. Try logging in instead."}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        token = Token.objects.create(user=user)

        return Response({
            "token": token.key,
            "username": user.username,
        })


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=400)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "username": user.username,
        })
        
        
      