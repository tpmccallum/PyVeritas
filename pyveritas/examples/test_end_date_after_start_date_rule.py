from pyveritas.contracts import DataContract
from pyveritas.rules import EndDateAfterStartDateRule
from pyveritas.validator import Validator
from datetime import datetime
import typing as t
from pyveritas.rules import Rule, RuleContext, StringRegexRule, NumberRangeRule, StringLengthRule, RequiredRule

class EventContract(DataContract):
    """
    Data contract for validating event data, including start and end dates.
    """
    def __init__(self):
        super().__init__([
            EndDateAfterStartDateRule(start_date_field="start_date", end_date_field="end_date"),
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

# Example Usage:
event_contract = EventContract()
validator = Validator(event_contract)

valid_event_data = {
    "start_date": datetime(2023, 1, 15),
    "end_date": datetime(2024, 2, 16),
}

invalid_event_data = {
    "start_date": datetime(2024, 2, 16),
    "end_date": datetime(2023, 1, 15),
}

print("Validating event data...")
# Show example of the data being processed
print(f"Is the raw data ({valid_event_data}) valid?: {validator.is_valid(valid_event_data)}")

print(f"Is the raw data ({invalid_event_data}) valid?: {validator.is_valid(invalid_event_data)}")