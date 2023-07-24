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

from advertisement.models import *
from .serializers import *
from api.utils import *

class ADAttributeList(APIView):
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        responses={200: ADAttributesListSerializer}
    )
    def get(self, request):
        attributes = AD_Attribute.objects.all()
        serializer = ADAttributesListSerializer(attributes, many=True)
        return Response({
            "response":"success",
            "data": serializer.data
        })
    
class BannerList(APIView):
    created = openapi.Parameter('created', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    type = openapi.Parameter('type', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    category = openapi.Parameter('category', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(
        operation_description="Authorization IS NOT required.",
        operation_summary="Banner list, not paginated",
        manual_parameters=[created, type, category],
        responses={200: BannerListSerializer}
    )
    def get(self, request):
        created = request.query_params.get("created", None)
        type = request.query_params.get("type", None)
        category = request.query_params.get("category", None)
        banners = Banner.objects.filter(is_active=True)
        if type:
            type = int(type)
            banners = banners.filter(type=type)
        if category:
            category = int(category)
            banners = banners.filter(category=category)
        if created == 'true':
            banners = banners.order_by("-created_at")
        if created == "false":
            banners = banners.order_by("created_at")

        serializer = BannerListSerializer(banners, many=True)
        return Response({
            "response":"success",
            "data": serializer.data
        })

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response({
            "response":"success",
            "data": serializer.data
        })

class AdvertisementList(APIView, LimitOffsetPagination):
    title = openapi.Parameter("title", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    description = openapi.Parameter("description", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    vip = openapi.Parameter('vip', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    likes = openapi.Parameter('likes', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    rating = openapi.Parameter('rating', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    created = openapi.Parameter('created', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
    user = openapi.Parameter("user", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    category = openapi.Parameter("category", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    minprice = openapi.Parameter("minprice", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    maxprice = openapi.Parameter("maxprice", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    attribute = openapi.Parameter("attribute", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    atrvalue = openapi.Parameter("atrvalue", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    @swagger_auto_schema(
        manual_parameters=[title, description, vip, likes, rating, created,
                           user, category, minprice, maxprice, attribute, atrvalue],
        operation_summary="Paginated list of advertisements.",
        operation_description="Authorizaton IS NOT required. \n\n" \
                        "***IMPORTANT*** 'rating', 'created' and 'likes' ordering should be used one at time.\n\n" \
                        "'category', 'user', 'minprice', 'maxprice', 'attribute' need to be integer field.",
        responses={200:AdvertisementListSerializer}
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
            category = request.query_params.get("category", None)
            minprice = request.query_params.get("minprice", None)
            maxprice = request.query_params.get("maxprice", None)

            advertisements = Advertisement.objects.filter(is_active=True)

            if vip == "true":
                advertisements = advertisements.filter(is_vip=True)
            if vip == "false":
                advertisements = advertisements.filter(is_vip=False)
            
            if category:
                advertisements = advertisements.filter(category=category)
            
            if user:
                advertisements = advertisements.filter(user=user)
            
            if title:
                advertisements = advertisements.filter(Q(title_tm__icontains=title) | 
                                                    Q(title_ru__icontains=title) |
                                                    Q(title_en__icontains=title))
            if description:
                advertisements = advertisements.filter(Q(description_tm__icontains=description) |
                                                    Q(description_ru__icontains=description) |
                                                    Q(description_en__icontains=description))
            if attribute and atrvalue:
                attribute = int(attribute)
                atrvalue = str(atrvalue)
                ad_list = AD_Attribute_Value.objects.filter(
                                        Q(attribute__id=attribute) &
                                        Q(value_tm__icontains=atrvalue)).values_list(
                                        'advertisement__pk',
                                        flat=True)
                advertisements = advertisements.filter(pk__in=ad_list)
                
            if rating == "true":
                advertisements = advertisements.order_by("-rating")
            if rating == "false":
                advertisements = advertisements.order_by("rating")
            if likes == "true":
                advertisements = advertisements.order_by("-like_count")
            if likes == "false":
                advertisements = advertisements.order_by("like_count")
            if created == "true":
                advertisements = advertisements.order_by("-created_at")
            if created == "false":
                advertisements = advertisements.order_by("created_at")
            
            
            if minprice and maxprice:
                advertisements = advertisements.filter(price__range=(minprice, maxprice))
            
            data = self.paginate_queryset(advertisements, request, view=self)
            serializer = AdvertisementListSerializer(data, many=True)
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
    
class AdvertisementDetail(APIView):
    @swagger_auto_schema(
        operation_summary="Authorization IS NOT Required",
        operation_description="***IMPORTANT*** 'pk' IS primary key of advertisement.",
        responses={200: AdvertisementListSerializer}
    )
    def get(self, request, pk):
        try:
            if Advertisement.objects.filter(pk=pk).exists():
                advertisement = Advertisement.objects.get(pk=pk)
                serializer = AdvertisementListSerializer(advertisement)
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
        
class AdvertisementCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS Required.",
            operation_summary="Create New Advertisement.",
            request_body=AdvertisementCreateSerializer,
            responses={200: AdvertisementListSerializer}
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
            data._mutable = _mutable
            serializer = AdvertisementCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                if Advertisement.objects.filter(pk=serializer.data['id']).exists():
                    advertisement = Advertisement.objects.get(pk=serializer.data['id'])
                    if mobile_verified or email_verified:
                        advertisement.is_active = True
                    advertisement.save()
                    user.ads_count = user.ads_count + 1
                    user.save()
                    out_serializer = AdvertisementListSerializer(advertisement)
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

class AdvertisementUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
            operation_description="Authorization IS Required.",
            operation_summary="Advertisement Update.",
            request_body=AdvertisementCreateSerializer,
            responses={200: AdvertisementListSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            mobile_verified = user.mobile_verified
            email_verified = user.email_verified
            if Advertisement.objects.filter(pk=pk).exists():
                advertisement = Advertisement.objects.get(pk=pk)
                if advertisement.user != user:
                    return Response({
                        "response":"error",
                        "message": MSG_NOT_BELONG_TO_USER
                    })
                if mobile_verified or email_verified:
                    advertisement.is_active = True
                serializer = AdvertisementCreateSerializer(advertisement, data=data)
                if serializer.is_valid():
                    serializer.save()
                    out_serializer = AdvertisementListSerializer(advertisement)
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

class AdvertisementDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS Required.",
        operation_summary="Advertisement Delete."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if Advertisement.objects.filter(pk=pk).exists():
                advertisement = Advertisement.objects.get(pk=pk)
                if advertisement.user != user:
                    return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                advertisement.delete()
                user.ads_count = user.ads_count - 1
                user.save()
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

class ADAttrValueCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Create Advertisement.",
        request_body=ADAttributeValueCreateSerializer,
        responses={200:ADAttributeValueOutSerializer}
    )
    def post(self, request):
        try:
            user = request.user
            data = request.data
            ad_id = data["advertisement"]
            attr_id = data["attribute"]
            ad_id = int(ad_id)
            attr_id = int(attr_id)
            if Advertisement.objects.filter(pk=ad_id).exists() and \
                AD_Attribute.objects.filter(pk=attr_id).exists():
                advertisement = Advertisement.objects.get(pk=ad_id)
                if advertisement.user != user:
                    return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                serializer = ADAttributeValueCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    if AD_Attribute_Value.objects.filter(pk=serializer.data['id']).exists():
                        attr_value = AD_Attribute_Value.objects.get(pk=serializer.data['id'])
                        out_serializer = ADAttributeValueOutSerializer(attr_value)
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

class ADAttrValueUpdate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Update Advertisement.",
        request_body=ADAttributeValueCreateSerializer,
        responses={200:ADAttributeValueOutSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            ad_id = data["advertisement"]
            attr_id = data["attribute"]
            ad_id = int(ad_id)
            attr_id = int(attr_id)
            if Advertisement.objects.filter(pk=ad_id).exists() and \
                AD_Attribute.objects.filter(pk=attr_id).exists():
                advertisement = Advertisement.objects.get(pk=ad_id)
                if advertisement.user != user:
                    return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                ad_attr_value = AD_Attribute_Value.objects.get(pk=pk)
                serializer = ADAttributeValueCreateSerializer(ad_attr_value, data=data)
                if serializer.is_valid():
                    serializer.save()
                    if AD_Attribute_Value.objects.filter(pk=serializer.data['id']).exists():
                        attr_value = AD_Attribute_Value.objects.get(pk=serializer.data['id'])
                        out_serializer = ADAttributeValueUOutSerializer(attr_value)
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
        

class ADAttrValueDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS required.",
        operation_summary="Advertisement attribute value delete."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if AD_Attribute_Value.objects.filter(pk=pk).exists():
                attr_value = AD_Attribute_Value.objects.get(pk=pk)
                advertisement = attr_value.advertisement
                if advertisement.user != user:
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

class ADCommentCreate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Create Advertisement Comment",
        operation_description = "",
        request_body=ADCommentCreateSerializer,
        responses={200:ADCommentCreateOutSerializer}
    )
    def post(self, request):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            ad_id = data["advertisement"]
            ad_id = int(ad_id)
            if Advertisement.objects.filter(pk=ad_id).exists():
                serializer = ADCommentCreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    if AD_Comment.objects.filter(pk=serializer.data['id']).exists():
                        comment = AD_Comment.objects.get(pk=serializer.data["id"])
                        mobile_verified = comment.user.mobile_verified
                        email_verified = comment.user.email_verified
                        if mobile_verified or email_verified:
                            comment.is_active = True
                            comment.save()
                        out_serializer = ADCommentCreateOutSerializer(comment)
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

class ADCommentUpdate(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary = "Update Advertisement Comment",
        operation_description = "",
        request_body=ADCommentCreateSerializer,
        responses={200:ADCommentCreateOutSerializer}
    )
    def put(self, request, pk):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            ad_id = data["advertisement"]
            ad_id = int(ad_id)
            if Advertisement.objects.filter(pk=ad_id).exists():
                if AD_Comment.objects.filter(pk=pk).exists():
                    comment = AD_Comment.objects.get(pk=pk)
                    if comment.user != user:
                        return Response({
                            "response":"error",
                            "message": MSG_NOT_BELONG_TO_USER
                        })
                    serializer = ADCommentCreateSerializer(comment, data=data)
                    if serializer.is_valid():
                        serializer.save()
                        mobile_verified = comment.user.mobile_verified
                        email_verified = comment.user.email_verified
                        if mobile_verified or email_verified:
                            comment.is_active = True
                            comment.save()
                        out_serializer = ADCommentOutSerializer(comment)
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
        
class ADCommentDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Authorization IS Required.",
        operation_summary="Advertisement Comment Delete."
    )
    def delete(self, request, pk):
        try:
            user = request.user
            if AD_Comment.objects.filter(pk=pk).exists():
                comment = AD_Comment.objects.get(pk=pk)
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
        
class ADRatingCreate(APIView):
    rating = openapi.Parameter('rating', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    @swagger_auto_schema(
        operation_summary = "Advertisement rating 1-5",
        operation_description="***IMPORTANT*** 'pk' is primary key of advertisement.",
        manual_parameters=[rating]
    )
    def get(self, request, pk):
        try:
            if Advertisement.objects.filter(pk=pk).exists():
                advertisement = Advertisement.objects.get(pk=pk)
                rating = request.query_params.get("rating", None)
                if not rating.isdigit():
                    return Response({
                        "response":"error",
                        "message": "'rating' need to be integer and between 1-5"
                    })
                rating = int(rating)
                rating_count = advertisement.rating_count
                old_rating = advertisement.rating
                new_rating = calculate_rating(old_rating, rating_count, rating)
                advertisement.rating = round(new_rating, 2)
                advertisement.rating_count = rating_count + 1
                advertisement.save()
                return Response({"response":"success", "rating":advertisement.rating})
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

class ADSeenCount(APIView):
    @swagger_auto_schema(
        operation_summary = "Advertisement seen count",
        operation_description="***IMPORTANT*** 'pk' is primary key of advertisement."
    )
    def get(self, request, pk):
        if Advertisement.objects.filter(pk=pk).exists():
            advertisement = Advertisement.objects.get(pk=pk)
            advertisement.seen_count = advertisement.seen_count + 1
            advertisement.save()
            return Response({"response":"success", "seen_ccount":advertisement.seen_count})
        else:
            return Response({
                    "response":"error",
                    "message": MSG_OBJECT_NOT_FOUND
                })

class ADLikeCountAdd(APIView):
    @swagger_auto_schema(
        operation_summary = "Advertisement like add",
        operation_description="***IMPORTANT*** 'pk' is primary key of advertisement."
    )
    def get(self, request, pk):
        if Advertisement.objects.filter(pk=pk).exists():
            advertisement = Advertisement.objects.get(pk=pk)
            advertisement.like_count = advertisement.like_count + 1
            advertisement.save()
            return Response({
                "response":"success",
                "like_count": advertisement.like_count
            })
        else:
            return Response({
                    "response":"error",
                    "message": MSG_OBJECT_NOT_FOUND
                })

class ADLikeCountRemove(APIView):
    @swagger_auto_schema(
        operation_summary = "Advertisement like remove",
        operation_description="***IMPORTANT*** 'pk' is primary key of advertisement."
    )
    def get(self, request, pk):
        if Advertisement.objects.filter(pk=pk).exists():
            advertisement = Advertisement.objects.get(pk=pk)
            advertisement.like_count = advertisement.like_count - 1
            advertisement.save()
            return Response({
                "response":"success",
                "like_count": advertisement.like_count
            })
        else:
            return Response({
                    "response":"error",
                    "message": MSG_OBJECT_NOT_FOUND
                })