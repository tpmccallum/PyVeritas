from pyveritas.contracts import DataContract
from pyveritas.rules import RuleContext
import typing as t

class Validator:
    """A simple validator class that validates data against a DataContract.

    The Validator takes a DataContract as input and provides methods for
    validating data against that contract.
    """

    def __init__(self, contract: DataContract):
        """Initializes a new Validator.

        Args:
            contract (DataContract): The DataContract to use for validation.
        """
        self.contract = contract

    def validate(self, data: t.Dict, context: RuleContext = None) -> t.List[str]:
        """Validates the given data against the contract.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): A RuleContext object providing additional
                context for the validation. Defaults to None.

        Returns:
            t.List[str]: A list of error messages. If the list is empty, the data is valid.
        """
        return self.contract.validate(data, context)

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Checks if the given data is valid according to the contract.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): A RuleContext object providing additional
                context for the validation. Defaults to None.

        Returns:
            bool: True if the data is valid, False otherwise.
        """
        return not bool(self.validate(data, context))

    def __call__(self, data: t.Dict, context: RuleContext = None) -> bool:
        """Allows the validator to be called like a function.

        Args:
            data (t.Dict): The data to validate.
            context (RuleContext, optional): A RuleContext object providing additional
                context for the validation. Defaults to None.

        Returns:
            bool: True if the data is valid, False otherwise.
        """
        return self.is_valid(data, context)