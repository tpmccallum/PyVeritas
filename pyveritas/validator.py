from pyveritas.contracts import DataContract
from pyveritas.rules import RuleContext
import typing as t

class Validator:
    """
    A simple validator class that validates data against a DataContract.
    """

    def __init__(self, contract: DataContract):
        self.contract = contract

    def validate(self, data: t.Dict, context: RuleContext = None) -> t.List[str]:
        """
        Validates the given data against the contract.
        """
        return self.contract.validate(data, context)

    def is_valid(self, data: t.Dict, context: RuleContext = None) -> bool:
        """
        Returns True if the data is valid, False otherwise.
        """
        return not bool(self.validate(data, context))

    def __call__(self, data: t.Dict, context: RuleContext = None) -> bool:
        """
        Allows the validator to be called like a function.
        """
        return self.is_valid(data, context)