from django.urls import path, include

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('ads/', include('api.advertisement.urls')),
    path('service/', include('api.service.urls')),
]