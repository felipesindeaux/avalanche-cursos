from rest_framework import generics
from rest_framework.views import Response, status

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from courses.models import Course
from courses.serializers import CourseSerializer

from .permissions import IsAdminToDelete, IsTeacher

class CreateListCourseView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Course.objects.all()
        else:
            return Course.objects.filter(is_active=True)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UpdateListCourseView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminToDelete]

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

class ListTeacherCoursesView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsTeacher]

    serializer_class = CourseSerializer

    def get_queryset(self):    
        return Course.objects.filter(owner=self.request.user)