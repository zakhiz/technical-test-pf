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
    transferred_to_name = serializers.CharField(read_only=True)
    transferred_at = serializers.DateTimeField(read_only=True)
    assigned_to_name = serializers.CharField(read_only=True)

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
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'assigned_to' in validated_data:
            validated_data['assigned_to'] = ObjectId(
                validated_data['assigned_to'])

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.assigned_to:
            data['assigned_to'] = str(instance.assigned_to.id)
            data['assigned_to_name'] = f"{instance.assigned_to.name} {instance.assigned_to.last_name}"
        else:
            data['assigned_to'] = None
            data['assigned_to_name'] = None

        if instance.transferred_to:
            data['transferred_to'] = str(instance.transferred_to.id)
            data['transferred_to_name'] = f"{instance.transferred_to.name} {instance.transferred_to.last_name}"
            data['transferred_at'] = instance.transferred_at
        else:
            data['transferred_to'] = None
            data['transferred_to_name'] = None
            data['transferred_at'] = None

        return data
