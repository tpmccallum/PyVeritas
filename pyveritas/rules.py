# pyveritas/rules.py

import re  # For regular expression validation
from datetime import datetime  # For date validation
import typing as t
from abc import ABC, abstractmethod
import json

class RuleContext:
    """
    Provides context to rules during validation.  Can be extended for
    application-specific needs.
    """
    def __init__(self, data:t.Dict = {}):
        self.context = data

class Rule(ABC):
    """
    Base class for all validation rules.
    """

    @abstractmethod
    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """
        Checks if the rule is valid for the given data.
        """
        pass

    @abstractmethod
    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        """
        Returns an error message if the rule is not valid.
        """
        pass

    def __and__(self, other: "Rule") -> "AndRule":
        return AndRule(self, other)

    def __or__(self, other: "Rule") -> "OrRule":
        return OrRule(self, other)

    def __invert__(self) -> "NotRule":
        return NotRule(self)


class AndRule(Rule):
    """
    Combines two rules with a logical AND.
    """

    def __init__(self, rule1: Rule, rule2: Rule):
        self.rule1 = rule1
        self.rule2 = rule2

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        return self.rule1.is_valid(data, context) and self.rule2.is_valid(data, context)

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        if not self.rule1.is_valid(data, context):
            return self.rule1.error_message(data, context)
        else:
            return self.rule2.error_message(data, context)


class OrRule(Rule):
    """
    Combines two rules with a logical OR.
    """

    def __init__(self, rule1: Rule, rule2: Rule):
        self.rule1 = rule1
        self.rule2 = rule2

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        return self.rule1.is_valid(data, context) or self.rule2.is_valid(data, context)

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        return f"Both rules failed: {self.rule1.error_message(data, context)} OR {self.rule2.error_message(data, context)}"


class NotRule(Rule):
    """
    Negates a rule.
    """

    def __init__(self, rule: Rule):
        self.rule = rule

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        return not self.rule.is_valid(data, context)

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        return f"Rule should not have been valid: {self.rule.error_message(data, context)}"

# -----------------------------------------------------------------------------
# String Validation Rules
# -----------------------------------------------------------------------------

class StringRule(Rule):
    """Base class for string-based rules."""

    def __init__(self, field: str):
        self.field = field

    def _get_value(self, data: t.Dict) -> str:
        """Helper method to get the string value from the data."""
        value = data.get(self.field)
        if not isinstance(value, str):
            return None  # Or raise an exception if you prefer strict type checking
        return value

class StringLengthRule(StringRule):
    """
    Checks if a string's length falls within a specified range.
    """

    def __init__(self, field: str, min_length: int = None, max_length: int = None):
        super().__init__(field)
        self.min_length = min_length
        self.max_length = max_length

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        value = self._get_value(data)
        if value is None:
            return False
        length = len(value)
        if self.min_length is not None and length < self.min_length:
            return False
        if self.max_length is not None and length > self.max_length:
            return False
        return True

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        value = self._get_value(data)
        if value is None:
            return f"Field '{self.field}' must be a string"

        if self.min_length is not None and self.max_length is not None:
            return f"Field '{self.field}' must be between {self.min_length} and {self.max_length} characters long"
        elif self.min_length is not None:
            return f"Field '{self.field}' must be at least {self.min_length} characters long"
        else:
            return f"Field '{self.field}' must be at most {self.max_length} characters long"


class StringRegexRule(StringRule):
    """
    Checks if a string matches a specified regular expression.
    """

    def __init__(self, field: str, regex: str):
        super().__init__(field)
        self.regex = regex

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        value = self._get_value(data)
        if value is None:
            return False
        return re.match(self.regex, value) is not None

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        value = self._get_value(data)
        if value is None:
            return f"Field '{self.field}' must be a string"
        return f"Field '{self.field}' must match the regular expression: {self.regex}"


class StringChoicesRule(StringRule):
    """
    Checks if a string is one of a specified set of choices.
    """

    def __init__(self, field: str, choices: t.List[str]):
        super().__init__(field)
        self.choices = choices

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        value = self._get_value(data)
        if value is None:
            return False
        return value in self.choices

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        value = self._get_value(data)
        if value is None:
            return f"Field '{self.field}' must be a string"
        return f"Field '{self.field}' must be one of the following choices: {self.choices}"


# -----------------------------------------------------------------------------
# Numerical Validation Rules
# -----------------------------------------------------------------------------

class NumberRule(Rule):
    """Base class for number-based rules."""

    def __init__(self, field: str):
        self.field = field

    def _get_value(self, data: t.Dict) -> t.Union[int, float, None]:
        """Helper method to get the number value from the data."""
        value = data.get(self.field)
        if not isinstance(value, (int, float)):
            return None  # Or raise an exception if you prefer strict type checking
        return value


class NumberRangeRule(NumberRule):
    """
    Checks if a number falls within a specified range (inclusive).
    """

    def __init__(self, field: str, min_value: t.Union[int, float] = None, max_value: t.Union[int, float] = None):
        super().__init__(field)
        self.min_value = min_value
        self.max_value = max_value

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        value = self._get_value(data)
        if value is None:
            return False
        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False
        return True

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        value = self._get_value(data)
        if value is None:
            return f"Field '{self.field}' must be a number"
        if self.min_value is not None and self.max_value is not None:
            return f"Field '{self.field}' must be between {self.min_value} and {self.max_value}"
        elif self.min_value is not None:
            return f"Field '{self.field}' must be at least {self.min_value}"
        else:
            return f"Field '{self.field}' must be at most {self.max_value}"


class IntegerRule(TypeRule):
    """
    Specialization of TypeRule for integers.
    """

    def __init__(self, field: str):
        super().__init__(field)

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        return isinstance(data.get(self.field), int)

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        return f"Field '{self.field}' must be an integer"


class FloatRule(TypeRule):
    """
    Specialization of TypeRule for floats.
    """

    def __init__(self, field: str):
        super().__init__(field)

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        return isinstance(data.get(self.field), float)

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        return f"Field '{self.field}' must be a float"


# -----------------------------------------------------------------------------
# Date and Time Validation Rules
# -----------------------------------------------------------------------------

class DateTimeRule(Rule):
    """Base class for datetime-based rules."""

    def __init__(self, field: str):
        self.field = field

    def _get_value(self, data: t.Dict) -> t.Union[datetime, str, None]:
        """Helper method to get the datetime value from the data."""
        value = data.get(self.field)
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                # Attempt to parse the string as a datetime
                return datetime.fromisoformat(value)  # Or use a different parsing method
            except ValueError:
                return None  # Or raise an exception
        return None

class DateTimeFormatRule(DateTimeRule):
    """
    Checks if a datetime string matches a specified format.
    """

    def __init__(self, field: str, format_string: str):
        super().__init__(field)
        self.format_string = format_string

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        value = self._get_value(data)
        if value is None:
            return False
        try:
            if isinstance(value, datetime):
                value.strftime(self.format_string)
            else:
                datetime.strptime(value, self.format_string) #Attempt to parse if it has not previously
            return True
        except ValueError:
            return False

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        value = data.get(self.field)
        if value is None:
            return f"Field '{self.field}' must be a datetime or a string that can be converted to a datetime"

        return f"Field '{self.field}' must be in the format: {self.format_string}"


# -----------------------------------------------------------------------------
# Boolean Validation Rules
# -----------------------------------------------------------------------------

class BooleanRule(TypeRule):
    """
    Checks if a field is a boolean.
    """

    def __init__(self, field: str):
        super().__init__(field)

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        return isinstance(data.get(self.field), bool)

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        return f"Field '{self.field}' must be a boolean"

# -----------------------------------------------------------------------------
# JSON Validation Rules
# -----------------------------------------------------------------------------

class JSONRule(Rule):
    """
    Checks if a field contains valid JSON.
    """

    def __init__(self, field: str):
        self.field = field

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        value = data.get(self.field)
        if not isinstance(value, str):
            return False  # JSON must be a string
        try:
            json.loads(value)  # Attempt to parse the JSON string
            return True
        except json.JSONDecodeError:
            return False

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        return f"Field '{self.field}' must contain valid JSON"