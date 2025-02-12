from pyveritas.contracts import DataContract
from pyveritas.validator import Validator
import importlib
import typing as t

class TestRunner():
    """
    A test runner for DataContracts.
    """

    def run(self):
        """
        Runs all test cases in the suite.
        """
        print(f"Running test suite: {self.name}...")

        for test_case in self.test_cases:
            description = test_case["description"]
            contract = test_case["contract"] # This is a string of the contract classname
            data = test_case["data"]
            expected_errors = test_case["expected_errors"]

            # Dynamically load the contract class
            module_name = "pyveritas.contracts"  # Assuming contracts are in pyveritas/contracts.py
            module = importlib.import_module(module_name)
            contract_class = getattr(module, contract)
            contract_instance = contract_class()

            validator = Validator(contract_instance)
            errors = validator.validate(data)

            self._evaluate_test(description, data, errors, expected_errors)

        print(f"Test suite {self.name} complete.")
        self.summary()