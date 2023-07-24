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

from service.models import *
from .serializers import *
from api.utils import *


class VehicleTypeList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: VehicleTypeListSerializer}
    )
    def get(self, request):
        types = VehicleType.objects.all()
        serializer = VehicleTypeListSerializer(types, many=True)
        return Response({
            "response":"success",
            "data": serializer.data
        })

class CargoTypeList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: CargoTypeListSerializer}
    )
    def get(self, request):
        types = CargoType.objects.all()
        serializer = CargoTypeListSerializer(types, many=True)
        return Response({
            "response":"success",
            "data": serializer.data
        })

class WarehouseTypeList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: WarehouseTypeListSerializer}
    )
    def get(self, request):
        types = WarehouseType.objects.all()
        serializer = WarehouseTypeListSerializer(types, many=True)
        return Response({
            "response":"success",
            "data": serializer.data
        })

class DriverAttributesList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: DriverAttrListSerializer}
    )
    def get(self, request):
        attributes = Driver_Attribute.objects.all()
        serializer = DriverAttrListSerializer(attributes, many=True)
        return Response({
            "response":"success",
            "data": serializer.data
        })

class CargoAttributesList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: CargoAttrListSerializer}
    )
    def get(self, request):
        attributes = CargoAttribute.objects.all()
        serializer = CargoAttrListSerializer(attributes, many=True)
        return Response({
            "response":"success",
            "data": serializer.data
        })
    
class WarehouseAttributesList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: WarehouseAttrListSerializer}
    )
    def get(self, request):
        attributes = WarehouseAttribute.objects.all()
        serializer = WarehouseAttrListSerializer(attributes, many=True)
        return Response({
            "response":"success",
            "data": serializer.data
        })

class TransportAttributesList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: TransportAttrListSerializer}
    )
    def get(self, request):
        attributes = TransportAttribute.objects.all()
        serializer = TransportAttrListSerializer(attributes, many=True)
        return Response({
            "response":"success",
            "data": serializer.data
        })
    
class DriverList(APIView, LimitOffsetPagination):
    title = openapi.Parameter("title", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    description = openapi.Parameter("description", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    vip = openapi.Parameter('vip', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    likes = openapi.Parameter('likes', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    rating = openapi.Parameter('rating', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    created = openapi.Parameter('created', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    user = openapi.Parameter("user", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    attribute = openapi.Parameter("attribute", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    atrvalue = openapi.Parameter("atrvalue", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    vehicle_type = openapi.Parameter("vehicle_type", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(
        manual_parameters=[title, description, vip, likes, rating, created,
                        user, attribute, atrvalue, vehicle_type],
        operation_description="Authorizaton IS NOT required. \n\n" \
                        "***IMPORTANT*** 'rating', 'created' and 'likes' ordering should be used one at time.\n\n" \
                        "'category', 'attribute' need to be integer field.",
        operation_summary="Paginated List of Drivers.",
        responses={200: DriversListSerializer}
    )
    def get(self, request):
        title = request.query_params.get("title", None)
        description = request.query_params.get("description", None)
        rating = request.query_params.get("rating", None)
        created = request.query_params.get("created", None)
        attribute = request.query_params.get("attribute", None)
        atrvalue = request.query_params.get("atrvalue", None)
        vip = request.query_params.get("vip", None)
        likes = request.query_params.get("likes", None)
        user = request.query_params.get("user", None)
        vehicle_type = request.query_params.get("vehicle_type", None)

        drivers = Driver.objects.filter(is_active=True)

        if vip == "true":
            drivers = drivers.filter(is_vip=True)
        if vip == "false":
            drivers = drivers.filter(is_vip=False)
        
        if user:
            drivers = drivers.filter(user=user)
        
        if title:
            drivers = drivers.filter(Q(title_tm__icontains=title) | 
                                                Q(title_ru__icontains=title) |
                                                Q(title_en__icontains=title))
        if description:
            drivers = drivers.filter(Q(description_tm__icontains=description) |
                                                Q(description_ru__icontains=description) |
                                                Q(description_en__icontains=description))
            
        if vehicle_type:
            drivers = drivers.filter(vehicle_type=vehicle_type)
            
        if attribute and atrvalue:
            attribute = int(attribute)
            atrvalue = str(atrvalue)
            dr_list = Driver_Attribute_Value.objects.filter(
                                    Q(attribute__id=attribute) &
                                    Q(value_tm__icontains=atrvalue)).values_list(
                                    'driver__pk',
                                    flat=True)
            drivers = drivers.filter(pk__in=dr_list)

        if rating == "true":
            drivers = drivers.order_by("-rating")
        if rating == "false":
            drivers = drivers.order_by("rating")
        if likes == "true":
            drivers = drivers.order_by("-like_count")
        if likes == "false":
            drivers = drivers.order_by("like_count")
        if created == "true":
            drivers = drivers.order_by("-created_at")
        if created == "false":
            drivers = drivers.order_by("created_at")

        
        data = self.paginate_queryset(drivers, request, view=self)
        serializer = DriversListSerializer(data, many=True)
        results = self.get_paginated_response(serializer.data)
        return Response({
            "response":"success",
            "data": results.data
        })

class DriverDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="Authorization IS NOT Required",
        operation_description="***IMPORTANT*** 'pk' IS primary key of driver.",
        responses={200: DriversListSerializer}
    )
    def get(self, reqeust, pk):
        try:
            if Driver.objects.filter(pk=pk).exists():
                driver = Driver.objects.get(pk=pk)
                serializer = DriversListSerializer(driver)
                return Response({
                        "response":"success",
                        "data": serializer.data
                    })
            else:
                return Response({
                    "response":"error",
                    "message": MSG_OBJECT_NOT_FOUND,
                }, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class DriverCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS Required.",
            operation_summary="Create New Driver.",
            request_body=DriverCreateSerializer,
            responses={200: DriversListSerializer}
    )
    def post(self, request):
        try:
            user = request.user
            data = request.data
            mobile_verified = user.mobile_verified
            email_verified = user.email_verified
            _mutable = data._mutable
            data._mutable = True
            data['user'] = user.id
            vehicle_type = data['vehicle_type']
            data['vehicle_type'] = int(vehicle_type)
            data._mutable = _mutable
            serializer = DriverCreateSerializer(data=data)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
                if Driver.objects.filter(pk=serializer.data['id']).exists():
                    driver = Driver.objects.get(pk=serializer.data['id'])
                    if mobile_verified or email_verified:
                            driver.is_active = True
                    driver.save()
                    out_serializer = DriversListSerializer(driver)
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
        
class DriverUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS Required.",
            operation_summary="Update Driver.",
            request_body=DriverCreateSerializer,
            responses={200: DriversListSerializer}
    )
    def put(self, request, pk):
        user = request.user
        data = request.data
        mobile_verified = user.mobile_verified
        email_verified = user.email_verified
        if Driver.objects.filter(pk=pk).exists():
            driver = Driver.objects.get(pk=pk)
            if driver.user != user:
                return Response({
                    "response":"error",
                    "message": MSG_NOT_BELONG_TO_USER
                })
            if mobile_verified or email_verified:
                driver.is_active = True
            serializer = DriverCreateSerializer(driver, data=data)
            if serializer.is_valid():
                serializer.save()
                out_serializer = DriversListSerializer(driver)
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
                    "message": MSG_OBJECT_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)

class DriverDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS Required.",
        operation_summary="Delete Driver."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if Driver.objects.filter(pk=pk).exists():
                driver = Driver.objects.get(pk=pk)
                print(driver.user)
                print(user)
                if driver.user != user:
                    return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                driver.delete()
                return Response({
                    "response": "success",
                    "message": MSG_OBJECT_DELTED
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
        
class DriverAttrValueCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Create Driver Attr Value.",
        request_body=DriverAttrValueCreateSerializer,
        responses={200:DriverAttrValueCreateOutSerializer}
    )
    def post(self, request):
        try:
            user = request.user
            data = request.data
            driver_id = data["driver"]
            attr_id = data["attribute"]
            driver_id = int(driver_id)
            attr_id = int(attr_id)
            if Driver.objects.filter(pk=driver_id).exists() and \
                Driver_Attribute.objects.filter(pk=attr_id).exists():
                driver = Driver.objects.get(pk=driver_id)
                if driver.user != user:
                    return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                serializer = DriverAttrValueCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    if Driver_Attribute_Value.objects.filter(pk=serializer.data['id']).exists():
                        attr_value = Driver_Attribute_Value.objects.get(pk=serializer.data['id'])
                        out_serializer = DriverAttrValueCreateOutSerializer(attr_value)
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

class DriverAttrValueUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Update Driver Attr Value.",
        request_body=DriverAttrValueCreateSerializer,
        responses={200:DriverAttrValueCreateOutSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            driver_id = data["driver"]
            attr_id = data["attribute"]
            driver_id = int(driver_id)
            attr_id = int(attr_id)
            if Driver.objects.filter(pk=driver_id).exists() and \
                Driver_Attribute.objects.filter(pk=attr_id).exists():
                driver = Driver.objects.get(pk=driver_id)
                if driver.user != user:
                    return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                driver_attr_value = Driver_Attribute_Value.objects.get(pk=pk)
                serializer = DriverAttrValueCreateSerializer(driver_attr_value, data=data)
                if serializer.is_valid():
                    serializer.save()
                    if Driver_Attribute_Value.objects.filter(pk=serializer.data["id"]).exists():
                        attr_value = Driver_Attribute_Value.objects.get(pk=serializer.data["id"])
                        out_serializer = DriverAttrValueCreateOutSerializer(attr_value)
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
            
class DriverAttrValueDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Driver attribute value delete."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if Driver_Attribute_Value.objects.filter(pk=pk).exists():
                attr_value = Driver_Attribute_Value.objects.get(pk=pk)
                driver = attr_value.driver
                if driver.user != user:
                    return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
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
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class DriverCommentCreate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Create Driver Comment",
        operation_description = "",
        request_body=DriverCommentCreateSerializer,
        responses={200:DriverCommentCreateOutSerializer}
    )
    def post(self, request):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            driver_id = data["driver"]
            driver_id = int(driver_id)

            if Driver.objects.filter(pk=driver_id).exists():
                serializer = DriverCommentCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    if DriverComment.objects.filter(pk=serializer.data["id"]).exists():
                        comment = DriverComment.objects.get(pk=serializer.data["id"])
                        mobile_verified = comment.user.mobile_verified
                        email_verified = comment.user.email_verified
                        if mobile_verified or email_verified:
                            comment.is_active = True
                            comment.save()
                        out_serializer = DriverCommentCreateOutSerializer(comment)
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
                            "response": "error",
                            "message": MSG_OBJECT_NOT_FOUND
                        }, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class DriverCommentUpdate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Update Driver Comment",
        operation_description = "",
        request_body=DriverCommentCreateSerializer,
        responses={200:DriverCommentCreateOutSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            driver_id = data["driver"]
            driver_id = int(driver_id)
            if Driver.objects.filter(pk=driver_id).exists():
                if DriverComment.objects.filter(pk=pk).exists():
                    comment = DriverComment.objects.get(pk=pk)
                    if comment.user != user:
                        return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                    serializer = DriverCommentCreateSerializer(comment, data=data)
                    if serializer.is_valid():
                        serializer.save()
                        mobile_verified = comment.user.mobile_verified
                        email_verified = comment.user.email_verified
                        if mobile_verified or email_verified:
                            comment.is_active = True
                            comment.save()
                        out_serializer = DriverCommentCreateOutSerializer(comment)
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
                            "message": MSG_OBJECT_NOT_FOUND
                        }, status=status.HTTP_404_NOT_FOUND)
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

class DriverCommentDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS Required.",
        operation_summary="Driver Comment Delete."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if DriverComment.objects.filter(pk=pk).exists():
                comment = DriverComment.objects.get(pk=pk)
                if comment.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                comment.delete()
                return Response({
                    "response": "success",
                    "message": MSG_OBJECT_DELTED
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
            
class DriverRatingCreate(APIView):
    rating = openapi.Parameter('rating', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(
        operation_summary = "Driver rating 1-5",
        operation_description="***IMPORTANT*** 'pk' is primary key of driver.",
        manual_parameters=[rating]
    )
    def get(self, request, pk):
        try:
            if Driver.objects.filter(pk=pk).exists():
                driver = Driver.objects.get(pk=pk)
                rating = request.query_params.get("rating", None)
                if not rating.isdigit():
                    return Response({
                        "response":"error",
                        "message": "'rating' need to be integer and between 1-5"
                    })
                rating = int(rating)
                rating_count = driver.rating_count
                old_rating = driver.rating
                new_rating = calculate_rating(old_rating, rating_count, rating)
                driver.rating = round(new_rating, 2)
                driver.rating_count = rating_count + 1
                driver.save()
                return Response({"response":"success", "rating":driver.rating})
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
        
class DriverSeenCount(APIView):
    @swagger_auto_schema(
        operation_summary = "Driver seen count",
        operation_description="***IMPORTANT*** 'pk' is primary key of driver."
    )
    def get(self, request, pk):
        if Driver.objects.filter(pk=pk).exists():
            driver = Driver.objects.get(pk=pk)
            driver.seen_count = driver.seen_count + 1
            driver.save()
            return Response({"response":"success", "seen_ccount":driver.seen_count})
        else:
            return Response({
                    "response":"error",
                    "message": MSG_OBJECT_NOT_FOUND
                })

class DriverLikeCountAdd(APIView):
    @swagger_auto_schema(
        operation_summary = "Driver like add",
        operation_description="***IMPORTANT*** 'pk' is primary key of driver."
    )
    def get(self, request, pk):
        if Driver.objects.filter(pk=pk).exists():
            driver = Driver.objects.get(pk=pk)
            driver.like_count = driver.like_count + 1
            driver.save()
            return Response({
                "response":"success",
                "like_count": driver.like_count
            })
        else:
            return Response({
                    "response":"error",
                    "message": MSG_OBJECT_NOT_FOUND
                })

class DriverLikeCountRemove(APIView):
    @swagger_auto_schema(
        operation_summary = "Driver like remove",
        operation_description="***IMPORTANT*** 'pk' is primary key of driver."
    )
    def get(self, request, pk):
        if Driver.objects.filter(pk=pk).exists():
            driver = Driver.objects.get(pk=pk)
            driver.like_count = driver.like_count - 1
            driver.save()
            return Response({
                "response":"success",
                "like_count": driver.like_count
            })
        else:
            return Response({
                    "response":"error",
                    "message": MSG_OBJECT_NOT_FOUND
                })

class CargoList(APIView, LimitOffsetPagination):
    title = openapi.Parameter("title", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    description = openapi.Parameter("description", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    vip = openapi.Parameter('vip', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    likes = openapi.Parameter('likes', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    rating = openapi.Parameter('rating', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    created = openapi.Parameter('created', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    user = openapi.Parameter("user", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    attribute = openapi.Parameter("attribute", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    atrvalue = openapi.Parameter("atrvalue", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    vehicle_type = openapi.Parameter("vehicle_type", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    cargo_type = openapi.Parameter("cargo_type", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    from_country = openapi.Parameter("from_country", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    from_location = openapi.Parameter("from_location", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    to_country = openapi.Parameter("to_country", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    to_location = openapi.Parameter("to_location", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    minweight = openapi.Parameter("minweight", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    maxweight = openapi.Parameter("maxweight", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    minvolume = openapi.Parameter("minvolume", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    maxvolume = openapi.Parameter("maxvolume", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    minprice = openapi.Parameter("minprice", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    maxprice = openapi.Parameter("maxprice", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    loading_date_start = openapi.Parameter("loading_date_start", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    loading_date_end = openapi.Parameter("loading_date_end", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    unloading_date_start = openapi.Parameter("unloading_date_start", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    unloading_date_end = openapi.Parameter("unloading_date_end", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)

    @swagger_auto_schema(
        manual_parameters=[title, description, vip, likes, rating, created,
                        user, attribute, atrvalue, vehicle_type, cargo_type,
                        from_country, from_location, to_country, to_location,
                        minweight, maxweight, minvolume, maxvolume, minprice,
                        maxprice, loading_date_start, loading_date_end,
                        unloading_date_start, unloading_date_end],
        operation_description="Authorizaton IS NOT required. \n\n" \
                        "***IMPORTANT*** 'rating', 'created' and 'likes' ordering should be used one at time.\n\n" \
                        "'category', 'attribute' need to be integer field.",
        operation_summary="Paginated List of Drivers.",
        responses={200: CargoListSerializer}
    )
    def get(self, request):
        try:
            title = request.query_params.get("title", None)
            description = request.query_params.get("description", None)
            rating = request.query_params.get("rating", None)
            created = request.query_params.get("created", None)
            attribute = request.query_params.get("attribute", None)
            atrvalue = request.query_params.get("atrvalue", None)
            vip = request.query_params.get("vip", None)
            likes = request.query_params.get("likes", None)
            user = request.query_params.get("user", None)
            vehicle_type = request.query_params.get("vehicle_type", None)
            cargo_type = request.query_params.get("cargo_type", None)
            from_country = request.query_params.get("from_country", None)
            from_location = request.query_params.get("from_location", None)
            to_country = request.query_params.get("to_country", None)
            to_location = request.query_params.get("to_location", None)
            minweight = request.query_params.get("minweight", None)
            maxweight = request.query_params.get("maxweight", None)
            minvolume = request.query_params.get("minvolume", None)
            maxvolume = request.query_params.get("maxvolume", None)
            minprice = request.query_params.get("minprice", None)
            maxprice = request.query_params.get("maxprice", None)
            loading_date_start = request.query_params.get("loading_date_start", None)
            loading_date_end = request.query_params.get("loading_date_end", None)
            unloading_date_start = request.query_params.get("unloading_date_start", None)
            unloading_date_end = request.query_params.get("unloading_date_end", None)

            cargos = Cargo.objects.filter(is_active=True)
            if vip == "true":
                cargos = cargos.filter(is_vip=True)
            if vip == "false":
                cargos = cargos.filter(is_vip=False)
            
            if user:
                cargos = cargos.filter(user=user)

            if title:
                cargos = cargos.filter(Q(title_tm__icontains=title) | 
                                        Q(title_ru__icontains=title) |
                                        Q(title_en__icontains=title))
            if description:
                cargos = cargos.filter(Q(description_tm__icontains=description) |
                                    Q(description_ru__icontains=description) |
                                    Q(description_en__icontains=description))
            
            if from_country:
                cargos = cargos.filter(from_country__icontains=from_country)
            if from_location:
                cargos = cargos.filter(from_location__icontains=from_location)
            if to_country:
                cargos = cargos.filter(to_country__icontains=to_country)
            if to_location:
                cargos = cargos.filter(to_location__icontains=to_location)
            
            if vehicle_type:
                cargos = cargos.filter(vehicle_type=vehicle_type)

            if cargo_type:
                cargos = cargos.filter(cargo_type=cargo_type)
            
            if minweight and maxweight:
                cargos = cargos.filter(weight__range=[minweight, maxweight])

            if minvolume and maxvolume:
                cargos = cargos.filter(volume__range=[minvolume, maxvolume])
            
            if minprice and maxprice:
                cargos = cargos.filter(price__range=[minprice, maxprice])
            
            if loading_date_start and loading_date_end:
                cargos = cargos.filter(loading_date__range=[loading_date_start, loading_date_end])
            
            if unloading_date_start and unloading_date_end:
                cargos = cargos.filter(unloading_date__range=[unloading_date_start, unloading_date_end])
            
            if attribute and atrvalue:
                attribute = int(attribute)
                atrvalue = str(atrvalue)
                cargo_list = CargoAttributeValue.objects.filter(
                                        Q(attribute__id=attribute) &
                                        Q(value_tm__icontains=atrvalue)).values_list(
                                        'cargo__pk',
                                        flat=True)
                cargos = cargos.filter(pk__in=cargo_list)
            
            if rating == "true":
                cargos = cargos.order_by("-rating")
            if rating == "false":
                cargos = cargos.order_by("rating")
            if likes == "true":
                cargos = cargos.order_by("-like_count")
            if likes == "false":
                cargos = cargos.order_by("like_count")
            if created == "true":
                cargos = cargos.order_by("-created_at")
            if created == "false":
                cargos = cargos.order_by("created_at")

            data = self.paginate_queryset(cargos, request, view=self)
            serializer = CargoListSerializer(data, many=True)
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





                                 
# TODO 44 Cargo Detail
# TODO 43 Cargo Create
# TODO 42 Cargo Update
# TODO 41 Cargo Delete
# TODO 40 Cargo Attr value create
# TODO 39 Cargo Attr value update
# TODO 38 Cargo Attr value delete
# TODO 37 Cargo comment create
# TODO 36 Cargo comment update
# TODO 35 Cargo comment delete
# TODO 34 Cargo rating create
# TODO 33 Cargo seen count create
# TODO 32 Cargo like count add
# TODO 31 Cargo like count remove
# TODO 30 Warehouse List
# TODO 29 Warehouse Detail
# TODO 28 Warehouse Create
# TODO 27 Warehouse Update
# TODO 26 Warehouse Delete
# TODO 25 Warehouse Attr value create
# TODO 24 Warehouse Attr value update
# TODO 23 Warehouse Attr value delete
# TODO 22 Warehouse comment create
# TODO 21 Warehouse comment update
# TODO 20 Warehouse comment delete
# TODO 19 Warehouse rating create
# TODO 18 Warehouse seen count create
# TODO 17 Warehouse like count add
# TODO 16 Warehouse like count remove
# TODO 15 Transport List
# TODO 14 Transport Detail
# TODO 13 Transport Create
# TODO 12 Transport Update
# TODO 11 Transport Delete
# TODO 10 Transport Attr value create
# TODO 9 Transport Attr value update
# TODO 8 Transport Attr value delete
# TODO 7 Transport comment create
# TODO 6 Transport comment update
# TODO 5 Transport comment delete
# TODO 4 Transport rating create
# TODO 3 Transport seen count create
# TODO 2 Transport like count add
# TODO 1 Transport like count remove