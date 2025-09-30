from mongoengine import Document, StringField, DateTimeField, ReferenceField, BooleanField
from apps.employees.models import Employee


class Task(Document):
    title = StringField(required=True, max_length=255)
    description = StringField(max_length=1000)
    assigned_to = ReferenceField(Employee, required=True)
    status = StringField(
        choices=['open', 'blocked', 'inprogress', 'qa', 'done'], default='open')
    due_date = DateTimeField()
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    transferred_to = ReferenceField(Employee, null=True)
    transferred_at = DateTimeField(null=True)

    meta = {
        'collection': 'tasks',
        'ordering': ['-created_at']
    }

    def __str__(self):
        return f"{self.title} - {self.assigned_to.name if self.assigned_to else 'Unassigned'}"
