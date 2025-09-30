from mongoengine import Document, StringField, EmailField, DecimalField, DateTimeField, ReferenceField, BooleanField
from apps.positions.models import Position


class Employee(Document):
    name = StringField(required=True, max_length=255)
    last_name = StringField(required=True, max_length=255)
    email = EmailField(required=True, unique=True)
    phone = StringField(required=True, max_length=20)
    position = ReferenceField(Position, required=True)
    salary = DecimalField(required=True, precision=2)
    hire_date = DateTimeField(required=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    deleted = BooleanField(default=False)
    deleted_at = DateTimeField()
    replacement_employee = ReferenceField(
        'self', null=True)

    meta = {
        'collection': 'employees',
        'ordering': ['-created_at']
    }

    def __str__(self):
        return f"{self.name} {self.last_name}"
