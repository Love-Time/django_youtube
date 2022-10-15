from django.urls import path, include, re_path
from . import views
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'video', VideoViewSet)
router.register(r'profile', UserViewSet)

urlpatterns = [
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('<int:pk>/', views.get_video, name='video'),
    path('', views.get_list_video, name='home'),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),

    # path('api/v1/video/', include(router.urls)),
    # path('api/v1/video/', include(router.urls)),
    # path('api/v1/video/<int:pk>/', VideoViewSet.as_view())

    # path('api/v1/videolist/', VideoApiList.as_view()),
    # path('api/v1/videolist/<int:pk>/', VideoApiDetailView.as_view()),

    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken'))
]
