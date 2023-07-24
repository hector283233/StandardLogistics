from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Q

from user.models import (User, Profile, BusinessAccount, 
                         BA_Attribute_Value, BA_Attribute)
from .serializers import *
from GlobalVariables import *
from api.utils import *

class LoginUser(APIView):
    """
    Authenticating user with email, mobile or username and password.
    Returns refresh, access tokens and user info.
    """
    @swagger_auto_schema(
        operation_summary="Login User",
        operation_description="***IMPORTANT*** For autherize user needed ONE AND ONLY ONE OF 'email' or 'mobile' or 'username'. Sending more will conflict the  \n'password' field is required too.",
        request_body=LoginInSerializer,
        responses={200: openapi.Response(
            description="Response Exapmle",
            examples={
                "application/json": {
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MjA5MzI4MSwiaWF0IjoxNjg5NTAxMjgxLCJqdGkiOiI4MzczMDQyZmQ0MzQ0YTE1OTViMDdiNWIyYTExYzgwZiIsInVzZXJfaWQiOjF9.RJ8WZoR1sTgfy93-39JyhT-PFvFDDNvmXnN9A7hx0b8",
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxMDM3MjgxLCJpYXQiOjE2ODk1MDEyODEsImp0aSI6ImMwNTZmNzFjMjAzNTQ1Y2ZiNmM2NmU2NGFiNWIwODMxIiwidXNlcl9pZCI6MX0.v-y0GWossKTR-gTpCogIq9Qck-GLN8Wid1R7fnI2RaA",
                    "user": {
                        "id": 1,
                        "username": "admin",
                        "groups": [{"name": "VIP"}, {"name": "Business"}]
                    }
                }
            }
        )},
    )
    def post(self, request):
        try:
            data = request.data
            if 'password' in data:
                if data['password'] == None or data['password'] == "":
                    return Response({
                        "response":"error",
                        "message": MSG_NO_PASSWORD,
                        }, status=status.HTTP_400_BAD_REQUEST)
                if 'username' not in data and 'mobile' not in data and 'email' not in data:
                    return Response({
                        'response': "error", 
                        "message": MSG_NO_USER_INFO,
                        }, status=status.HTTP_400_BAD_REQUEST)
                password = data['password']
                current_user = None
                if 'username' in data:
                    if data['username'] != None and data['username'] != "":
                        _user = User.objects.filter(username=data["username"]).first()
                        if _user:
                            current_user = _user
                if 'mobile' in data:
                    if data['mobile'] != None and data["mobile"] != "":
                        _user = User.objects.filter(mobile=data["mobile"]).first()
                        if _user:
                            current_user = _user
                if 'email'  in data:
                    if data["email"] != None and data["email"] != "":
                        _user = User.objects.filter(email=data["email"]).first()
                        if _user:
                            current_user = _user
                if current_user is None:
                    return Response({
                        "response": "error",
                        "message": MSG_USER_NOT_FOUND,
                        "data": {},
                    }, status=status.HTTP_404_NOT_FOUND)
                user = authenticate(username=current_user.username, password=password)
                if user is None:
                    return Response({
                        "response": "error",
                        "message": MSG_USERNAME_OR_PASSWORD_ERROR,
                        "data": {},
                    }, status=status.HTTP_404_NOT_FOUND)
                serializer = LoginOutSerializer(user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'response': "success",
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': serializer.data
                })
            else:
                return Response({
                    "response": "error",
                    "message": MSG_NO_PASSWORD,
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "response": "error", 
                "message": MSG_UNKNOWN_ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)
        
class RegisterUser(APIView):
    """
    Register user with email, mobile or username and password.
    Returns refresh, access tokens and user info.
    """
    @swagger_auto_schema(
        request_body=RegisterInSerializer,
        operation_summary="Register User",
        operation_description="",
        responses={200: openapi.Response(
            description="Response Exapmle",
            examples={
                "application/json": {
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MjA5MzI4MSwiaWF0IjoxNjg5NTAxMjgxLCJqdGkiOiI4MzczMDQyZmQ0MzQ0YTE1OTViMDdiNWIyYTExYzgwZiIsInVzZXJfaWQiOjF9.RJ8WZoR1sTgfy93-39JyhT-PFvFDDNvmXnN9A7hx0b8",
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxMDM3MjgxLCJpYXQiOjE2ODk1MDEyODEsImp0aSI6ImMwNTZmNzFjMjAzNTQ1Y2ZiNmM2NmU2NGFiNWIwODMxIiwidXNlcl9pZCI6MX0.v-y0GWossKTR-gTpCogIq9Qck-GLN8Wid1R7fnI2RaA",
                    "user": {
                        "id": 1,
                        "username": "admin",
                        "groups": [{"name": "VIP"}, {"name": "Business"}]
                    }
                }
            }
        )},
    )
    def post(self, request):
        try:
            data = request.data
            if 'password' in data:
                if data['password'] == None or data['password'] == "":
                    return Response({
                        "response":"error",
                        "message": MSG_NO_PASSWORD,
                        }, status=status.HTTP_400_BAD_REQUEST)
                if 'username' not in data and 'mobile' not in data and 'email' not in data:
                    return Response({
                        'response': "error", 
                        "message": MSG_NO_USER_INFO,
                        }, status=status.HTTP_400_BAD_REQUEST)
                password = data['password']
                current_user = None
                if 'mobile' in data:
                    if data['mobile'] != None and data["mobile"] != "":
                        _user = User.objects.filter(mobile=data["mobile"]).first()
                        if _user:
                            current_user = _user
                if 'email'  in data:
                    if data["email"] != None and data["email"] != "":
                        _user = User.objects.filter(email=data["email"]).first()
                        if _user:
                            current_user = _user
                if current_user:
                    return Response({
                        "response": "error",
                        "message": MSG_USER_ALREADY_EXISTS
                        }, status=status.HTTP_400_BAD_REQUEST)
                
                if 'mobile' in data:
                    if data['mobile'] != None and data["mobile"] != "":
                        user = User.objects.create(
                            mobile=data['mobile'], 
                            password=make_password(password)
                        )
                        serializer = LoginOutSerializer(user)
                        refresh = RefreshToken.for_user(user)
                        return Response({
                            "response":"success",
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'user': serializer.data
                            })
                    else:
                        return Response({
                            "response":"error",
                            "message": MSG_MOBILE_EMPTY
                            }, status=status.HTTP_400_BAD_REQUEST)
                if 'email' in data:
                    if data['email'] != None and data["email"] != "":
                        user = User.objects.create(
                            mobile=data['email'], 
                            password=make_password(password)
                        )
                        serializer = LoginOutSerializer(user)
                        refresh = RefreshToken.for_user(user)
                        return Response({
                            "response":"success",
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'user': serializer.data
                            })
                    else:
                        return Response({
                            "response":"error",
                            "message": MSG_EMAIL_EMPTY
                            }, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({
                    "response": "error",
                    "message": MSG_NO_PASSWORD,
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "response": "error", 
                "message": MSG_UNKNOWN_ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)    

class ChangePassword(APIView):
    """
    Change password providing 'old_password' and 'new_password'.
    Returns refresh, access tokens and user info.
    """
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        operation_summary="Change Password",
        operation_description="Need to authorize with Bearer token.",
        responses={200: openapi.Response(
            description="Response Exapmle",
            examples={
                "application/json": {
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MjA5MzI4MSwiaWF0IjoxNjg5NTAxMjgxLCJqdGkiOiI4MzczMDQyZmQ0MzQ0YTE1OTViMDdiNWIyYTExYzgwZiIsInVzZXJfaWQiOjF9.RJ8WZoR1sTgfy93-39JyhT-PFvFDDNvmXnN9A7hx0b8",
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxMDM3MjgxLCJpYXQiOjE2ODk1MDEyODEsImp0aSI6ImMwNTZmNzFjMjAzNTQ1Y2ZiNmM2NmU2NGFiNWIwODMxIiwidXNlcl9pZCI6MX0.v-y0GWossKTR-gTpCogIq9Qck-GLN8Wid1R7fnI2RaA",
                    "user": {
                        "id": 1,
                        "username": "admin",
                        "groups": [{"name": "VIP"}, {"name": "Business"}]
                    }
                }
            }
        )},
    )
    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data)
        if serializer.is_valid():
            user = request.user

            pass_check = user.check_password(data['old_password'])
            if pass_check:
                user.password = make_password(data['new_password'])
                user.save()
                username = user.username
                password = data['new_password']
                user = authenticate(username=username, password=password)
                if user is None:
                    return Response({
                        "response": "error",
                        "data": {}
                    }, status=status.HTTP_404_NOT_FOUND)
                user_serializer = LoginOutSerializer(user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'response': "success",
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': user_serializer.data,
                })
            else:
                return Response({
                    "response": "error",
                    "message": MSG_WRONG_PASSWORD,
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                "response":"error", 
                "message":MSG_WRONG_CREDENTIALS
                }, status=status.HTTP_400_BAD_REQUEST)
        
# TODO - Forgot Password
class ForgotPassword(APIView):
    def post(self, request):
        return Response("success")
    
class UpdateUser(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        operation_summary="Update email and/or mobile info of user.",
        operation_description="Need to authorize with Bearer token.",
        responses={200: UserDetailSerializer}
    )
    def put(self, request):
        try:
            data = request.data
            serializer = UserUpdateSerializer(data=data)
            if serializer.is_valid():

                user = request.user
                if 'mobile' in data:
                    if data['mobile'] != None and data["mobile"] != "":
                        user.mobile = data['mobile']
                if 'email'  in data:
                    if data["email"] != None and data["email"] != "":
                        user.email = data['email']
                if 'mobile_verified' in data:
                    if data['mobile_verified'] == True:
                        user.mobile_verified = True
                if 'email_verified' in data:
                    if data['email_verified'] == True:
                        user.email_verified = True
                
                user.save()
                out_serializer = UserDetailSerializer(user)
                return Response({
                    "response":"success", 
                    "data":out_serializer.data,
                    }, status=status.HTTP_200_OK)
        except:
            return Response({
                "response":"success",
                "message": MSG_UNKNOWN_ERROR
                }, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        request_body=ProfileOutSerializer,
        operation_summary="Update profile info of user.",
        operation_description="***IMPORTANT*** Body of request need to be 'form-data'. \nNeed to authorize with Bearer token.",
        responses={200: UserDetailSerializer}
    )
    def put(self, request):
        try:
            data = request.data
            user = request.user
            profile = Profile.objects.get(user=user)
            serializer = ProfileOutSerializer(profile, data=data)
            if serializer.is_valid():
                serializer.save()
                out_serializer = UserDetailSerializer(user)
                return Response({
                    "response":"success",
                    "data":out_serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "response":"error",
                    "message": MSG_NOT_VALID_INFO
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "response": "error", 
                "message": MSG_UNKNOWN_ERROR,
                }, status=status.HTTP_400_BAD_REQUEST)
        
class UserDetail(APIView):
    @swagger_auto_schema(
        operation_summary="Detailed info of user",
        operation_description="Autherization IS NOT required.",
        responses={200: UserDetailSerializer},
    )
    def get(self, request, pk):
        try:
            if User.objects.filter(pk=pk).exists():
                user = User.objects.get(pk=pk)
                serializer = UserDetailSerializer(user)
                return Response({
                    "response":"success",
                    "data": serializer.data
                })
            else:
                return Response({
                    "response": "error",
                    "message": MSG_USER_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({
                "response": "error",
                "message": MSG_UNKNOWN_ERROR,
            }, status=status.HTTP_400_BAD_REQUEST)
        
class UserListPaginated(APIView, LimitOffsetPagination):
    startdate = openapi.Parameter("startdate", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    enddate = openapi.Parameter("enddate", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    mobile = openapi.Parameter('mobile', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    email = openapi.Parameter('email', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    country = openapi.Parameter('country', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    city = openapi.Parameter('city', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    first_name = openapi.Parameter('first_name', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    last_name = openapi.Parameter('last_name', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    mobile_verified = openapi.Parameter('mobile_verified', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    email_verified = openapi.Parameter('email_verified', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    @swagger_auto_schema(
            manual_parameters=[startdate, enddate, mobile, email, country, city,
                               first_name, last_name, mobile_verified, email_verified],
            operation_summary="Paginated list of users.",
            operation_description="Autherization IS NOT required.",
            responses={200: UserDetailSerializer}
    )
    def get(self, request):
        try:
            startdate = request.query_params.get("startdate", None)
            enddate = request.query_params.get("enddate", None)
            mobile = request.query_params.get("mobile", None)
            email = request.query_params.get("email", None)
            country = request.query_params.get("country", None)
            city = request.query_params.get("city", None)
            first_name = request.query_params.get("first_name", None)
            last_name = request.query_params.get("last_name", None)
            mobile_verified = request.query_params.get("mobile_verified", None)
            email_verified = request.query_params.get("email_verified", None)
            users = User.objects.filter(is_active=True)
            if startdate  and enddate:
                if validate_date(startdate) and validate_date(enddate):
                    users = users.filter(date_joined__range=[startdate, enddate])
                else:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_VALID_DATE
                        }, status=status.HTTP_400_BAD_REQUEST)
            if mobile:
                users = users.filter(mobile__icontains=mobile)
            if email:
                users = users.filter(email__icontains=email)
            if mobile_verified == 'true':
                users = users.filter(mobile_verified=True)
            if mobile_verified == 'false':
                users = users.filter(mobile_verified=False)
            if email_verified == 'true':
                users = users.filter(email_verified=True)
            if email_verified == 'false':
                users = users.filter(email_verified=False)
            if country:
                profiles = Profile.objects.filter(country__icontains=country)
                users = users.filter(pk__in=profiles)
            if city:
                profiles = Profile.objects.filter(city__icontains=city)
                users = users.filter(pk__in=profiles)
            if first_name:
                profiles = Profile.objects.filter(first_name__icontains=first_name)
                users = users.filter(pk__in=profiles)
            if last_name:
                profiles = Profile.objects.filter(last_name__icontains=last_name)
                users = users.filter(pk__in=profiles)
            
            data = self.paginate_queryset(users, request, view=self)
            serializer = UserDetailSerializer(data, many=True)
            results = self.get_paginated_response(serializer.data)
            return Response({
                "response":"success",
                "data": results.data
            })
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)
        

class BusinessAccountList(APIView, LimitOffsetPagination):
    verified = openapi.Parameter('verified', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    title = openapi.Parameter("title", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    description = openapi.Parameter("description", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    email = openapi.Parameter("email", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    instagram = openapi.Parameter("instagram", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    facebook = openapi.Parameter("facebook", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    telegram = openapi.Parameter("telegram", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    phone = openapi.Parameter("phone", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    rating = openapi.Parameter('rating', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    created = openapi.Parameter('created', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    attribute = openapi.Parameter("attribute", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    atrvalue = openapi.Parameter("atrvalue", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    @swagger_auto_schema(
        manual_parameters=[verified, title, description, email, instagram, facebook, 
                           telegram, phone, rating, created, attribute, atrvalue],
        operation_description="Authorization IS NOT required.\n\n " \
                                "***IMPORTANT*** 'attribute' and 'atrvalue' needs to be proved together.\n\n " \
                                "***IMPORTANT*** 'rating' and 'created' are ordering properties and should be" \
                                " queried saparately.",
        operation_summary="Paginated list of buziness accounts.",
        responses={200: BusinessAccountListSerializer}
    )
    def get(self, request):
        try:
            verified = request.query_params.get("verified", None)
            title = request.query_params.get("title", None)
            description = request.query_params.get("description", None)
            email = request.query_params.get("email", None)
            instagram = request.query_params.get("instagram", None)
            facebook = request.query_params.get("facebook", None)
            telegram = request.query_params.get("telegram", None)
            phone = request.query_params.get("phone", None)
            rating = request.query_params.get("rating", None)
            created = request.query_params.get("created", None)
            attribute = request.query_params.get("attribute", None)
            atrvalue = request.query_params.get("atrvalue", None)
            
            accounts = BusinessAccount.objects.filter(is_active=True)
            
            if verified == "true":
                accounts = accounts.filter(is_verified=True)
            if verified == "false":
                accounts = accounts.filter(is_verified=False)
            if title:
                accounts = accounts.filter(Q(title_tm__icontains=title) | 
                                        Q(title_ru__icontains=title) |
                                        Q(title_en__icontains=title))
            if description:
                accounts = accounts.filter(Q(description_tm__icontains=description) |
                                        Q(description_ru__icontains=description) |
                                        Q(description_en__icontains=description))
            if email:
                accounts = accounts.filter(Q(email__icontains=email))
            if instagram:
                accounts = accounts.filter(Q(instagram__icontains=instagram))
            if facebook:
                accounts = accounts.filter(Q(facebook__icontains=facebook))
            if telegram:
                accounts = accounts.filter(Q(telegram__icontains=telegram))
            if phone:
                accounts = accounts.filter(Q(phone__icontains=phone))
            if rating == "true":
                accounts = accounts.order_by("-rating")
            if rating == "false":
                accounts = accounts.order_by("rating")
            if created == "true":
                accounts = accounts.order_by("-created_at")
            if created == "false":
                accounts = accounts.order_by("created_at")

            if attribute and atrvalue:
                attribute = int(attribute)
                atrvalue = str(atrvalue)
                ba_list = BA_Attribute_Value.objects.filter(
                                        Q(attribute__id=attribute) &
                                        Q(value_tm__icontains=atrvalue)).values_list(
                                        'business_account__pk',
                                        flat=True)
                accounts = accounts.filter(pk__in=ba_list)
            
                
            data = self.paginate_queryset(accounts, request, view=self)
            serializer = BusinessAccountListSerializer(data, many=True)
            results = self.get_paginated_response(serializer.data)
            return Response({
                "response":"success",
                "data":results.data
            })
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class BusinessAccountDetail(APIView):
    @swagger_auto_schema(
            operation_summary="Authorization IS NOT Required",
            operation_description="***IMPORTANT*** 'pk' IS primary key of business account, NOT primary key of user account.",
            responses={200: BusinessAccountDetailSerializer}
    )
    def get(self, request, pk):
        try:
            if BusinessAccount.objects.filter(pk=pk).exists():
                account = BusinessAccount.objects.get(pk=pk)
                serializer = BusinessAccountDetailSerializer(account)
                return Response({
                    "response":"success",
                    "data":serializer.data
                })
            else:
                return Response({
                    "response":"error",
                    "message": MSG_BA_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class BusinessAccountCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS Required.",
            operation_summary="Create Business account.",
            request_body=BusinessAccountCreateSerializer,
    )
    def post(self, request):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            if BusinessAccount.objects.filter(user=user).exists():
                return Response({
                    "response":"error",
                    "message": MSG_BA_EXISTS
                })
            serializer = BusinessAccountCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                if BusinessAccount.objects.filter(pk=serializer.data['id']).exists():
                    out_account = BusinessAccount.objects.get(pk=serializer.data['id'])
                    out_serializer = BusinessAccountDetailSerializer(out_account)
                    return Response({
                        "response":"success",
                        "data": out_serializer.data
                    })
                else:
                    return Response({
                        "response":"error",
                        "message": MSG_UNKNOWN_ERROR
                    })
            else:
                return Response({
                    "response":"error",
                    "message": MSG_DATA_NOT_VALID
                })
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)
        
class BusinessAccountUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS required.",
            operation_summary="Update business account.",
            request_body=BusinessAccountCreateSerializer,
            responses={200: BusinessAccountDetailSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            if BusinessAccount.objects.filter(pk=pk).exists():
                account = BusinessAccount.objects.get(pk=pk)
                if account.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                serializer = BusinessAccountCreateSerializer(account, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    out_serializer = BusinessAccountDetailSerializer(account)
                    return Response({
                        "response":"success",
                        "data": out_serializer.data
                    })
                else:
                    return Response({
                        "response":"error",
                        "message": MSG_DATA_NOT_VALID
                    })
            else:
                return Response({
                        "response": "error",
                        "message": MSG_BA_NOT_FOUND
                    }, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class BusinessAccountDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Delete business account.",
    )
    def delete(self, request, pk):
        try:
            user = request.user
            data = request.data
            if BusinessAccount.objects.filter(pk=pk).exists():
                account = BusinessAccount.objects.get(pk=pk)
                if account.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                account.delete()
                return Response({
                    "response": "success",
                    "message": MSG_OBJECT_DELTED
                })
            else:
                return Response({
                        "response": "error",
                        "message": MSG_BA_NOT_FOUND
                    }, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class BAAttrValueCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS required.",
            operation_summary="Update business account.",
            request_body=BAAttributeValueCreateSerializer,
            responses={200: BAAttributeValueCreateSerializer}
    )
    def post(self, request):
        try:
            user = request.user
            data = request.data
            ba_id = data['business_account']
            ba_id = int(ba_id)
            attr_id = data["attribute"]
            attr_id = int(attr_id)
            if BusinessAccount.objects.filter(pk=ba_id).exists() and  \
                BA_Attribute.objects.filter(pk=attr_id).exists():
                account = BusinessAccount.objects.get(pk=ba_id)
                if account.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                serializer = BAAttributeValueCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    if BA_Attribute_Value.objects.filter(pk=serializer.data['id']).exists():
                        attr_value = BA_Attribute_Value.objects.get(pk=serializer.data["id"])
                        out_serializer = BAAttributeValueOutSerializer(attr_value)
                        return Response({
                            "response":"success",
                            "data": out_serializer.data
                        })
                    else:
                        return Response({
                            "response":"error",
                            "message": MSG_UNKNOWN_ERROR
                        })
                else:
                    return Response({
                        "response":"error",
                        "message": MSG_DATA_NOT_VALID
                    })
            else:
                return Response({
                    "response":"error",
                    "message": MSG_OBJECT_NOT_FOUND
                })
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class BAAttrValueUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS required.",
            operation_summary="Update business update.",
            request_body=BAAttributeValueCreateSerializer,
            responses={200: BAAttributeValueCreateSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            ba_id = data['business_account']
            ba_id = int(ba_id)
            attr_id = data["attribute"]
            attr_id = int(attr_id)
            if BA_Attribute_Value.objects.filter(pk=pk).exists():
                ba_attr_value = BA_Attribute_Value.objects.get(pk=pk)
                if BusinessAccount.objects.filter(pk=ba_id).exists() and  \
                    BA_Attribute.objects.filter(pk=attr_id).exists():
                    account = BusinessAccount.objects.get(pk=ba_id)
                    if account.user != user:
                        return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                    ba_attr_value = BA_Attribute_Value.objects.get(pk=pk)
                    serializer = BAAttributeValueCreateSerializer(ba_attr_value, data=data)
                    if serializer.is_valid():
                        serializer.save()
                        if BA_Attribute_Value.objects.filter(pk=serializer.data['id']).exists():
                            attr_value = BA_Attribute_Value.objects.get(pk=serializer.data["id"])
                            out_serializer = BAAttributeValueOutSerializer(attr_value)
                            return Response({
                                "response":"success",
                                "data": out_serializer.data
                            })
                        else:
                            return Response({
                                "response":"error",
                                "message": MSG_UNKNOWN_ERROR
                            })
                    else:
                        return Response({
                            "response":"error",
                            "message": MSG_DATA_NOT_VALID
                        })
                else:
                    return Response({
                        "response":"error",
                        "message": MSG_OBJECT_NOT_FOUND
                    })
            else:
                return Response({
                        "response": "error",
                        "message": MSG_OBJECT_NOT_FOUND
                    }, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class BAAttrValueDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS required.\n\n "\
            "***IMPORTANT***   need to provide 'business_account' as int," \
            "bakcend will additionally check if the user can delete this object.",
        operation_summary="business attribute delete.",
        request_body=BAAttributeValueDeleteSerializer
    )
    def delete(self, request, pk):
        try:
            user = request.user
            data = request.data
            ba_id = data['business_account']
            if BusinessAccount.objects.filter(pk=ba_id).exists():
                account = BusinessAccount.objects.get(pk=ba_id)
                if account.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                if BA_Attribute_Value.objects.filter(pk=pk).exists():
                    attr_value = BA_Attribute_Value.objects.get(pk=pk)
                    attr_value.delete()
                    return Response({
                        "response": "success",
                        "message": MSG_OBJECT_DELTED
                    })
                else:
                    return Response({
                            "response": "error",
                            "message": MSG_OBJECT_NOT_FOUND
                        }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    "response":"error",
                    "message": MSG_OBJECT_NOT_FOUND
                })
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class BARatingCreate(APIView):
    rating = openapi.Parameter('rating', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(
        operation_summary = "Business Account rating 1-5",
        operation_description="***IMPORTANT*** 'pk' is primary key of business account.",
        manual_parameters=[rating]
    )
    def get(self, request, pk):
        try:
            if BusinessAccount.objects.filter(pk=pk).exists():
                account = BusinessAccount.objects.get(pk=pk)
                rating = request.query_params.get("rating", None)
                if not rating.isdigit():
                    return Response({
                        "response":"error",
                        "message": "'rating' need to be integer and between 1-5"
                    })
                rating = int(rating)
                rating_count = account.rating_count
                old_rating = account.rating
                new_rating = calculate_rating(old_rating, rating_count, rating)
                account.rating = round(new_rating, 2)
                account.rating_count = rating_count + 1
                account.save()
                return Response({"response":"success", "rating":account.rating})
            else:
                return Response({
                    "response":"error",
                    "message": MSG_OBJECT_NOT_FOUND
                })
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class BASeenCount(APIView):
    @swagger_auto_schema(
        operation_summary = "Business Account seen count",
        operation_description="***IMPORTANT*** 'pk' is primary key of business account."
    )
    def get(self, request, pk):
        if BusinessAccount.objects.filter(pk=pk).exists():
            account = BusinessAccount.objects.get(pk=pk)
            account.seen_count = account.seen_count + 1
            account.save()
            return Response({"response":"success", "seen_ccount":account.seen_count})
        else:
            return Response({
                    "response":"error",
                    "message": MSG_OBJECT_NOT_FOUND
                })