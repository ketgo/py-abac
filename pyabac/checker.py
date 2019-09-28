"""
    Checker to evaluate fit of inquiry to a policy
"""

import types

from objectpath import Tree


class Checker(object):

    def __init__(self, inquiry):
        """
            Initialize checker

            :param inquiry: inquiry object
        """
        # Subject element tree
        self._subject_tree = Tree(inquiry.subject)
        # Resource element tree
        self._resource_tree = Tree(inquiry.resource)
        # Action element tree
        self._action_tree = Tree(inquiry.action)
        # Context element tree
        self._context_tree = Tree(inquiry.context)

    def fits(self, policy):
        """
            Check if inquiry fits the given policy

            :param policy: policy object
            :return: True if fits else false
        """
        # Check if any of the subject attributes fit the policy
        if not self._policy_fits(self._subject_tree, policy.subjects):
            return False
        # Check if any of the resource attributes fit the policy
        if not self._policy_fits(self._resource_tree, policy.resources):
            return False
        # Check if any of the action attributes fit the policy
        if not self._policy_fits(self._action_tree, policy.actions):
            return False
        # Check if any of the context attributes fit policy
        if not self._policy_fits(self._context_tree, policy.context):
            return False
        # If the policy fits then return True
        return True

    def _policy_fits(self, element_tree, policy_element):
        # Check each rule in the policy element
        for rule in policy_element:
            # If any of the rule fits then return True
            if self._rule_fits(element_tree, rule):
                return True
            # If no rule fits then return False
        return False

    def _rule_fits(self, element_tree, rule):
        # Check each attribute and required condition in the rule
        for attribute_path, condition in rule.items():
            # Check all values at attribute path
            attribute_values = self._extract_values(element_tree, attribute_path)
            for value in attribute_values:
                # Check if the extracted value satisfies the condition. Return False if any
                # of the attribute does not satisfy the condition.
                if not condition.is_satisfied(value):
                    return False
        # If all rules satisfied then return True
        return True

    @staticmethod
    def _extract_values(element_tree, attribute_path):
        rvalue = element_tree.execute(attribute_path)
        if not rvalue:
            return [None]
        if isinstance(rvalue, types.GeneratorType):
            return list(rvalue)
        return [rvalue]
