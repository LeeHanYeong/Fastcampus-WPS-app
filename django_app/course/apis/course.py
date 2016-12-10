from rest_framework import filters
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import CursorPagination

from course.models import Course
from course.serializers import CourseSerializer


__all__ = [
    'CourseViewSet',
]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CursorPagination
    filter_backends = (filters.OrderingFilter, )

