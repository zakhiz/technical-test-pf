from rest_framework import serializers
from ..models import Employee
from bson import ObjectId


class EmployeeSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255, min_length=2)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    position = serializers.CharField()
    salary = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=0)
    position_name = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_position(self, value):
        try:
            ObjectId(value)
            return value
        except Exception as e:
            raise serializers.ValidationError(f"Invalid position ID {e}")

    def validate_email(self, value):
        if not self.instance:
            if Employee.objects(email=value).first():
                raise serializers.ValidationError("Email already exists")
        else:
            # Para MongoDB, usamos __ne (not equal) en lugar de exclude
            if Employee.objects(email=value, id__ne=self.instance.id).first():
                raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        if 'position' in validated_data:
            validated_data['position'] = ObjectId(validated_data['position'])
        return Employee.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'position' in validated_data:
            validated_data['position'] = ObjectId(validated_data['position'])

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.position and hasattr(instance.position, 'name'):
            data['position_name'] = instance.position.name
            data['position'] = str(instance.position.id)
        return data
