from rest_framework import serializers
from course.models import Lecture

__all__ = [
    'LectureSerializer',
]


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'
