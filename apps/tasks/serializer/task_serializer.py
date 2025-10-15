from rest_framework import serializers
from ..models import Task
from bson import ObjectId


class TaskSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(required=True, max_length=255, min_length=2)
    description = serializers.CharField(
        max_length=1000, required=False, allow_blank=True)
    assigned_to = serializers.CharField(required=True)
    status = serializers.ChoiceField(
        choices=['open', 'blocked', 'inprogress', 'qa', 'done'], default='open')
    due_date = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    transferred_to = serializers.CharField(read_only=True)
    transferred_at = serializers.DateTimeField(read_only=True)

    def validate_assigned_to(self, value):
        if not value:
            raise serializers.ValidationError("Assigned employee is required")
        try:
            ObjectId(value)
            return value
        except Exception as e:
            raise serializers.ValidationError(f"Invalid employee ID: {e}")

    def create(self, validated_data):
        if 'assigned_to' in validated_data:
            validated_data['assigned_to'] = ObjectId(
                validated_data['assigned_to'])
        task = Task(**validated_data)
        task.save()
        return task

    def update(self, instance, validated_data):
        if 'assigned_to' in validated_data:
            validated_data['assigned_to'] = ObjectId(
                validated_data['assigned_to'])

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
