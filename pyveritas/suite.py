from colorama import Fore, Style

class VeritasTestSuite:
    """
    A suite for running unit tests with customizable test cases and result summaries.

    Attributes:
        name (str): The name of the test suite.
        tests (list): A list of tests, each represented by a tuple (description, test_function, params, should_raise).
        passed (int): The number of tests that passed.
        failed (int): The number of tests that failed.
        failed_tests (list): A list of failed test descriptions.
    """

    def __init__(self, name):
        """
        Initializes the test suite with a name.

        Args:
            name (str): The name of the test suite.
        """
        self.name = name
        self.tests = []
        self.passed = 0
        self.failed = 0
        self.failed_tests = []

    def test(self, description, test_function, params=None, should_raise=None):
        """
        Adds a test case to the suite, supporting parameterization.

        Args:
            description (str): A brief description of the test case.
            test_function (callable): The function to be tested.
            params (list, optional): A list of tuples with parameters for the test function.
            should_raise (Exception, optional): An expected exception type, if applicable.
        """
        if params is None:
            params = [(None,)]  # Default to no parameters for a non-parameterized test

        # Each test will be parameterized by the provided params
        self.tests.append((description, test_function, params, should_raise))

    def run(self):
        """
        Executes all tests in the suite and reports results, handling parameterized tests.
        """
        print(f"Running test suite: {self.name}")
        for i, (desc, func, params, should_raise) in enumerate(self.tests, 1):
            for param_set in params:
                try:
                    # Call the function with the current parameter set
                    result = func(*param_set)

                    # Check for expected exceptions
                    if should_raise:
                        self.failed += 1
                        self.failed_tests.append(f"{desc} with params {param_set}")
                        print(f"{Fore.RED}Test {i} FAILED: {desc} (Exception was expected but not raised){Style.RESET_ALL}")
                    else:
                        self.passed += 1
                        print(f"{Fore.GREEN}Test {i} PASSED: {desc} with params {param_set}{Style.RESET_ALL}")
                except Exception as e:
                    # Handle expected exceptions
                    if should_raise and isinstance(e, should_raise):
                        self.passed += 1
                        print(f"{Fore.GREEN}Test {i} PASSED: {desc} with params {param_set} (Expected exception raised: {e}){Style.RESET_ALL}")
                    else:
                        self.failed += 1
                        self.failed_tests.append(f"{desc} with params {param_set} (Unexpected exception: {e})")
                        print(f"{Fore.RED}Test {i} FAILED: {desc} with params {param_set} (Unexpected exception: {e}){Style.RESET_ALL}")

    def summary(self):
        """
        Prints a summary of test results, including passed and failed tests.
        """
        print("\n" + "-" * 40)
        print(f"Test Summary for Suite: {self.name}")
        print(f"Total Tests Run: {len(self.tests)}")
        print(f"{Fore.GREEN}Passed: {self.passed}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {self.failed}{Style.RESET_ALL}")
        if self.failed_tests:
            print("\nFailed Tests:")
            for failure in self.failed_tests:
                print(f"  - {failure}")

