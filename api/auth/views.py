from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password

class LoginUser(APIView):
    @swagger_auto_schema(
            operation_summary="Login User",
    )
    def post(self, request):
        return Response("success")