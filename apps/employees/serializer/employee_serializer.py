from rest_framework import serializers

from apps.employees.models import employee
from ..models import Employee
from bson import ObjectId
from apps.positions.models import Position
from datetime import datetime


class EmployeeSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    position = serializers.CharField()
    salary = serializers.FloatField(min_value=0)
    hire_date = serializers.DateTimeField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    deleted = serializers.BooleanField(read_only=True, required=False)
    deleted_at = serializers.DateTimeField(read_only=True, required=False)
    replacement_employee = serializers.CharField(
        read_only=True)

    def validate_position(self, value):
        try:
            ObjectId(value)
            if not Position.objects.filter(id=value):
                raise serializers.ValidationError("Position not found")
            return value
        except Exception as e:
            print(e)
            raise serializers.ValidationError("Invalid position ID")

    def validate_email(self, value):
        if not self.instance:
            if Employee.objects(email=value).first():
                raise serializers.ValidationError("Email already exists")
        else:
            if Employee.objects(email=value, id__ne=self.instance.id).first():
                raise serializers.ValidationError("Email already used")
        return value

    def create(self, validated_data):
        validated_data = self._convert_value_position_to_objectId(
            validated_data)
        validated_data.pop('created_at', None)
        validated_data.pop('updated_at', None)
        employee = Employee(**validated_data)
        employee.save()
        return employee

    def update(self, instance, validated_data):
        if 'position' in validated_data:
            validated_data = self._convert_value_position_to_objectId(
                validated_data)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def _convert_value_position_to_objectId(self, values):
        if 'position' in values:
            values['position'] = ObjectId(values['position'])
        return values
