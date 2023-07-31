from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
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
        try:
            types = VehicleType.objects.all()
            serializer = VehicleTypeListSerializer(types, many=True)
            return Response({
                "response":"success",
                "data": serializer.data
            })
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class CargoTypeList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: CargoTypeListSerializer}
    )
    def get(self, request):
        try:
            types = CargoType.objects.all()
            serializer = CargoTypeListSerializer(types, many=True)
            return Response({
                "response":"success",
                "data": serializer.data
            })
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class WarehouseTypeList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: WarehouseTypeListSerializer}
    )
    def get(self, request):
        try:
            types = WarehouseType.objects.all()
            serializer = WarehouseTypeListSerializer(types, many=True)
            return Response({
                "response":"success",
                "data": serializer.data
            })
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class DriverAttributesList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: DriverAttrListSerializer}
    )
    def get(self, request):
        try:
            attributes = Driver_Attribute.objects.all()
            serializer = DriverAttrListSerializer(attributes, many=True)
            return Response({
                "response":"success",
                "data": serializer.data
            })
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class CargoAttributesList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: CargoAttrListSerializer}
    )
    def get(self, request):
        try:
            attributes = CargoAttribute.objects.all()
            serializer = CargoAttrListSerializer(attributes, many=True)
            return Response({
                "response":"success",
                "data": serializer.data
            })
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)
    
class WarehouseAttributesList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: WarehouseAttrListSerializer}
    )
    def get(self, request):
        try:
            attributes = WarehouseAttribute.objects.all()
            serializer = WarehouseAttrListSerializer(attributes, many=True)
            return Response({
                "response":"success",
                "data": serializer.data
            })
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class TransportAttributesList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: TransportAttrListSerializer}
    )
    def get(self, request):
        try:
            attributes = TransportAttribute.objects.all()
            serializer = TransportAttrListSerializer(attributes, many=True)
            return Response({
                "response":"success",
                "data": serializer.data
            })
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)
    
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
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class DriverDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="Authorization IS NOT Required",
        operation_description="***IMPORTANT*** 'pk' IS primary key of driver.",
        responses={200: DriversDetailSerializer}
    )
    def get(self, reqeust, pk):
        try:
            if Driver.objects.filter(pk=pk).exists():
                driver = Driver.objects.get(pk=pk)
                serializer = DriversDetailSerializer(driver)
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
            responses={200: DriversDetailSerializer}
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
                    out_serializer = DriversDetailSerializer(driver)
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
            responses={200: DriversDetailSerializer}
    )
    def put(self, request, pk):
        try:
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
                    out_serializer = DriversDetailSerializer(driver)
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
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

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
        try:
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
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class DriverLikeCountAdd(APIView):
    @swagger_auto_schema(
        operation_summary = "Driver like add",
        operation_description="***IMPORTANT*** 'pk' is primary key of driver."
    )
    def get(self, request, pk):
        try:
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
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class DriverLikeCountRemove(APIView):
    @swagger_auto_schema(
        operation_summary = "Driver like remove",
        operation_description="***IMPORTANT*** 'pk' is primary key of driver."
    )
    def get(self, request, pk):
        try:
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
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

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
                        "'category', 'user' and 'attribute' need to be integer field.",
        operation_summary="Paginated List of Cargos.",
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

class CargoDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="Authorization IS NOT Required",
        operation_description="***IMPORTANT*** 'pk' IS primary key of cargo.",
        responses={200: CargoDetailSerializer}
    )
    def get(self, request, pk):
        try:
            if Cargo.objects.filter(pk=pk).exists():
                cargo = Cargo.objects.get(pk=pk)
                serializer = CargoDetailSerializer(cargo)
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

class CargoCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS Required.",
            operation_summary="Create New Cargo.",
            request_body=CargoCreateSerializer,
            responses={200: CargoDetailSerializer}
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
            serializer = CargoCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                if Cargo.objects.filter(pk=serializer.data["id"]).exists():
                    cargo = Cargo.objects.get(pk=serializer.data['id'])
                    if mobile_verified or email_verified:
                        cargo.is_active = True
                    cargo.save()
                    out_serializer = CargoDetailSerializer(cargo)
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

class CargoUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS Required.",
            operation_summary="Cargo Update.",
            request_body=CargoCreateSerializer,
            responses={200: CargoDetailSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            mobile_verified = user.mobile_verified
            email_verified = user.email_verified
            if Cargo.objects.filter(pk=pk).exists():
                cargo = Cargo.objects.get(pk=pk)
                if cargo.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                if mobile_verified or email_verified:
                    cargo.is_active = True
                serializer = CargoCreateSerializer(cargo, data=data)
                if serializer.is_valid():
                    serializer.save()
                    out_serializer = CargoDetailSerializer(cargo)
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
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class CargoDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS Required.",
        operation_summary="Delete Cargo."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if Cargo.objects.filter(pk=pk).exists():
                cargo = Cargo.objects.get(pk=pk)
                if cargo.user != user:
                    return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                cargo.delete()
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

class CargoAttrValueCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Create Cargo Attr Value.",
        request_body=CargoAttrValueCreateSerializer,
        responses={200:CargoAttrValueCreateOutSerializer}
    )
    def post(self, request):
        try:
            user = request.user
            data = request.data
            cargo_id = data["cargo"]
            attr_id = data["attribute"]
            cargo_id = int(cargo_id)
            attr_id = int(attr_id)
            if Cargo.objects.filter(pk=cargo_id).exists and \
                CargoAttribute.objects.filter(pk=attr_id).exists():
                cargo = Cargo.objects.get(pk=cargo_id)
                if cargo.user != user:
                    return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                serializer = CargoAttrValueCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    if CargoAttributeValue.objects.filter(pk=serializer.data['id']).exists():
                        attr_value = CargoAttributeValue.objects.get(pk=serializer.data['id'])
                        out_serializer = CargoAttrValueCreateOutSerializer(attr_value)
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

class CargoAttrValueUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Update Cargo Attr Value.",
        request_body=CargoAttrValueCreateSerializer,
        responses={200:CargoAttrValueCreateOutSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            cargo_id = data["cargo"]
            attr_id = data["attribute"]
            cargo_id = int(cargo_id)
            attr_id = int(attr_id)
            if Cargo.objects.filter(pk=cargo_id).exists and \
                CargoAttribute.objects.filter(pk=attr_id).exists():
                cargo = Cargo.objects.get(pk=cargo_id)
                if cargo.user != user:
                    return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                cargo_attr_value = CargoAttributeValue.objects.get(pk=pk)
                serializer = CargoAttrValueCreateSerializer(cargo_attr_value, data=data)
                if serializer.is_valid():
                    serializer.save()
                    if CargoAttributeValue.objects.filter(pk=serializer.data['id']).exists():
                        attr_value = CargoAttributeValue.objects.get(pk=serializer.data['id'])
                        out_serializer = CargoAttrValueCreateOutSerializer(attr_value)
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

class CargoAttrValueDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Cargo attribute value delete."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if CargoAttributeValue.objects.filter(pk=pk).exists():
                attr_value = CargoAttributeValue.objects.get(pk=pk)
                cargo = attr_value.cargo
                if cargo.user != user:
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

class CargoCommentCreate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Create Cargo Comment",
        operation_description = "",
        request_body=CargoCommentCreateSerializer,
        responses={200:CargoCommentCreateOutSerializer}
    )
    def post(self, request):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            cargo_id = data["cargo"]
            cargo_id = int(cargo_id)

            if Cargo.objects.filter(pk=cargo_id).exists():
                serializer = CargoCommentCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    if CargoComment.objects.filter(pk=serializer.data['id']).exists():
                        comment = CargoComment.objects.get(pk=serializer.data['id'])
                        mobile_verified = comment.user.mobile_verified
                        email_verified = comment.user.email_verified
                        if mobile_verified or email_verified:
                            comment.is_active = True
                            comment.save()
                        out_serializer = CargoCommentCreateOutSerializer(comment)
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
        
class CargoCommentUpdate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Update Cargo Comment",
        operation_description = "",
        request_body=CargoCommentCreateSerializer,
        responses={200:CargoCommentCreateOutSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            cargo_id = data["cargo"]
            cargo_id = int(cargo_id)
            if Cargo.objects.filter(pk=cargo_id).exists():
                if CargoComment.objects.filter(pk=pk).exists():
                    comment = CargoComment.objects.get(pk=pk)
                    if comment.user != user:
                        return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                    serializer = CargoCommentCreateSerializer(comment, data=data)
                    if serializer.is_valid():
                        serializer.save()
                        mobile_verified = comment.user.mobile_verified
                        email_verified = comment.user.email_verified
                        if mobile_verified or email_verified:
                            comment.is_active = True
                            comment.save()
                        out_serializer = CargoCommentCreateOutSerializer(comment)
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

class CargoCommentDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS Required.",
        operation_summary="Cargo Comment Delete."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if CargoComment.objects.filter(pk=pk).exists():
                comment = CargoComment.objects.get(pk=pk)
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

class CargoRatingCreate(APIView):
    rating = openapi.Parameter('rating', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(
        operation_summary = "Cargo rating 1-5",
        operation_description="***IMPORTANT*** 'pk' is primary key of cargo.",
        manual_parameters=[rating]
    )
    def get(self, request, pk):
        try:
            if Cargo.objects.filter(pk=pk).exists():
                cargo = Cargo.objects.get(pk=pk)
                rating = request.query_params.get("rating", None)
                if not rating.isdigit():
                    return Response({
                        "response":"error",
                        "message": "'rating' need to be integer and between 1-5"
                    })
                rating = int(rating)
                rating_count = cargo.rating_count
                old_rating = cargo.rating
                new_rating = calculate_rating(old_rating, rating_count, rating)
                cargo.rating = round(new_rating, 2)
                cargo.rating_count = rating_count + 1
                cargo.save()
                return Response({"response":"success", "rating":cargo.rating})
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

class CargoSeenCount(APIView):
    @swagger_auto_schema(
        operation_summary = "Cargo seen count",
        operation_description="***IMPORTANT*** 'pk' is primary key of cargo."
    )
    def get(self, request, pk):
        try:
            if Cargo.objects.filter(pk=pk).exists():
                cargo = Cargo.objects.get(pk=pk)
                cargo.seen_count = cargo.seen_count + 1
                cargo.save()
                return Response({"response":"success", "seen_ccount":cargo.seen_count})
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
        
class CargoLikeCountAdd(APIView):
    @swagger_auto_schema(
        operation_summary = "Cargo like add",
        operation_description="***IMPORTANT*** 'pk' is primary key of cargo."
    )
    def get(self, request, pk):
        try:
            if Cargo.objects.filter(pk=pk).exists():
                cargo = Cargo.objects.get(pk=pk)
                cargo.like_count = cargo.like_count + 1
                cargo.save()
                return Response({
                    "response":"success",
                    "like_count": cargo.like_count
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

class CargoLikeCountRemove(APIView):
    @swagger_auto_schema(
        operation_summary = "Cargo like remove",
        operation_description="***IMPORTANT*** 'pk' is primary key of cargo."
    )
    def get(self, request, pk):
        try:
            if Cargo.objects.filter(pk=pk).exists():
                cargo = Cargo.objects.get(pk=pk)
                cargo.like_count = cargo.like_count - 1
                cargo.save()
                return Response({
                    "response":"success",
                    "like_count": cargo.like_count
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

class WarehouseList(APIView, LimitOffsetPagination):
    title = openapi.Parameter("title", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    description = openapi.Parameter("description", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    vip = openapi.Parameter('vip', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    likes = openapi.Parameter('likes', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    rating = openapi.Parameter('rating', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    created = openapi.Parameter('created', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    user = openapi.Parameter("user", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    attribute = openapi.Parameter("attribute", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    atrvalue = openapi.Parameter("atrvalue", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    warehouse_type = openapi.Parameter("warehouse_type", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    is_available = openapi.Parameter('is_available', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    minprice = openapi.Parameter("minprice", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    maxprice = openapi.Parameter("maxprice", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    country = openapi.Parameter("country", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    location = openapi.Parameter("location", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    mincapacity = openapi.Parameter("mincapacity", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    maxcapacity = openapi.Parameter("maxcapacity", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        manual_parameters=[title, description, vip, likes, rating, created,
                        user, attribute, atrvalue, warehouse_type, country, 
                        location, mincapacity, maxcapacity, minprice,
                        maxprice, is_available],
        operation_description="Authorizaton IS NOT required. \n\n" \
                        "***IMPORTANT*** 'rating', 'created' and 'likes' ordering should be used one at time.\n\n" \
                        "'warehouse_type', 'user' and 'attribute' need to be integer field.",
        operation_summary="Paginated List of Warehouse.",
        responses={200: WarehouseListSerializer}
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
            is_available = request.query_params.get("is_available", None)
            warehouse_type = request.query_params.get("warehouse_type", None)
            minprice = request.query_params.get("minprice", None)
            maxprice = request.query_params.get("maxprice", None)
            country = request.query_params.get("country", None)
            location = request.query_params.get("location", None)
            mincapacity = request.query_params.get("mincapacity", None)
            maxcapacity = request.query_params.get("maxcapacity", None)

            warehouses = Warehouse.objects.filter(is_active=True)

            if vip == "true":
                warehouses = warehouses.filter(is_vip=True)
            if vip == "false":
                warehouses = warehouses.filter(is_vip=False)

            if is_available == "true":
                warehouses = warehouses.filter(is_available=True)
            if is_available == "false":
                warehouses = warehouses.filter(is_available=False)

            if user:
                warehouses = warehouses.filter(user=user)
            
            if title:
                warehouses = warehouses.filter(Q(title_tm__icontains=title) | 
                                        Q(title_ru__icontains=title) |
                                        Q(title_en__icontains=title))
            if description:
                warehouses = warehouses.filter(Q(description_tm__icontains=description) |
                                    Q(description_ru__icontains=description) |
                                    Q(description_en__icontains=description))
            
            if country:
                warehouses = warehouses.filter(from_country__icontains=country)
            if location:
                warehouses = warehouses.filter(from_location__icontains=location)
            
            if warehouse_type:
                warehouses = warehouses.filter(warehouse_type=warehouse_type)
            
            if mincapacity and maxcapacity:
                warehouses = warehouses.filter(volume__range=[mincapacity, maxcapacity])
            
            if minprice and maxprice:
                warehouses = warehouses.filter(price__range=[minprice, maxprice])
            
            if attribute and atrvalue:
                attribute = int(attribute)
                atrvalue = str(atrvalue)
                warehouse_list = CargoAttributeValue.objects.filter(
                                        Q(attribute__id=attribute) &
                                        Q(value_tm__icontains=atrvalue)).values_list(
                                        'warehouse__pk',
                                        flat=True)
                warehouses = warehouses.filter(pk__in=warehouse_list)


            if rating == "true":
                warehouses = warehouses.order_by("-rating")
            if rating == "false":
                warehouses = warehouses.order_by("rating")
            if likes == "true":
                warehouses = warehouses.order_by("-like_count")
            if likes == "false":
                warehouses = warehouses.order_by("like_count")
            if created == "true":
                warehouses = warehouses.order_by("-created_at")
            if created == "false":
                warehouses = warehouses.order_by("created_at")

            data = self.paginate_queryset(warehouses, request, view=self)
            serializer = WarehouseListSerializer(data, many=True)
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

class WarehouseDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="Authorization IS NOT Required",
        operation_description="***IMPORTANT*** 'pk' IS primary key of warehouse.",
        responses={200: WarehouseDetailSerializer}
    )
    def get(self, request, pk):
        try:
            if Warehouse.objects.filter(pk=pk).exists():
                warehouse = Warehouse.objects.get(pk=pk)
                serializer = WarehouseDetailSerializer(warehouse)
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

class WarehouseCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS Required.",
            operation_summary="Create New Cargo.",
            request_body=WarehouseCreateSerializer,
            responses={200: WarehouseDetailSerializer}
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
            warehouse_type = data['warehouse_type']
            data['warehouse_type'] = int(warehouse_type)
            data._mutable = _mutable
            serializer = WarehouseCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                if Warehouse.objects.filter(pk=serializer.data['id']).exists():
                    warehouse = Warehouse.objects.get(pk=serializer.data["id"])
                    if mobile_verified or email_verified:
                        warehouse.is_active = True
                    warehouse.save()
                    out_serializer = WarehouseDetailSerializer(warehouse)
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
            
class WarehouseUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS Required.",
            operation_summary="Cargo Update.",
            request_body=WarehouseCreateSerializer,
            responses={200: WarehouseDetailSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            mobile_verified = user.mobile_verified
            email_verified = user.email_verified
            if Warehouse.objects.filter(pk=pk).exists():
                warehouse = Warehouse.objects.get(pk=pk)
                if warehouse.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                if mobile_verified or email_verified:
                    warehouse.is_active = True
                serializer = WarehouseCreateSerializer(warehouse, data=data)
                if serializer.is_valid():
                    serializer.save()
                    out_serializer = WarehouseDetailSerializer(warehouse)
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
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class WarehouseDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS Required.",
        operation_summary="Delete Warehouse."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if Warehouse.objects.filter(pk=pk).exists():
                warehouse = Warehouse.objects.get(pk=pk)
                if warehouse.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                warehouse.delete()
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

class WarehouseAttrValueCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Create Cargo Attr Value.",
        request_body=WarehouseAttrValueCreateSerializer,
        responses={200:WarehouseAttrValueCreateOutSerializer}
    )
    def post(self, request):
        try:
            user = request.user
            data = request.data
            warehouse_id = data["warehouse"]
            attr_id = data["attribute"]
            warehouse_id = int(warehouse_id)
            attr_id = int(attr_id)
            if Warehouse.objects.filter(pk=warehouse_id).exists() and \
                WarehouseAttribute.objects.filter(pk=attr_id).exists():
                warehouse = Warehouse.objects.get(pk=warehouse_id)
                if warehouse.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                serializer = WarehouseAttrValueCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    if WarehouseAttributeValue.objects.filter(pk=serializer.data['id']).exists():
                        attr_value = WarehouseAttributeValue.objects.get(pk=serializer.data['id'])
                        out_serializer = WarehouseAttrValueCreateOutSerializer(attr_value)
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

class WarehouseAttrValueUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Create Cargo Attr Value.",
        request_body=WarehouseAttrValueCreateSerializer,
        responses={200:WarehouseAttrValueCreateOutSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            warehouse_id = data["warehouse"]
            attr_id = data["attribute"]
            warehouse_id = int(warehouse_id)
            attr_id = int(attr_id)
            if Warehouse.objects.filter(pk=warehouse_id).exists() and \
                WarehouseAttribute.objects.filter(pk=attr_id).exists():
                warehouse = Warehouse.objects.get(pk=warehouse_id)
                if warehouse.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                warehouse_attr_value = WarehouseAttributeValue.objects.get(pk=pk)
                serializer = WarehouseAttrValueCreateSerializer(warehouse_attr_value, data=data)
                if serializer.is_valid():
                    serializer.save()
                    if WarehouseAttributeValue.objects.filter(pk=serializer.data['id']).exists():
                        attr_value = WarehouseAttributeValue.objects.get(pk=serializer.data['id'])
                        out_serializer = WarehouseAttrValueCreateOutSerializer(attr_value)
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

class WarehouseAttrValueDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Warehouse attribute value delete."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if WarehouseAttributeValue.objects.filter(pk=pk).exists():
                attr_value = WarehouseAttributeValue.objects.get(pk=pk)
                warehouse = attr_value.warehouse
                if warehouse.user != user:
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
             
class WarehouseCommentCrate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Create Driver Comment",
        operation_description = "",
        request_body=WarehouseCommentCreateSerializer,
        responses={200:WarehouseCommentCreateOutSerializer}
    )
    def post(self, request):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            warehouse_id = data["warehouse"]
            warehouse_id = int(warehouse_id)

            if Warehouse.objects.filter(pk=warehouse_id).exists():
                serializer = WarehouseCommentCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    if WarehouseComment.objects.filter(pk=serializer.data['id']).exists():
                        warehouse = WarehouseComment.objects.get(pk=serializer.data['id'])
                        mobile_verified = warehouse.user.mobile_verified
                        email_verified = warehouse.user.email_verified
                        if mobile_verified or email_verified:
                            warehouse.is_active = True
                            warehouse.save()
                        out_serializer = WarehouseCommentCreateOutSerializer(warehouse)
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

class WarehouseCommentUpdate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Create Driver Comment",
        operation_description = "",
        request_body=WarehouseCommentCreateSerializer,
        responses={200:WarehouseCommentCreateOutSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            warehouse_id = data["warehouse"]
            warehouse_id = int(warehouse_id)
            if Warehouse.objects.filter(pk=warehouse_id).exists():
                if WarehouseComment.objects.filter(pk=pk).exists():
                    comment = WarehouseComment.objects.get(pk=pk)
                    if comment.user != user:
                        return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                    serializer = WarehouseCommentCreateSerializer(comment, data=data)
                    if serializer.is_valid():
                        serializer.save()
                        mobile_verified = comment.user.mobile_verified
                        email_verified = comment.user.email_verified
                        if mobile_verified or email_verified:
                            comment.is_active = True
                            comment.save()
                        out_serializer = WarehouseCommentCreateOutSerializer(comment)
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
        
class WarehouseCommentDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS Required.",
        operation_summary="Warehouse Comment Delete."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if WarehouseComment.objects.filter(pk=pk).exists():
                comment = WarehouseComment.objects.get(pk=pk)
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

class WarehouseRatingCreate(APIView):
    rating = openapi.Parameter('rating', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(
        operation_summary = "Warehouse rating 1-5",
        operation_description="***IMPORTANT*** 'pk' is primary key of warehouse.",
        manual_parameters=[rating]
    )
    def get(self, request, pk):
        try:
            if Warehouse.objects.filter(pk=pk).exists():
                warehouse = Warehouse.objects.get(pk=pk)
                rating = request.query_params.get("rating", None)
                if not rating.isdigit():
                    return Response({
                        "response":"error",
                        "message": "'rating' need to be integer and between 1-5"
                    })
                rating = int(rating)
                rating_count = warehouse.rating_count
                old_rating = warehouse.rating
                new_rating = calculate_rating(old_rating, rating_count, rating)
                warehouse.rating = round(new_rating, 2)
                warehouse.rating_count = rating_count + 1
                warehouse.save()
                return Response({"response":"success", "rating":warehouse.rating})
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
        
class WarehouseSeenCount(APIView):
    @swagger_auto_schema(
        operation_summary = "Warehouse seen count",
        operation_description="***IMPORTANT*** 'pk' is primary key of warehouse."
    )
    def get(self, request, pk):
        try:
            if Warehouse.objects.filter(pk=pk).exists():
                warehouse = Warehouse.objects.get(pk=pk)
                warehouse.seen_count = warehouse.seen_count + 1
                warehouse.save()
                return Response({"response":"success", "seen_ccount":warehouse.seen_count})
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
        
class WarehouseLikeCountAdd(APIView):
    @swagger_auto_schema(
        operation_summary = "Warehouse like add",
        operation_description="***IMPORTANT*** 'pk' is primary key of warehouse."
    )
    def get(self, request, pk):
        try:
            if Warehouse.objects.filter(pk=pk).exists():
                warehouse = Warehouse.objects.get(pk=pk)
                warehouse.like_count = warehouse.like_count + 1
                warehouse.save()
                return Response({
                    "response":"success",
                    "like_count": warehouse.like_count
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

class WarehouseLikeCountRemove(APIView):
    @swagger_auto_schema(
        operation_summary = "Warehouse like remove",
        operation_description="***IMPORTANT*** 'pk' is primary key of warehouse."
    )
    def get(self, request, pk):
        try:
            if Warehouse.objects.filter(pk=pk).exists():
                warehouse = Warehouse.objects.get(pk=pk)
                warehouse.like_count = warehouse.like_count - 1
                warehouse.save()
                return Response({
                    "response":"success",
                    "like_count": warehouse.like_count
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

class TransportList(APIView, LimitOffsetPagination):
    title = openapi.Parameter("title", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    description = openapi.Parameter("description", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    vip = openapi.Parameter('vip', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    likes = openapi.Parameter('likes', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    rating = openapi.Parameter('rating', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    created = openapi.Parameter('created', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    is_local = openapi.Parameter('is_local', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    user = openapi.Parameter("user", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    attribute = openapi.Parameter("attribute", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    atrvalue = openapi.Parameter("atrvalue", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    vehicle_type = openapi.Parameter("vehicle_type", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    from_country = openapi.Parameter("from_country", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    from_location = openapi.Parameter("from_location", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    to_country = openapi.Parameter("to_country", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    to_location = openapi.Parameter("to_location", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    minprice = openapi.Parameter("minprice", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    maxprice = openapi.Parameter("maxprice", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(
        manual_parameters=[title, description, vip, likes, rating, created,
                        user, attribute, atrvalue, vehicle_type, from_country, 
                        from_location, to_country, to_location, minprice, 
                        maxprice, is_local],
        operation_description="Authorizaton IS NOT required. \n\n" \
                        "***IMPORTANT*** 'rating', 'created' and 'likes' ordering should be used one at time.\n\n" \
                        "'category', 'user' and 'attribute' need to be integer field.",
        operation_summary="Paginated List of Cargos.",
        responses={200: TransportListSerializer}
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
            from_country = request.query_params.get("from_country", None)
            from_location = request.query_params.get("from_location", None)
            to_country = request.query_params.get("to_country", None)
            to_location = request.query_params.get("to_location", None)
            minprice = request.query_params.get("minprice", None)
            maxprice = request.query_params.get("maxprice", None)
            is_local = request.query_params.get("is_local", None)

            transport = Transport.objects.filter(is_active=True)
            
            if vip == "true":
                transport = transport.filter(is_vip=True)
            if vip == "false":
                transport = transport.filter(is_vip=False)
            
            if is_local == "true":
                transport = transport.filter(is_local=True)
            if is_local == "false":
                transport = transport.filter(is_local=False)
            
            if user:
                transport = transport.filter(user=user)
            
            if title:
                transport = transport.filter(Q(title_tm__icontains=title) | 
                                        Q(title_ru__icontains=title) |
                                        Q(title_en__icontains=title))
            if description:
                transport = transport.filter(Q(description_tm__icontains=description) |
                                    Q(description_ru__icontains=description) |
                                    Q(description_en__icontains=description))
            
            if from_country:
                transport = transport.filter(from_country__icontains=from_country)
            if from_location:
                transport = transport.filter(from_location__icontains=from_location)
            if to_country:
                transport = transport.filter(to_country__icontains=to_country)
            if to_location:
                transport = transport.filter(to_location__icontains=to_location)
            
            if vehicle_type:
                transport = transport.filter(vehicle_type=vehicle_type)
            
            if minprice and maxprice:
                transport = transport.filter(price__range=[minprice, maxprice])
            
            if attribute and atrvalue:
                attribute = int(attribute)
                atrvalue = str(atrvalue)
                transport_list = TransportAttributeValue.objects.filter(
                                        Q(attribute__id=attribute) &
                                        Q(value_tm__icontains=atrvalue)).values_list(
                                        'transport__pk',
                                        flat=True)
                transport = transport.filter(pk__in=transport_list)
            
            if rating == "true":
                transport = transport.order_by("-rating")
            if rating == "false":
                transport = transport.order_by("rating")
            if likes == "true":
                transport = transport.order_by("-like_count")
            if likes == "false":
                transport = transport.order_by("like_count")
            if created == "true":
                transport = transport.order_by("-created_at")
            if created == "false":
                transport = transport.order_by("created_at")
            
            data = self.paginate_queryset(transport, request, view=self)
            serializer = TransportListSerializer(data, many=True)
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

class TransportDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="Authorization IS NOT Required",
        operation_description="***IMPORTANT*** 'pk' IS primary key of transport.",
        responses={200: TransportDetailSerializer}
    )
    def get(self, request, pk):
        try:
            if Transport.objects.filter(pk=pk).exists():
                warehouse = Transport.objects.get(pk=pk)
                serializer = TransportDetailSerializer(warehouse)
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

class TransportCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS Required.",
            operation_summary="Create New Transport.",
            request_body=TransportCreateSerializer,
            responses={200: TransportDetailSerializer}
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
            serializer = TransportCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                if Transport.objects.filter(pk=serializer.data["id"]).exists():
                    transport = Transport.objects.get(pk=serializer.data["id"])
                    if mobile_verified or email_verified:
                        transport.is_active = True
                    transport.save()
                    out_serializer = TransportDetailSerializer(transport)
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

class TransportUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS Required.",
            operation_summary="Update Transport.",
            request_body=TransportCreateSerializer,
            responses={200: TransportDetailSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            mobile_verified = user.mobile_verified
            email_verified = user.email_verified
            if Transport.objects.filter(pk=pk).exists():
                transport = Transport.objects.get(pk=pk)
                if transport.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                if mobile_verified or email_verified:
                    transport.is_active = True
                serializer = TransportCreateSerializer(transport, data=data)
                if serializer.is_valid():
                    serializer.save()
                    out_serializer = TransportDetailSerializer(transport)
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
        except:
            return Response({
                "response":"error",
                "message": MSG_UNKNOWN_ERROR
            }, status=status.HTTP_400_BAD_REQUEST)

class TransportDelete(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_description="Authorization IS Required.",
        operation_summary="Delete Transport."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if Transport.objects.filter(pk=pk).exists():
                transport = Transport.objects.get(pk=pk)
                if transport.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                transport.delete()
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

class TransportAttrValueCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Create Transport Attr Value.",
        request_body=TransportAttrValueCreateSerializer,
        responses={200:TransportAttrValueCreateOutSerializer}
    )
    def post(self, request):
        try:
            user = request.user
            data = request.data
            transport_id = data["transport"]
            attr_id = data["attribute"]
            transport_id = int(transport_id)
            attr_id = int(attr_id)
            if Transport.objects.filter(pk=transport_id).exists() and \
                TransportAttribute.objects.filter(pk=attr_id).exists():
                transport = Transport.objects.get(pk=transport_id)
                if transport.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                serializer = TransportAttrValueCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    if TransportAttributeValue.objects.filter(pk=serializer.data["id"]).exists():
                        attr_value = TransportAttributeValue.objects.get(pk=serializer.data['id'])
                        out_serializer = TransportAttrValueCreateOutSerializer(attr_value)
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

class TransportAttrValueUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Update Transport Attr Value.",
        request_body=TransportAttrValueCreateSerializer,
        responses={200:TransportAttrValueCreateOutSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            transport_id = data["transport"]
            attr_id = data["attribute"]
            transport_id = int(transport_id)
            attr_id = int(attr_id)
            if Transport.objects.filter(pk=transport_id).exists() and \
                TransportAttribute.objects.filter(pk=attr_id).exists():
                transport = Transport.objects.get(pk=transport_id)
                if transport.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                transport_attr_value = TransportAttributeValue.objects.get(pk=pk)
                serializer = TransportAttrValueCreateSerializer(transport_attr_value, data=data)
                if serializer.is_valid():
                    serializer.save()
                    if TransportAttributeValue.objects.filter(pk=serializer.data['id']).exists():
                        attr_value = TransportAttributeValue.objects.get(pk=serializer.data['id'])
                        out_serializer = TransportAttrValueCreateOutSerializer(attr_value)
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

class TransportAttrValueDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Transport attribute value delete."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if TransportAttributeValue.objects.filter(pk=pk).exists():
                attr_value = TransportAttributeValue.objects.get(pk=pk)
                transport = attr_value.transport
                if transport.user != user:
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

class TransportCommentCreate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Create Cargo Comment",
        operation_description = "",
        request_body=TransportCommentCreateSerializer,
        responses={200:TransportCommentCreateOutSerializer}
    )
    def post(self, request):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            transport_id = data["transport"]
            transport_id = int(transport_id)

            if Transport.objects.filter(pk=transport_id).exists():
                serializer = TransportCommentCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    if TransportComment.objects.filter(pk=serializer.data['id']).exists():
                        comment = TransportComment.objects.get(pk=serializer.data['id'])
                        mobile_verified = comment.user.mobile_verified
                        email_verified = comment.user.email_verified
                        if mobile_verified or email_verified:
                            comment.is_active = True
                            comment.save()
                        out_serializer = TransportCommentCreateOutSerializer(comment)
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

class TransportCommentUpdate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Update Cargo Comment",
        operation_description = "",
        request_body=TransportCommentCreateSerializer,
        responses={200:TransportCommentCreateOutSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            transport_id = data["transport"]
            transport_id = int(transport_id)

            if Transport.objects.filter(pk=transport_id).exists():
                if TransportComment.objects.filter(pk=pk).exists():
                    comment = TransportComment.objects.get(pk=pk)
                    if comment.user != user:
                        return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                    serializer = TransportCommentCreateSerializer(comment, data=data)
                    if serializer.is_valid():
                        serializer.save()
                        mobile_verified = comment.user.mobile_verified
                        email_verified = comment.user.email_verified
                        if mobile_verified or email_verified:
                            comment.is_active = True
                            comment.save()
                        out_serializer = TransportCommentCreateOutSerializer(comment)
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

class TransportCommentDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS Required.",
        operation_summary="Transport Comment Delete."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if TransportComment.objects.filter(pk=pk).exists():
                comment = TransportComment.objects.get(pk=pk)
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

class TransportRatingCreate(APIView):
    rating = openapi.Parameter('rating', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(
        operation_summary = "Transport rating 1-5",
        operation_description="***IMPORTANT*** 'pk' is primary key of transport.",
        manual_parameters=[rating]
    )
    def get(self, request, pk):
        try:
            if Transport.objects.filter(pk=pk).exists():
                transport = Transport.objects.get(pk=pk)
                rating = request.query_params.get("rating", None)
                if not rating.isdigit():
                    return Response({
                        "response":"error",
                        "message": "'rating' need to be integer and between 1-5"
                    })
                rating = int(rating)
                rating_count = transport.rating_count
                old_rating = transport.rating
                new_rating = calculate_rating(old_rating, rating_count, rating)
                transport.rating = round(new_rating, 2)
                transport.rating_count = rating_count + 1
                transport.save()
                return Response({"response":"success", "rating":transport.rating})
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

class TransportSeenCount(APIView):
    @swagger_auto_schema(
        operation_summary = "Transport seen count",
        operation_description="***IMPORTANT*** 'pk' is primary key of transport."
    )
    def get(self, request, pk):
        try:
            if Transport.objects.filter(pk=pk).exists():
                transport = Transport.objects.get(pk=pk)
                transport.seen_count = transport.seen_count + 1
                transport.save()
                return Response({"response":"success", "seen_ccount":transport.seen_count})
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
        
class TransportLikeCountAdd(APIView):
    @swagger_auto_schema(
        operation_summary = "Transport like add",
        operation_description="***IMPORTANT*** 'pk' is primary key of transport."
    )
    def get(self, request, pk):
        try:
            if Transport.objects.filter(pk=pk).exists():
                transport = Transport.objects.get(pk=pk)
                transport.like_count = transport.like_count + 1
                transport.save()
                return Response({
                    "response":"success",
                    "like_count": transport.like_count
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

class TransportLikeCountRemove(APIView):
    @swagger_auto_schema(
        operation_summary = "Transport like remove",
        operation_description="***IMPORTANT*** 'pk' is primary key of transport."
    )
    def get(self, request, pk):
        try:
            if Transport.objects.filter(pk=pk).exists():
                transport = Transport.objects.get(pk=pk)
                transport.like_count = transport.like_count - 1
                transport.save()
                return Response({
                    "response":"success",
                    "like_count": transport.like_count
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


