from rest_framework import serializers
from course.models import LectureSection
from course.serializers.lecture import LectureSerializer

__all__ = [
    'LectureSectionSerializer',
    'LectureSectionDetailSerializer',
]


class LectureSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LectureSection
        fields = '__all__'


class LectureSectionDetailSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(source='lecture_set', many=True, read_only=True)

    class Meta:
        model = LectureSection
        fields = '__all__'
