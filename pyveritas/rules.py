import re  # For regular expression validation
from datetime import datetime  # For date validation
import typing as t
from abc import ABC, abstractmethod
import json

class RuleContext:
    """Provides context to rules during validation.

    Can be extended for application-specific needs.

    Attributes:
        context (t.Dict, optional): A dictionary containing contextual data. Defaults to {}.
    """

    def __init__(self, data: t.Dict = {}):
        """Initializes a new RuleContext."""
        self.context = data

    def __str__(self):
        """Returns a string representation of the RuleContext."""
        return str(self.context)

class Rule(ABC):
    """Base class for all validation rules.

    Rules define a specific validation check. Subclasses must implement
    the `is_valid` and `error_message` methods.
    """

    @abstractmethod
    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the rule is valid for the given data.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): Contextual information for the rule.
                Defaults to None.

        Returns:
            bool: True if the data is valid, False otherwise.
        """
        pass

    @abstractmethod
    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        """Returns an error message if the rule is not valid.

        Args:
            data (t.Dict): The data that failed validation.
            context (RuleContext, optional): Contextual information for the rule.
                Defaults to None.

        Returns:
            str: An error message describing the validation failure.
        """
        pass

    def __and__(self, other: "Rule") -> "AndRule":
        """Combines this rule with another rule using a logical AND.

        Args:
            other (Rule): The other rule to combine with.

        Returns:
            AndRule: A new AndRule object that combines the two rules.
        """
        return AndRule(self, other)

    def __or__(self, other: "Rule") -> "OrRule":
        """Combines this rule with another rule using a logical OR.

        Args:
            other (Rule): The other rule to combine with.

        Returns:
            OrRule: A new OrRule object that combines the two rules.
        """
        return OrRule(self, other)

    def __invert__(self) -> "NotRule":
        """Negates this rule.

        Returns:
            NotRule: A new NotRule object that negates this rule.
        """
        return NotRule(self)


    def __str__(self):
        """Returns a string representation of the rule (the error message)."""
        return self.error_message

class AndRule(Rule):
    """Combines two rules with a logical AND.

    The data must be valid according to both rules for the AndRule to be valid.
    """

    def __init__(self, rule1: Rule, rule2: Rule):
        """Initializes a new AndRule.

        Args:
            rule1 (Rule): The first rule.
            rule2 (Rule): The second rule.
        """
        self.rule1 = rule1
        self.rule2 = rule2

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the data is valid according to both rules.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): Contextual information for the rules. Defaults to None.

        Returns:
            bool: True if the data is valid according to both rules, False otherwise.
        """
        return self.rule1.is_valid(data, context) and self.rule2.is_valid(data, context)

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        """Returns an error message if the data is not valid according to either rule.

        Args:
            data (t.Dict): The data that failed validation.
            context (RuleContext, optional): Contextual information for the rules. Defaults to None.

        Returns:
            str: An error message describing the validation failure.
        """
        if not self.rule1.is_valid(data, context):
            return self.rule1.error_message(data, context)
        else:
            return self.rule2.error_message(data, context)


    def __str__(self):
        """Returns a string representation of the AndRule."""
        return f'AndRule {str(self.rule1)} AND {str(self.rule2)}'

class OrRule(Rule):
    """Combines two rules with a logical OR.

    The data must be valid according to at least one of the rules for the
    OrRule to be valid.
    """

    def __init__(self, rule1: Rule, rule2: Rule):
        """Initializes a new OrRule.

        Args:
            rule1 (Rule): The first rule.
            rule2 (Rule): The second rule.
        """
        self.rule1 = rule1
        self.rule2 = rule2

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the data is valid according to at least one of the rules.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): Contextual information for the rules. Defaults to None.

        Returns:
            bool: True if the data is valid according to at least one of the rules, False otherwise.
        """
        return self.rule1.is_valid(data, context) or self.rule2.is_valid(data, context)

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        """Returns an error message if the data is not valid according to either rule.

        Args:
            data (t.Dict): The data that failed validation.
            context (RuleContext, optional): Contextual information for the rules. Defaults to None.

        Returns:
            str: An error message describing the validation failure.
        """
        return f"Both rules failed: {self.rule1.error_message(data, context)} OR {self.rule2.error_message(data, context)}"


    def __str__(self):
        """Returns a string representation of the OrRule."""
        return f'OrRule {str(self.rule1)} OR {str(self.rule2)}'

class NotRule(Rule):
    """Negates a rule.

    The data must *not* be valid according to the rule for the NotRule to be valid.
    """

    def __init__(self, rule: Rule):
        """Initializes a new NotRule.

        Args:
            rule (Rule): The rule to negate.
        """
        self.rule = rule

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the data is *not* valid according to the rule.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            bool: True if the data is *not* valid according to the rule, False otherwise.
        """
        return not self.rule.is_valid(data, context)

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        """Returns an error message if the data *is* valid according to the rule.

        Args:
            data (t.Dict): The data that passed validation (but shouldn't have).
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            str: An error message describing the validation failure (i.e., that the data was unexpectedly valid).
        """
        return f"Rule should not have been valid: {self.rule.error_message(data, context)}"

    def __str__(self):
        """Returns a string representation of the NotRule."""
        return f'NotRule NOT ({str(self.rule)})'

    # -----------------------------------------------------------------------------
    # String Validation Rules
    # -----------------------------------------------------------------------------

class StringRule(Rule):
    """Base class for string-based rules.

    Provides a helper method for retrieving the string value from the data.
    """

    def __init__(self, field: str):
        """Initializes a new StringRule.

        Args:
            field (str): The name of the field to validate.
        """
        self.field = field

    def _get_value(self, data: t.Dict) -> str:
        """Helper method to get the string value from the data.

        Args:
            data (t.Dict): The data to validate.

        Returns:
            str: The string value of the field, or None if the field is not a string.
        """
        value = data.get(self.field)
        if not isinstance(value, str):
            return None  # Or raise an exception if you prefer strict type checking
        return value

class StringLengthRule(StringRule):
    """Checks if a string's length falls within a specified range.

    The string length must be greater than or equal to `min_length` and less
    than or equal to `max_length` (inclusive).
    """

    def __init__(self, field: str, min_length: int = None, max_length: int = None):
        """Initializes a new StringLengthRule.

        Args:
            field (str): The name of the field to validate.
            min_length (int, optional): The minimum allowed length of the string. Defaults to None.
            max_length (int, optional): The maximum allowed length of the string. Defaults to None.
        """
        super().__init__(field)
        self.min_length = min_length
        self.max_length = max_length

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the string's length is within the specified range.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            bool: True if the string's length is within the specified range, False otherwise.
        """
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
        """Returns an error message if the string's length is not within the specified range.

        Args:
            data (t.Dict): The data that failed validation.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            str: An error message describing the validation failure.
        """
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
    """Checks if a string matches a specified regular expression.

    The string must match the regular expression for the StringRegexRule
    to be valid.
    """

    def __init__(self, field: str, regex: str):
        """Initializes a new StringRegexRule.

        Args:
            field (str): The name of the field to validate.
            regex (str): The regular expression to match.
        """
        super().__init__(field)
        self.regex = regex

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the string matches the regular expression.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            bool: True if the string matches the regular expression, False otherwise.
        """
        value = self._get_value(data)
        if value is None:
            return False
        return re.match(self.regex, value) is not None

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        """Returns an error message if the string does not match the regular expression.

        Args:
            data (t.Dict): The data that failed validation.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            str: An error message describing the validation failure.
        """
        value = self._get_value(data)
        if value is None:
            return f"Field '{self.field}' must be a string"
        return f"Field '{self.field}' must match the regular expression: {self.regex}"


class StringChoicesRule(StringRule):
    """Checks if a string is one of a specified set of choices.

    The string must be present in the `choices` list for the StringChoicesRule
    to be valid.
    """

    def __init__(self, field: str, choices: t.List[str]):
        """Initializes a new StringChoicesRule.

        Args:
            field (str): The name of the field to validate.
            choices (List[str]): A list of valid choices for the string.
        """
        super().__init__(field)
        self.choices = choices

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the string is one of the specified choices.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            bool: True if the string is one of the specified choices, False otherwise.
        """
        value = self._get_value(data)
        if value is None:
            return False
        return value in self.choices

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        """Returns an error message if the string is not one of the specified choices.

        Args:
            data (t.Dict): The data that failed validation.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            str: An error message describing the validation failure.
        """
        value = self._get_value(data)
        if value is None:
            return f"Field '{self.field}' must be a string"
        return f"Field '{self.field}' must be one of the following choices: {self.choices}"


    # -----------------------------------------------------------------------------
    # Numerical Validation Rules
    # -----------------------------------------------------------------------------

class NumberRule(Rule):
    """Base class for number-based rules.

    Provides a helper method for retrieving the number value from the data.
    """

    def __init__(self, field: str):
        """Initializes a new NumberRule.

        Args:
            field (str): The name of the field to validate.
        """
        self.field = field

    def _get_value(self, data: t.Dict) -> t.Union[int, float, None]:
        """Helper method to get the number value from the data.

        Args:
            data (t.Dict): The data to validate.

        Returns:
            Union[int, float, None]: The number value of the field, or None if the field is not a number.
        """
        value = data.get(self.field)
        if not isinstance(value, (int, float)):
            return None  # Or raise an exception if you prefer strict type checking
        return value


class NumberRangeRule(NumberRule):
    """Checks if a number falls within a specified range (inclusive).

    The number must be greater than or equal to `min_value` and less
    than or equal to `max_value` (inclusive).
    """

    def __init__(self, field: str, min_value: t.Union[int, float] = None, max_value: t.Union[int, float] = None):
        """Initializes a new NumberRangeRule.

        Args:
            field (str): The name of the field to validate.
            min_value (Union[int, float], optional): The minimum allowed value. Defaults to None.
            max_value (Union[int, float], optional): The maximum allowed value. Defaults to None.
        """
        super().__init__(field)
        self.min_value = min_value
        self.max_value = max_value

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the number is within the specified range.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            bool: True if the number is within the specified range, False otherwise.
        """
        value = self._get_value(data)
        if value is None:
            return False
        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False
        return True

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        """Returns an error message if the number is not within the specified range.

        Args:
            data (t.Dict): The data that failed validation.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            str: An error message describing the validation failure.
        """
        value = self._get_value(data)
        if value is None:
            return f"Field '{self.field}' must be a number"
        if self.min_value is not None and self.max_value is not None:
            return f"Field '{self.field}' must be between {self.min_value} and {self.max_value}"
        elif self.min_value is not None:
            return f"Field '{self.field}' must be at least {self.min_value}"
        else:
            return f"Field '{self.field}' must be at most {self.max_value}"


    # -----------------------------------------------------------------------------
    # Date and Time Validation Rules
    # -----------------------------------------------------------------------------

class DateTimeRule(Rule):
    """Base class for datetime-based rules.

    Provides a helper method for retrieving the datetime value from the data.
    """

    def __init__(self, field: str):
        """Initializes a new DateTimeRule.

        Args:
            field (str): The name of the field to validate.
        """
        self.field = field

    def _get_value(self, data: t.Dict) -> t.Union[datetime, str, None]:
        """Helper method to get the datetime value from the data.

        Args:
            data (t.Dict): The data to validate.

        Returns:
            Union[datetime, str, None]: The datetime value of the field, or None if the field is not a datetime or string.
        """
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
    """Checks if a datetime string matches a specified format.

    The datetime string must match the specified format for the
    DateTimeFormatRule to be valid.
    """

    def __init__(self, field: str, format_string: str):
        """Initializes a new DateTimeFormatRule.

        Args:
            field (str): The name of the field to validate.
            format_string (str): The format string to match.
        """
        super().__init__(field)
        self.format_string = format_string

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the datetime string matches the specified format.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            bool: True if the datetime string matches the specified format, False otherwise.
        """
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
        """Returns an error message if the datetime string does not match the specified format.

        Args:
            data (t.Dict): The data that failed validation.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            str: An error message describing the validation failure.
        """
        value = data.get(self.field)
        if value is None:
            return f"Field '{self.field}' must be a datetime or a string that can be converted to a datetime"

        return f"Field '{self.field}' must be in the format: {self.format_string}"

class EndDateAfterStartDateRule(Rule):
    """Checks if an end date happens after a start date.

    The end date must happen after the start date for the
    EndDateAfterStartDateRule to be valid.
    """

    def __init__(self, start_date_field: str, end_date_field: str):
        """Initializes a new EndDateAfterStartDateRule.

        Args:
            start_date_field (str): The name of the field containing the start date.
            end_date_field (str): The name of the field containing the end date.
        """
        self.start_date_field = start_date_field
        self.end_date_field = end_date_field

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the end date is after the start date in the given data.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): A RuleContext object providing additional
                context for the validation. Defaults to None.

        Returns:
            bool: True if the end date is after the start date, False otherwise.
        """
        start_date = data.get(self.start_date_field)
        end_date = data.get(self.end_date_field)

        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            return False  # Or raise an exception if you prefer strict type checking

        return end_date > start_date

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        """Returns an error message if the end date is not after the start date.

        Args:
            data (t.Dict): The data that failed validation.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            str: An error message describing the validation failure.
        """
        return f"End date must be after start date. Start Date:'{self.start_date_field}', End Date:'{self.end_date_field}'"

    # -----------------------------------------------------------------------------
    # Boolean Validation Rules
    # -----------------------------------------------------------------------------

class BooleanRule(Rule):
    """Checks if a field is a boolean.

    The field must be a boolean value for the BooleanRule to be valid.
    """

    def __init__(self, field: str):
        """Initializes a new BooleanRule.

        Args:
            field (str): The name of the field to validate.
        """
        super().__init__(field)

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the field is a boolean.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            bool: True if the field is a boolean, False otherwise.
        """
        return isinstance(data.get(self.field), bool)

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        """Returns an error message if the field is not a boolean.

        Args:
            data (t.Dict): The data that failed validation.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            str: An error message describing the validation failure.
        """
        return f"Field '{self.field}' must be a boolean"

    # -----------------------------------------------------------------------------
    # JSON Validation Rules
    # -----------------------------------------------------------------------------

class JSONRule(Rule):
    """Checks if a field contains valid JSON.

    The field must contain a valid JSON string for the JSONRule to be valid.
    """

    def __init__(self, field: str):
        """Initializes a new JSONRule.

        Args:
            field (str): The name of the field to validate.
        """
        self.field = field

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the field contains valid JSON.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            bool: True if the field contains valid JSON, False otherwise.
        """
        value = data.get(self.field)
        if not isinstance(value, str):
            return False  # JSON must be a string
        try:
            json.loads(value)  # Attempt to parse the JSON string
            return True
        except json.JSONDecodeError:
            return False

        def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
            """Returns an error message if the field does not contain valid JSON.

            Args:
                data (t.Dict): The data that failed validation.
                context (RuleContext, optional): Contextual information for the rule. Defaults to None.

            Returns:
                str: An error message describing the validation failure.
            """
            return f"Field '{self.field}' must contain valid JSON"

    # -----------------------------------------------------------------------------
    # Type Validation Rules
    # -----------------------------------------------------------------------------

class TypeRule(Rule):
    """Checks if a field is of a specific type.

    The field must be of the specified type for the TypeRule to be valid.
    """

    def __init__(self, field: str, expected_type: type):
        """Initializes a new TypeRule.

        Args:
            field (str): The name of the field to validate.
            expected_type (type): The expected type of the field.
        """
        self.field = field
        self.expected_type = expected_type

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the field is of the specified type.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            bool: True if the field is of the specified type, False otherwise.
        """
        return isinstance(data.get(self.field), self.expected_type)

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        """Returns an error message if the field is not of the specified type.

        Args:
            data (t.Dict): The data that failed validation.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            str: An error message describing the validation failure.
        """
        return f"Field '{self.field}' must be of type {self.expected_type.__name__}"
# -----------------------------------------------------------------------------
# Required Validation Rules
# -----------------------------------------------------------------------------

class RequiredRule(Rule):
    """Checks if a field is present in the data.

    The field must be present in the data for the RequiredRule to be valid.
    """
    def __init__(self, field: str):
        """Initializes a new RequiredRule.

        Args:
            field (str): The name of the field to validate.
        """
        self.field = field

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if a field is present in the data.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            bool: True if the field is present in the data, False otherwise.
        """
        return self.field in data

    def error_message(self, data: t.Dict, context: RuleContext = None) -> str:
        """Returns an error message if the field is not present in the data.

        Args:
            data (t.Dict): The data that failed validation.
            context (RuleContext, optional): Contextual information for the rule. Defaults to None.

        Returns:
            str: An error message describing the validation failure.
        """
        return f"Field '{self.field}' is required"