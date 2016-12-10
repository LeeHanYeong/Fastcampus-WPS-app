from rest_framework import filters
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import CursorPagination

from course.models import LectureSection
from course.serializers import LectureSectionSerializer

__all__ = [
    'LectureSectionViewSet',
]


class LectureSectionViewSet(ModelViewSet):
    queryset = LectureSection.objects.order_by('course__title')
    serializer_class = LectureSectionSerializer
    pagination_class = CursorPagination
    filter_backends = (filters.OrderingFilter,)
    # ordering_fields = ('course__title', )
