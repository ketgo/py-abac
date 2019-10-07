"""
    Policy targets class
"""

import re

from marshmallow import Schema, fields, post_load

from ..request import Request


class Targets(object):

    def __init__(self, subject_id: list, resource_id: list, action_id: list):
        self.subject_id = subject_id
        self.resource_id = resource_id
        self.action_id = action_id

    def match(self, request: Request):
        """
            Check if request matches policy targets

            :param request: authorization request
            :return: True if matches else False
        """
        return self._is_in(self.subject_id, request.subject_id) and \
               self._is_in(self.resource_id, request.resource_id) and \
               self._is_in(self.action_id, request.action_id)

    def _is_in(self, ace_ids: list, ace_id: str):
        """
            Returns True if `ace_id` is in `ace_ids`.
        """
        for _id in ace_ids:
            if self.__same(_id, ace_id):
                return True

    @staticmethod
    def __same(pattern: str, what: str):
        rvalue = False
        # If `pattern` is substring of `what` then return False as regex match returns True
        if len(pattern) < len(what) and pattern in what:
            return rvalue
        if re.search(pattern, what):
            rvalue = True
        return rvalue


class TargetsSchema(Schema):
    subject_id = fields.List(fields.String(required=True), default=[r".*"], missing=[r".*"])
    resource_id = fields.List(fields.String(required=True), default=[r".*"], missing=[r".*"])
    action_id = fields.List(fields.String(required=True), default=[r".*"], missing=[r".*"])

    @post_load
    def post_load(self, data, **_):
        return Targets(**data)
