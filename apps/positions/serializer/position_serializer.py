from rest_framework import serializers
from ..models import Position
from apps.employees.models import Employee
from datetime import datetime


class PositionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255, min_length=2)
    description = serializers.CharField(required=False, max_length=1000)
    employee_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_name(self, value):
        if not self.instance:
            if Position.objects(name__iexact=value).first():
                raise serializers.ValidationError(
                    "Position with this name already exists")
        else:
            if Position.objects(name__iexact=value, id__ne=self.instance.id).first():
                raise serializers.ValidationError(
                    "Position with this name already exists")
        return value.strip()

    def validate_description(self, value):
        if value and len(value.strip()) < 5:
            raise serializers.ValidationError(
                "Description must have at least 5 characters")
        return value.strip() if value else value

    def create(self, validated_data):
        validated_data.pop('created_at', None)
        validated_data.pop('updated_at', None)
        position = Position(**validated_data)
        position.save()
        return position

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['employee_count'] = Employee.objects(position=instance).count()
        return data
