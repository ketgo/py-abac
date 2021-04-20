"""
    Policy targets class
"""

import fnmatch
from typing import Union, List

from pydantic import BaseModel, constr

from ..context import EvaluationContext


class Targets(BaseModel):
    """
        Policy targets
    """
    subject_id: Union[constr(min_length=1), List[constr(min_length=1)]] = "*"
    resource_id: Union[constr(min_length=1), List[constr(min_length=1)]] = "*"
    action_id: Union[constr(min_length=1), List[constr(min_length=1)]] = "*"

    def match(self, ctx: EvaluationContext):
        """
            Check if request matches policy targets

            :param ctx: policy evaluation context
            :return: True if matches else False
        """
        return self._is_in(self.subject_id, ctx.subject_id) and \
               self._is_in(self.resource_id, ctx.resource_id) and \
               self._is_in(self.action_id, ctx.action_id)

    @staticmethod
    def _is_in(ace_ids, ace_id: str):
        """
            Returns True if `ace_id` is in `ace_ids`.
        """
        _ace_ids = ace_ids if isinstance(ace_ids, list) else [ace_ids]
        for _id in _ace_ids:
            # Unix file name type string matching
            if fnmatch.fnmatch(ace_id, _id):
                return True
        return False
