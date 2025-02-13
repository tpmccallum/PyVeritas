from abc import ABC, abstractmethod
import typing as t
from pyveritas.rules import Rule, RuleContext, StringRegexRule, NumberRangeRule, StringLengthRule, RequiredRule


class DataContract(ABC):
    """
    Base class for all data contracts.

    A data contract defines the structure and constraints for a particular
    type of data. Subclasses must implement the `validate` method.
    """

    def __init__(self, rules: t.List[Rule] = None):
        """Initializes a new DataContract.

        Args:
            rules (List[Rule], optional): A list of validation rules to apply to the data.
                Defaults to None (an empty list).
        """
        self.rules = rules or []

    @abstractmethod
    def validate(self, data: t.Dict, context: RuleContext = None) -> t.List[str]:
        """Validates the given data against the contract's rules.

        Args:
            data (t.Dict): A dictionary containing the data to validate.
            context (RuleContext, optional): A RuleContext object providing additional
                context for the validation. Defaults to None.

        Returns:
            t.List[str]: A list of error messages. If the list is empty, the data is valid.
        """
        pass

    def add_rule(self, rule: Rule):
        """Adds a rule to the contract.

        Args:
            rule (Rule): The rule to add.
        """
        self.rules.append(rule)

    def __call__(self, data: t.Dict, context: RuleContext = None) -> t.List[str]:
        """Allows the contract to be called like a function.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): A RuleContext object providing additional
                context for the validation. Defaults to None.

        Returns:
            t.List[str]: A list of error messages. If the list is empty, the data is valid.
        """
        return self.validate(data, context)


class UserContract(DataContract):
    """
    Example data contract for a User object.

    This contract checks that the 'name' field is a string with a length
    between 3 and 20 characters, the 'email' field is a valid email
    address, and the 'age' field is a number between 0 and 120.
    """

    def __init__(self):
        """Initializes a new UserContract with the validation rules."""
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
        """Validates the given data against the contract's rules.

        Args:
            data (t.Dict): A dictionary containing the data to validate.
            context (RuleContext, optional): A RuleContext object providing additional
                context for the validation. Defaults to None.

        Returns:
            t.List[str]: A list of error messages. If the list is empty, the data is valid.
        """
        errors = []
        for rule in self.rules:
            if not rule.is_valid(data, context):
                errors.append(rule.error_message(data, context))
        return errors