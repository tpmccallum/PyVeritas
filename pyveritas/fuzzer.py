import random
from colorama import Fore, Style

class VeritasFuzzer:
    """
    A fuzz testing utility for dynamically testing functions with randomized inputs.

    Attributes:
        name (str): The name of the function or module being tested.
        passed (int): The number of successful fuzz tests.
        failed (int): The number of failed fuzz tests.
        failed_inputs (list): A list of inputs and exceptions for failed tests.
        input_spec (dict): A dictionary defining input specifications for fuzzing.
        iterations (int): The number of fuzz test iterations.
    """

    @staticmethod
    def choice(options):
        """
        Returns a random element from a list of options.

        Args:
            options (list): A list of possible values.
        
        Returns:
            Any: A randomly chosen value from the options.
        """
        return random.choice(options)

    @staticmethod
    def float_range(min_value, max_value):
        """
        Generates a random floating-point number within a specified range.

        Args:
            min_value (float): The lower bound of the range.
            max_value (float): The upper bound of the range.

        Returns:
            float: A randomly generated float within the range.
        """
        return random.uniform(min_value, max_value)

    def __init__(self, name):
        """
        Initializes the fuzzer with a name and default parameters.

        Args:
            name (str): The name of the fuzzing task.
        """
        self.name = name
        self.passed = 0
        self.failed = 0
        self.failed_inputs = []
        self.input_spec = None
        self.iterations = 100

    def test(self, input_spec, iterations=100):
        """
        Defines the input specifications and number of iterations for fuzzing.

        Args:
            input_spec (dict): A dictionary where keys are parameter names and values are functions generating input data.
            iterations (int, optional): The number of test iterations. Default is 100.
        """
        self.input_spec = input_spec
        self.iterations = iterations

    def run(self, function):
        """
        Executes fuzz tests on a specified function.

        Args:
            function (callable): The function to be fuzz-tested.

        Raises:
            ValueError: If `test()` is not called before running.
        """
        if not self.input_spec:
            raise ValueError("Input specification not set. Please call 'test()' first.")
        
        print(f"Running fuzz tests on function: {function.__name__}")
        for i in range(self.iterations):
            inputs = {key: spec() for key, spec in self.input_spec.items()}
            try:
                function(**inputs)
                self.passed += 1
                print(f"{Fore.GREEN}Fuzzing iteration {i+1}: PASSED with inputs {inputs}{Style.RESET_ALL}")
            except Exception as e:
                self.failed += 1
                self.failed_inputs.append((inputs, e))
                print(f"{Fore.RED}Fuzzing iteration {i+1}: FAILED with inputs {inputs} (Exception: {e}){Style.RESET_ALL}")

    def summary(self):
        """
        Prints a summary of the fuzzing results, including passed and failed iterations.
        """
        print("\n" + "-" * 40)
        print(f"Fuzzing Summary for Function: {self.name}")
        print(f"Total Iterations: {self.passed + self.failed}")
        print(f"{Fore.GREEN}Passed: {self.passed}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {self.failed}{Style.RESET_ALL}")
        if self.failed_inputs:
            print("\nFailed Inputs:")
            for inputs, e in self.failed_inputs:
                print(f"  - Inputs: {inputs}, Exception: {e}")
