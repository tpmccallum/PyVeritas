from abc import ABC, abstractmethod
import typing as t
from pyveritas.rules import Rule, RuleContext, StringRegexRule, NumberRangeRule, StringLengthRule, RequiredRule


class DataContract(ABC):
    """
    Base class for all data contracts.
    """

    def __init__(self, rules: t.List[Rule] = None):
        self.rules = rules or []

    @abstractmethod
    def validate(self, data: t.Dict, context: RuleContext = None) -> t.List[str]:
        """
        Validates the given data against the contract's rules.
        Returns a list of error messages.  If the list is empty, the data is valid.
        """
        pass

    def add_rule(self, rule: Rule):
        """
        Adds a rule to the contract.
        """
        self.rules.append(rule)

    def __call__(self, data: t.Dict, context: RuleContext = None) -> t.List[str]:
        """
        Allows the contract to be called like a function.
        """
        return self.validate(data, context)


class UserContract(DataContract):
    """
    Example data contract for a User object.
    """

    def __init__(self):
        super().__init__([
            RequiredRule("email"),
            StringRegexRule(
                field="email",
                regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
            ),
            RequiredRule("age"),
            NumberRangeRule(field="age", min_value=0, max_value=120),
            RequiredRule("name"),
            StringLengthRule(field="name", min_length=3, max_length=20)
        ])

    def validate(self, data: t.Dict, context: RuleContext = None) -> t.List[str]:
        errors = []
        for rule in self.rules:
            if not rule.is_valid(data, context):
                errors.append(rule.error_message(data, context))
        return errors