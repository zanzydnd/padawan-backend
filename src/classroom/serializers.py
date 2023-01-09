from rest_framework import serializers

from classroom.models import Classroom


class ClassroomSerializer(serializers.ModelSerializer):
    def create(self, validated_data, **kwargs):
        classroom_obj = Classroom(**validated_data)
        classroom_obj.teacher = kwargs.get("user")
        classroom_obj.save()
        return classroom_obj

    class Meta:
        model = Classroom
        fields = ('id', 'name', 'description',"unique_code", "teacher_id")
        read_only_fields = ('id', "unique_code", "teacher_id")
