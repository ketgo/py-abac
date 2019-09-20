from marshmallow import fields


class Context(fields.Field):
    """Context filed"""

    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return value
