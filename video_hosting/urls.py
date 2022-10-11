from django.urls import path, include
from . import views
from .views import VideoViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'video', VideoViewSet)



urlpatterns = [
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('<int:pk>/', views.get_video, name='video'),
    path('', views.get_list_video, name='home'),

    path('api/v1/', include(router.urls))

    # path('api/v1/videolist/', VideoApiList.as_view()),
    # path('api/v1/videolist/<int:pk>/', VideoApiDetailView.as_view()),
]