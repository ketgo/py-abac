"""
    SQL storage policy model
"""

from typing import Union, List, Type

from sqlalchemy import Column, String, Integer, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ...policy import Policy

Base = declarative_base()


class TargetModel:
    """
        Base policy target model
    """
    target_id = Column(String(248), comment="Target ID used for filtering policies")


class SubjectTargetModel(TargetModel, Base):
    """
        Subject target data model
    """
    __tablename__ = "py_abac_subject_targets"

    id = Column(Integer, primary_key=True)
    uid = Column(String(248), ForeignKey("py_abac_policies.uid", ondelete="CASCADE"))


class ResourceTargetModel(TargetModel, Base):
    """
        Resource target data model
    """
    __tablename__ = "py_abac_resource_targets"

    id = Column(Integer, primary_key=True)
    uid = Column(String(248), ForeignKey("py_abac_policies.uid", ondelete="CASCADE"))


class ActionTargetModel(TargetModel, Base):
    """
        Action target data model
    """
    __tablename__ = "py_abac_action_targets"

    id = Column(Integer, primary_key=True)
    uid = Column(String(248), ForeignKey("py_abac_policies.uid", ondelete="CASCADE"))


class PolicyModel(Base):
    """
        Policy data model
    """
    __tablename__ = "py_abac_policies"

    uid = Column(String(248), primary_key=True)
    json = Column(JSON(), nullable=False)
    subjects = relationship(SubjectTargetModel, passive_deletes=True, lazy='joined')
    resources = relationship(ResourceTargetModel, passive_deletes=True, lazy='joined')
    actions = relationship(ActionTargetModel, passive_deletes=True, lazy='joined')

    @classmethod
    def from_policy(cls, policy: Policy) -> "PolicyModel":
        """
            Create `PolicyModel` from `Policy` object
        """
        rvalue = cls()
        rvalue._setup(policy)

        return rvalue

    def to_policy(self) -> Policy:
        """
            Get `Policy` object from model instance
        """
        return Policy.from_json(self.json)

    def update(self, policy: Policy):
        """
            Update policy model instance to match policy object
        """
        self._setup(policy)

    @classmethod
    def get_filtered_cursor(cls, subject_id: str, resource_id: str, action_id: str):
        pass

    def _setup(self, policy: Policy):
        """
            Setup instance using policy object
        """
        self.uid = policy.uid
        self.json = policy.to_json()

        # Setup targets
        self._setup_targets(
            policy.targets.subject_id,
            self.subjects,
            SubjectTargetModel
        )
        self._setup_targets(
            policy.targets.resource_id,
            self.resources,
            ResourceTargetModel
        )
        self._setup_targets(
            policy.targets.action_id,
            self.actions,
            ActionTargetModel
        )

    @staticmethod
    def _setup_targets(
            target_id: Union[str, List[str]],
            model_attr: List[TargetModel],
            target_model_cls: Type[TargetModel]
    ):
        """
            Setup policy target ID(s) into model attribute.
        """
        # Create list of target ID(s) present in policy
        target_ids: List[str] = target_id if isinstance(target_id, list) else [target_id]
        # Remove all previous ID(s) associated with policy in model
        model_attr.clear()
        for tid in target_ids:
            target_model = target_model_cls()
            # Replace with SQL wildcard '%'
            target_model.target_id = tid.replace('%', '"%"').replace('*', '%')
            model_attr.append(target_model)
