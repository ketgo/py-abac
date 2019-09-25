"""
    Benchmark test for json-object marshalling
"""

import pytest
from marshmallow import Schema, fields, post_load
import jsonpickle
import jsonschema


N = 1000


class JObject(object):

    def __init__(self, subjects):
        self.subjects = subjects

    def to_json(self):
        jsonpickle.encode(self)

    @staticmethod
    def from_json(data):
        return jsonpickle.decode(data)


class MObject(object):
    class MObjectSchema(Schema):
        subjects = fields.List(fields.Mapping())

        @post_load
        def post_load(self, data, **_):
            return MObject(**data)

    def __init__(self, subjects):
        self.subjects = subjects

    def to_json(self):
        return self.MObjectSchema().dump(self)

    @staticmethod
    def from_json(data):
        return MObject.MObjectSchema().load(data)


def runs_n(n, func, data):
    return [func(data) for _ in range(n)]


@pytest.mark.parametrize('json, result', [
    ({"subjects": [{"b": [1, {"c": 2}]}]}, MObject([{"b": [1, {"c": 2}]}])),
])
def test_marshmallow(json, result, benchmark):
    o = benchmark(runs_n, N, MObject.from_json, json)
    assert o[0].subjects == result.subjects


@pytest.mark.parametrize('json, result', [
    ({"subjects": [{"b": [1, {"c": 2}]}]}, JObject([{"b": [1, {"c": 2}]}])),
])
def test_jsonpickle(json, result, benchmark):
    pickled = jsonpickle.encode(result)
    o = benchmark(runs_n, N, JObject.from_json, pickled)
    assert o[0].subjects == result.subjects


if __name__ == '__main__':
    pytest.main()
