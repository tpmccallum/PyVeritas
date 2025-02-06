from pyveritas.base import VeritasBase
from pyveritas.base import logger
import re
import sys
import random
import importlib
import concurrent.futures

class VeritasUnitTester(VeritasBase):

    def _generate_value(self, input_spec):
        """
        Generates a value based on the input specification, respecting the precedence rules:
        - value > regular_expression > range > type
        """
        name = input_spec["name"]
        type_spec = input_spec["type"]

        if "value" in input_spec:
            if "regular_expression" in input_spec or "range" in input_spec:
                logger.warning(
                    f"Warning: 'value' precedence over 'regular_expression'/'range' for {name}"
                )
            return input_spec["value"]

        elif "regular_expression" in input_spec:
            regex = input_spec["regular_expression"]
            return self._generate_number_from_regex(type_spec, regex)

        elif "range" in input_spec:
            min_value, max_value = input_spec["range"]["min"], input_spec["range"]["max"]
            if min_value > max_value:
                raise ValueError(
                    f"Invalid range for {name}: min {min_value} must be less than max {max_value}"
                )
            return self._generate_number_from_range(type_spec, min_value, max_value)

        elif type_spec == "int":
            return random.randint(-sys.maxsize - 1, sys.maxsize)
        elif type_spec == "float":
            return random.uniform(sys.float_info.min, sys.float_info.max)
        else:
            raise ValueError(f"Unsupported input type: {type_spec}")

    def _generate_number_from_regex(self, value_type, regex):
        """
        Generates a random number (int or float) based on a regex pattern.
        """
        if value_type == "int":
            int_match = re.search(r"\\d{(\d+)}", regex)
            int_digits = int(int_match.group(1)) if int_match else None

            if int_digits:
                lower = 10**(int_digits - 1)
                upper = (10**int_digits) - 1
            else:
                lower = -sys.maxsize - 1
                upper = sys.maxsize

            return random.randint(lower, upper)

        elif value_type == "float":
            int_match = re.search(r"\\d{(\d+)}", regex)
            float_match = re.search(r"\.\\d{(\d+)}", regex)
            int_digits = int(int_match.group(1)) if int_match else None
            decimal_places = int(float_match.group(1)) if float_match else 2

            lower = 10**(int_digits - 1) if int_digits else -100000
            upper = (10**int_digits) - 1 if int_digits else 100000
            integer_part = random.randint(int(lower), int(upper))
            decimal_part = random.uniform(0, 1)

            return float(f"{integer_part}.{str(decimal_part)[2:2+decimal_places]}")

    def _generate_number_from_range(self, value_type, min_val, max_val):
        """
        Generates a random number (int or float) within a given range.
        """
        if value_type == "int":
            return random.randint(min_val, max_val)
        elif value_type == "float":
            return random.uniform(min_val, max_val)

    def _run_single_test(self, func, case, i):
        """
        Runs a single test iteration.
        """
        input_params = {}
        for input_spec in case.get("input", []):
            input_params[input_spec["name"]] = self._generate_value(input_spec)

        expected_exception = case.get("exception", None)
        exception_message = case.get("exception_message", None)

        try:
            result = func(**input_params)
            self._evaluate_test(
                f"Test {i}",
                input_params,
                result,
                expected_exception,
                exception_message,
            )
        except Exception as e:
            self._evaluate_test(
                f"Test {i}", input_params, e, expected_exception, exception_message
            )

    def run(self, parallel=True):
        """
        Executes all tests in the suite and reports results, incorporating fuzzing logic.
        """
        print(f"Test Name: {self.name}...")
        for case in self.test_cases:
            iterations = case.get('iterations', 100)
            
            # Determine if fuzzing should be activated
            fuzz_active = any(
                'value' not in input_spec 
                or 'regular_expression' in input_spec 
                or 'range' in input_spec 
                for input_spec in case.get("input", [])
            )

            # Dynamically import the module where the functions are defined
            mod = importlib.import_module("tests.truth_statements")
            func = getattr(mod, case['function_name'])

            if fuzz_active:
                if parallel:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        futures = [
                            executor.submit(self._run_single_test, func, case, i)
                            for i in range(iterations)
                        ]
                        concurrent.futures.wait(futures)
                else:
                    for i in range(iterations):
                        self._run_single_test(func, case, i)
            else:
                # If no fuzzing, run the test once with static values
                self._run_single_test(func, case, 0)

        print(f"Test Suite: {self.name} complete.")