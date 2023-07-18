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
]