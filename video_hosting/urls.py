from django.urls import path, include
from . import views
from .views import *
from rest_framework import routers


urlpatterns = [
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('<int:pk>/', views.get_video, name='video'),
    path('', views.get_list_video, name='home'),

    path('api/v1/video/',VideoApiList.as_view()),
    path('api/v1/video/<int:pk>/',VideoApiDetailView.as_view())

    # path('api/v1/videolist/', VideoApiList.as_view()),
    # path('api/v1/videolist/<int:pk>/', VideoApiDetailView.as_view()),
]