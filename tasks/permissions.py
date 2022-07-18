from rest_framework import permissions
from courses.models import Course
from lessons.models import Lesson
from students.models import Student
from django.core.exceptions import ObjectDoesNotExist
from tasks.models import Task

from utils import get_object_or_404




class IsTeacherOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        
        lesson_id = view.kwargs.get("lesson_id")
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        course = get_object_or_404(Course, pk=lesson.course_id)

        return course.owner == request.user
           

class IsTeacherOwnerTask(permissions.BasePermission):

    def has_permission(self, request, view):
        task_id = view.kwargs.get("pk")
        task = get_object_or_404(Task, pk=task_id)
        lesson = get_object_or_404(Lesson, pk=task.lesson.id)
        course = get_object_or_404(Course, pk=lesson.course_id)
        return course.owner == request.user
                

class IsAdmServer(permissions.BasePermission):

    def has_permission(self, request, view):
        
        return request.user.is_superuser

class HasCourseBondTaks(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_superuser

        task_id = view.kwargs.get("pk")
        task = get_object_or_404(Task, pk=task_id)
        lesson = get_object_or_404(Lesson, pk=task.lesson.id)
        course = get_object_or_404(Course, pk=lesson.course_id)
        if course.owner == request.user:
                return True 

        if request.method in permissions.SAFE_METHODS:
            if request.user.is_superuser:
                return True
            try:
                Student.objects.get(course=course, student=request.user)
                return True
            except ObjectDoesNotExist:
                return False
        
        return False

class HasCourseBond(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            lesson_id = view.kwargs.get("lesson_id")
            lesson = get_object_or_404(Lesson, pk=lesson_id)
            course = get_object_or_404(Course, pk=lesson.course_id)
            if course.owner == request.user or request.user.is_superuser:
                return True 

            try:
                Student.objects.get(course=course, student=request.user)
                return True
            except ObjectDoesNotExist:
                return False
        
        return False