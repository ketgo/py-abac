from marshmallow import fields


class Subject(fields.Field):
    """Subject filed"""

    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return value
