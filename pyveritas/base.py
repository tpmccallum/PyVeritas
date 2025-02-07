import argparse
from colorama import Fore, Style
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("VeritasBase")


class VeritasBase:
    """
    Base class for test suites, providing common functionality for running tests,
    managing test results, and reporting.
    """

    def __init__(self, name):
        self.name = name
        self.passed = 0
        self.failed = 0
        self.failed_items = []
        self.test_cases = []

    def add(self, test_case_json):
        """
        Adds a test case to the suite from a JSON structure.

        Args:
            test_case_json (dict): A dictionary containing all test case details.
        """
        # Default to enabled if not specified
        if test_case_json.get("enabled", 1):
            # The JSON is allowed to have no items in the `input` tuple` this is valid
            if "input" not in test_case_json:
                print(f"Adding test case with no input arguments: {test_case_json}")
            else:
                # The input JSON must contain a `type` value for each input parameter in the JSON
                for input_spec in test_case_json.get("input", []):
                    if "type" not in input_spec:
                        raise ValueError(
                            f"Missing 'type' for input parameter: {input_spec.get('name', 'Unnamed Input')}"
                        )
                    # The input JSON must contain a `name` value for each input parameter in the JSON
                    if "name" not in input_spec:
                        raise ValueError(
                            f"Missing 'name' for input parameter: {input_spec.get('type', 'Unnamed Type')}"
                        )
                    # If neither `value`, `regular_expression`, nor a properly set `range` is present for any of the items in the `input` tuple, the add process stops with an error that helps the user write better JSON for their test.
                    if "value" not in input_spec and "regular_expression" not in input_spec and "range" not in input_spec and "type" not in input_spec:
                        raise ValueError(
                            f"Either 'value', 'regular_expression', 'type', or 'range' must be specified for each input '{input_spec['name']}'."
                        )
            logger.info(
                f"Adding test case: {test_case_json.get('description', 'Unnamed Test Case')}"
            )
            self.test_cases.append(test_case_json)
        else:
            logger.info(
                f"Test case: {test_case_json.get('description', 'Unnamed Test Case')} is disabled."
            )

    def _evaluate_test(
        self, desc, input_params, result, expected_exception, exception_message
    ):
        if expected_exception:
            if isinstance(result, Exception):
                # Check if exception type matches
                if result.__class__.__name__ == expected_exception:
                    # Check if the exception message matches (if provided)
                    if exception_message is None or exception_message in str(result):
                        self.passed += 1
                        logger.info(
                            f"{Fore.GREEN}PASSED: {desc} with params {input_params} (Expected exception: {expected_exception}){Style.RESET_ALL}"
                        )
                        return
                    else:
                        error_msg = f"Expected exception message: '{exception_message}', Got: '{str(result)}'"
                else:
                    error_msg = f"Expected exception: {expected_exception}, Got: {result.__class__.__name__}"
            else:
                error_msg = f"Expected exception: {expected_exception}, but no exception was raised."

            self.failed += 1
            self.failed_items.append((desc, input_params, error_msg))
            logger.error(f"{Fore.RED}FAILED: {desc} with params {input_params} ({error_msg}){Style.RESET_ALL}")


    def summary(self):
        """
        Prints a summary of test results, including passed and failed tests.
        """
        logger.info("\n" + "-" * 40)
        logger.info(f"Test Summary for Suite: {self.name}")
        logger.info(f"Total Tests Run: {self.passed + self.failed}")
        logger.info(f"{Fore.GREEN}Passed: {self.passed}{Style.RESET_ALL}")
        logger.info(f"{Fore.RED}Failed: {self.failed}{Style.RESET_ALL}")
        if self.failed_items:
            logger.info("\nFailed Tests:")
            for desc, inputs, error in self.failed_items:
                logger.info(f"  - {desc} with inputs {inputs}: {error}")
