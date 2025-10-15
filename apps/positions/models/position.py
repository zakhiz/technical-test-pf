from mongoengine import Document, StringField, DateTimeField


class Position(Document):
    name = StringField(required=True, max_length=255, unique=True)
    description = StringField(required=False, max_length=1000)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    meta = {
        'collection': 'positions',
        'ordering': ['-created_at'],
        'indexes': ['name', 'description']
    }

    def __str__(self):
        return self.name
