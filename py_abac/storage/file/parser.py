"""
    JSON Dot Parser
"""

import json
from typing import Dict

from dotty_dict import dotty
from flatten_dict import flatten_dict


class JSONDotParser:
    """
        JSON dot notation parser. The class exposes serializing
        and de-serializing methods to parse JSON in dotted notation
        to and from python dict objects.
    """

    @classmethod
    def __nest(cls, obj: Dict) -> Dict:
        """
            Nest a given flatten dict object. A flatten dict does not
            contain any nesting and has its keys in dotted notation.
        """
        _dotty = dotty()
        for key, value in obj.items():
            _dotty[key] = value

        return _dotty.to_dict()

    @classmethod
    def __flatten(cls, obj: Dict) -> Dict:
        """
            Flatten a given dict object. A flatten dict does not
            contain any nesting and has its keys in dotted notation.
        """
        return flatten_dict.flatten(
            obj, reducer='dot', enumerate_types=(list,), keep_empty_types=(dict, list)
        )

    @classmethod
    def loads(cls, string: str, sep: str = ",") -> Dict:
        """
            Deserialize string in dotted JSON notation to python
            dict object.

            :param string: string to deserialize.
            :param sep: delimiter separating key value pairs. Defaults to ','.
            :returns: deserialized python dict
        """
        if sep != ",":
            string.replace(sep, ",")
        obj = json.loads("{{{}}}".format(string))

        return cls.__nest(obj)

    @classmethod
    def dumps(cls, obj: Dict, sep: str = ",") -> str:
        """
            Serialize python dict object as string in dotted JSON
            notation.

            :param obj: object to serialize.
            :param sep: delimiter separating key value pairs. Defaults to ','.
            :returns: serialized string
        """
        flatten = cls.__flatten(obj)

        return sep.join([
            '"{}":{}'.format(key, value) for key, value in flatten.items()
        ])
