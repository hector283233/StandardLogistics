from django.urls import path

from . import views

urlpatterns = [
    path('banner-list/', views.BannerList.as_view(), name='banner-list'),
    path('category-list/', views.CategoryListView.as_view(),
         name="category-list"),
    path('ads-list/', views.AdvertisementList.as_view(), name='ads-list'),
    path('ads-detail/<int:pk>/', views.AdvertisementDetail.as_view(),
         name="ads-detail"),
    path('ads-create/', views.AdvertisementCreate.as_view(),
         name='ads-create'),
    path('ads-update/<int:pk>/', views.AdvertisementUpdate.as_view(),
         name="ads-update"),
    path('ads-delete/<int:pk>/', views.AdvertisementDelete.as_view(),
         name='ads-delete'),
    path('ads-attr-value-create/', views.ADAttrValueCreate.as_view(),
         name='ads-attr-value-create'),
    path('ads-attr-value-update/<int:pk>/', views.ADAttrValueUpdate.as_view(),
         name="ads-attr-value-update"),
    path('ads-attr-value-delete/<int:pk>/', views.ADAttrValueDelete.as_view(),
         name='ads-attr-value-delete'),
    path('ads-comment-create/', views.ADCommentCreate.as_view(),
         name='ads-comment-create'),
    path('ads-comment-update/<int:pk>/', views.ADCommentUpdate.as_view(),
         name='ads-comment-update'),
    path('ads-comment-delete/<int:pk>/', views.ADCommentDelete.as_view(),
         name='ads-comment-delete'),
    path('ads-rate/<int:pk>/', views.ADRatingCreate.as_view(),
         name="ads-rate"),
    path('ads-seen-count/<int:pk>/', views.ADSeenCount.as_view(),
         name="ads-seen-count"),
    path('ads-like-count-add/<int:pk>/', views.ADLikeCountAdd.as_view(),
         name="ads-like-count-add"),
    path('ads-like-count-remove/<int:pk>/', views.ADLikeCountRemove.as_view(),
         name="ads-like-count-remove"),
    path('ads-attributes-list/', views.ADAttributeList.as_view(),
         name='ads-attributes-list'),
]