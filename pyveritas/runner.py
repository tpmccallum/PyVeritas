from pyveritas.contracts import DataContract
from pyveritas.validator import Validator
import importlib
import typing as t


class TestRunner():
    """A test runner for DataContracts.

    This class is responsible for running test cases and validating data
    against data contracts.
    """

    def __init__(self, name: str):
        """Initializes a new TestRunner.

        Args:
            name (str): The name of the test suite.
        """
        self.name = name
        self.test_cases: t.List[t.Dict] = []  # List of test case dictionaries

    def add(self, test_case: t.Dict):
        """Adds a test case to the suite.

        Args:
            test_case (t.Dict): A dictionary containing test case details
                             (description, contract, data, expected_errors)
        """
        if not isinstance(test_case, dict):
            raise TypeError("Test case must be a dictionary")

        if "description" not in test_case:
            raise ValueError("Test case must have a 'description' field")

        if "contract" not in test_case:
            raise ValueError("Test case must have a 'contract' field")

        if "data" not in test_case:
            raise ValueError("Test case must have a 'data' field")

        self.test_cases.append(test_case)

    def run(self):
        """Runs all test cases in the suite.

        For each test case, it dynamically loads the contract class,
        instantiates it, validates the data against the contract, and
        prints the results.
        """
        print(f"Running test suite: {self.name}...")

        for test_case in self.test_cases:
            description = test_case["description"]
            contract = test_case["contract"]  # This is a string of the contract classname
            data = test_case["data"]
            expected_errors = test_case["expected_errors"]

            # Dynamically load the contract class
            module_name = "pyveritas.contracts"  # Assuming contracts are in pyveritas/contracts.py
            module = importlib.import_module(module_name)
            contract_class = getattr(module, contract)
            contract_instance = contract_class()

            validator = Validator(contract_instance)
            errors = validator.validate(data)

            if set(errors) == set(expected_errors):
                print(f"PASSED: {description}")
            else:
                print(f"FAILED: {description} - Expected errors: {expected_errors}, Got: {errors}")

        print(f"Test suite {self.name} complete.")

    def summary(self):
        """Prints a summary of test results.

        This method has been removed and is not used for the "base.py" file has been removed
        """
        pass

    def _evaluate_test(self, description: str, data: t.Dict, errors: t.List[str], expected_errors: t.List[str]):
        """
        Evaluates the test result and updates the test suite statistics.
        """
        if set(errors) == set(expected_errors):
            print(f"PASSED: {description}")
        else:
            print(f"FAILED: {description} - Expected errors: {expected_errors}, Got: {errors}")