from django.http import StreamingHttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Video
from .serializers import VideoSerializer
from .services import open_file
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from .permissions import *


def get_list_video(request):
    return render(request, 'video_hosting/home.html', {'video_list': Video.objects.all()})


def get_video(request, pk: int):
    _video = get_object_or_404(Video, id=pk)
    return render(request, "video_hosting/video.html", {"video": _video})


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response


##############
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = (IsAuthenticatedOrOwnerOrReadOnly,)

# class VideoApiList(generics.ListCreateAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#
# class VideoApiDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer
#     permission_classes = (IsOwnerOrAdminOrReadOnly,)
# Ниже нахуй не надо, 2 класса выше делают всю работу
# class VideoApiView(APIView):
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             w = Video.objects.all()
#             return Response({'videos': VideoSerializer(w, many=True).data})
#
#         try:
#             w = Video.objects.get(pk=pk)
#             return Response(VideoSerializer(w).data)
#         except:
#             return Response({"error": "Object does not exists"})
#
#     def post(self, request):
#         serializer = VideoSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'title': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'error': "Method PUT not allowed"})
#         try:
#             instance = Video.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#         serializer = VideoSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'post': serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({'error': 'Method DELETE not allowed'})
#
#         try:
#             Video.objects.get(pk=pk).delete()
#         except:
#             return Response({"error": "Object does not exists"})
#
#         return Response({'video': 'delete video ' + str(pk)})
# class VideoApiView(generics.ListAPIView):
#     queryset = Video.objects.all()
#     serializer_class = VideoSerializer
