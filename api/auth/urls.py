from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('change-password/', views.ChangePassword.as_view(), name='change-password'),
    # path('forgot-password/', views.ForgotPassword.as_view(), name='forgot-password'),
    path('user-update/', views.UpdateUser.as_view(), name='user-update'),
    path('profile-update/', views.UpdateProfile.as_view(), name='profile-update'),
    path('user-detail/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('user-list/', views.UserListPaginated.as_view(), name='user-list'),
    path('business-list/', views.BusinessAccountList.as_view(),
         name='business-list'),
    path('business-create/', views.BusinessAccountCreate.as_view(),
         name='business-create'),
    path('business-detail/<int:pk>/', views.BusinessAccountDetail.as_view(),
         name="business-detail"),
    path('business-update/<int:pk>/', views.BusinessAccountUpdate.as_view(),
         name="business-update"),
    path('business-delete/<int:pk>/', views.BusinessAccountDelete.as_view(),
         name="business-delete"),
    path('ba-attr-value-create', views.BAAttrValueCreate.as_view(), 
         name='ba-attr-value-create'),
    path('ba-attr-value-update/<int:pk>/', views.BAAttrValueUpdate.as_view(),
         name='ba-attr-value-update'),
    path('ba-attr-value-delete/<int:pk>/', views.BAAttrValueDelete.as_view(),
         name='ba-attr-value-delete'),
    path('ba-rate/<int:pk>/', views.BARatingCreate.as_view(), name='ba-rate'),
    path('ba-seen-count/<int:pk>/', views.BASeenCount.as_view(), name='ba-seen-count'),
]