"""
    Policy class
"""

import enum

from .rules import Rules
from .targets import Targets
from ..context import EvaluationContext
from ..exceptions import PolicyCreateError

from pydantic import BaseModel, conint, ValidationError


class Access(enum.Enum):
    """
        Access decisions
    """
    DENY_ACCESS = "deny"
    ALLOW_ACCESS = "allow"


class Policy(BaseModel):
    """
        Policy class containing rules and targets
    """
    uid: str
    description: str = ""
    rules: Rules
    targets: Targets
    effect: Access
    priority: conint(ge=0) = 0

    @classmethod
    def from_json(cls, data: dict) -> "Policy":
        """
            Create Policy object from JSON
        """
        try:
            return cls.parse_obj(data)
        except ValidationError as err:
            raise PolicyCreateError(err.json())

    def to_json(self):
        """
            Convert policy object to JSON
        """
        return self.dict()

    def fits(self, ctx: EvaluationContext) -> bool:
        """
            Check if the request fits policy

            :param ctx: evaluation context
            :return: True if fits else False
        """
        return self.rules.is_satisfied(ctx) and self.targets.match(ctx)

    @property
    def is_allowed(self) -> bool:
        """
            Check if access is allowed
        """
        return self.effect == Access.ALLOW_ACCESS
