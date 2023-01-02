from rest_framework import serializers

from classroom.models import Classroom


class ClassroomSerializer(serializers.ModelSerializer):
    def create(self, validated_data, **kwargs):
        return

    class Meta:
        model = Classroom
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)
