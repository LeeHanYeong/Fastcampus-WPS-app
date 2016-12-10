from rest_framework import serializers
from course.models import Course
from course.serializers.lecture import LectureSectionSerializer

__all__ = [
    'CourseSerializer',
]


class CourseSerializer(serializers.ModelSerializer):
    sections = LectureSectionSerializer(
        many=True,
        source='lecturesection_set',
        read_only=True
    )

    class Meta:
        model = Course
        fields = (
            'type',
            'title',
            'number',
            'description',
            'start_date',
            'end_date',
            'sections',
        )