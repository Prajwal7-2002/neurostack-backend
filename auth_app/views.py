from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import SignupSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "User created successfully"}, status=201)


class ResetPasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        user = request.user

        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password updated successfully"}, status=200)
