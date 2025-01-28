# PyVeritas

Robust, user-friendly unit testing and fuzzing support for your Python application. Designed to be simple (easy to code your tests) and accessible (all of your testing in the one place).

# 🚀 Overview

PyVeritas is your easy-to-use software testing framework. PyVeritas combines unit testing, and the randomness of fuzzing to help you ensure the reliability and quality of your Python code.

# 🌟 Features

**Fuzzing**: Create meaningful fuzzing inputs tailored to your specific code logic.

**Unit Testing**: Write and run lean and relevant tests for your existing Python code.

# 🛠️ Installation

PyVeritas is easy to install via pip:

```bash
pip install pyveritas
```

# ✨ Quick Start

Example, testing a calculator function. Let's say you had a Python file called `my_code.py` where you had implemented a `calculate_discount()` function. 

If you add the `run_unit_tests()` and `run_fuzz_tests()`, as shown below, you can ensure the robustness of your code:

```python
import argparse
from pyveritas import VeritasTestSuite, VeritasFuzzer

# Pre-existing function to test
def calculate_discount(price: float, discount: float) -> float:
    if price <= 0 or discount < 0 or discount > 100:
        raise ValueError("Invalid price or discount")
    return price * (1 - discount / 100)

def run_unit_tests():
    # Test suite
    suite = VeritasTestSuite("DiscountCalculatorTests")
    
    suite.test("Discount calculation is correct", lambda: calculate_discount(100, 20) == 80)
    suite.test("Invalid discount should raise ValueError", lambda: calculate_discount(-10, 50), should_raise=ValueError)
    
    suite.run()  # Run the test suite
    suite.summary()  # Output the summary of the test suite

def run_fuzz_tests():
    # Fuzz tests
    fuzzer = VeritasFuzzer("DiscountCalculatorFuzzing")
    
    fuzzer.test(
        input_spec={
            "price": lambda: VeritasFuzzer.float_range(0, 1000),
            "discount": lambda: VeritasFuzzer.float_range(0, 100),
        },
        iterations=1000,
    )
    fuzzer.run(calculate_discount)  # Run the fuzz tests
    fuzzer.summary()  # Output the summary of the fuzz tests

def main():
    parser = argparse.ArgumentParser(description="Run tests or fuzz tests on your Python code.")
    parser.add_argument('action', choices=['test', 'fuzz'], help="Specify 'test' to run unit tests or 'fuzz' to run fuzzing tests.")
    args = parser.parse_args()
    
    if args.action == 'test':
        run_unit_tests()
    elif args.action == 'fuzz':
        run_fuzz_tests()

if __name__ == "__main__":
    main()
```

When calling the `test` and `fuzz` as arguments, your code (example as shown above) will return something similar to the following:

```bash
$ python3 tests/my_code.py test

Running test suite: DiscountCalculatorTests
Test 1 PASSED: Discount calculation is correct
Test 2 PASSED: Invalid discount should raise ValueError (Expected exception raised: Invalid price or discount)

----------------------------------------
Test Summary for Suite: DiscountCalculatorTests
Total Tests Run: 2
Passed: 2
Failed: 0
```

```bash
$ python3 tests/my_code.py fuzz
Running fuzz tests on function: calculate_discount
Fuzzing iteration 1: PASSED with inputs {'price': 748.5057904261024, 'discount': 84.29362340396797}
Fuzzing iteration 2: PASSED with inputs {'price': 595.7437257017222, 'discount': 49.09955272366074}

...

Fuzzing iteration 999: PASSED with inputs {'price': 144.38623673700423, 'discount': 41.81132465276192}
Fuzzing iteration 1000: PASSED with inputs {'price': 934.2668869132724, 'discount': 48.77225754237649}

----------------------------------------
Fuzzing Summary for Function: DiscountCalculatorFuzzing
Total Iterations: 1000
Passed: 1000
Failed: 0
```

PyVeritas aims to simplify advanced testing scenarios without requiring users to write extensive boilerplate code or understand complex concepts.
