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

# Your function to test
def calculate_discount(price: float, discount: float) -> float:
    """
    Calculates the discounted price.
    
    Args:
        price (float): The original price.
        discount (float): The discount percentage.
    
    Returns:
        float: The final price after applying the discount.
    
    Raises:
        ValueError: If the price is non-positive or discount is out of range.
    """
    if price <= 0 or discount < 0 or discount > 100:
        raise ValueError("Invalid price or discount")
    return price * (1 - discount / 100)

# The run_tests function that you will create for your unit testing - this is just an example of how
def run_tests():
    """Runs unit tests using VeritasTestSuite."""
    suite = VeritasTestSuite("DiscountCalculatorTests")
    
    # Test valid discount calculations
    suite.test(
        "Valid discount calculation",
        calculate_discount,
        test_cases=[
            {"input": {"price": 100, "discount": 20}, "expected_output": 80},
            {"input": {"price": 50, "discount": 10}, "expected_output": 45},
            {"input": {"price": 200, "discount": 50}, "expected_output": 100},
        ]
    )
    
    # Test invalid discount scenarios
    suite.test(
        "Invalid discount should raise ValueError",
        calculate_discount,
        test_cases=[
            {"input": {"price": -10, "discount": 50}, "expected_exception": ValueError},
            {"input": {"price": 100, "discount": -5}, "expected_exception": ValueError},
            {"input": {"price": 100, "discount": 150}, "expected_exception": ValueError},
        ]
    )
    
    suite.run()
    suite.summary()

# The function that you would write to fuzz test your existing Python code - this is just an example of how
def run_fuzz_tests():
    """Runs fuzz tests using VeritasFuzzer."""
    fuzzer = VeritasFuzzer("DiscountCalculatorFuzzing")
    
    # Define test cases for fuzzing
    fuzzer.test(
        test_cases=[
            {"input": {"price": 100, "discount": 20}, "expected_output": 80},
            {"input": {"price": 50, "discount": 10}, "expected_output": 45},
            {"input": {"price": 200, "discount": 50}, "expected_output": 100},
            {"input": {"price": -10, "discount": 50}, "expected_exception": ValueError},  # Invalid input, should raise ValueError
            {"input": {"price": 100, "discount": -5}, "expected_exception": ValueError},  # Invalid input, should raise ValueError
            {"input": {"price": 100, "discount": 150}, "expected_exception": ValueError}, # Invalid input, should raise ValueError
        ],
        iterations=1000,
    )
    
    fuzzer.run(calculate_discount)
    fuzzer.summary()

# You will need to ensure your existing Python code argument parser facilitates the running of test and fuzz - below is an example of how to achieve this easily using Python's argparse library
def main():
    parser = argparse.ArgumentParser(description="Run unit tests or fuzz tests with PyVeritas.")
    parser.add_argument('action', choices=['test', 'fuzz'], help="Specify 'test' for unit tests or 'fuzz' for fuzzing tests.")
    args = parser.parse_args()
    
    if args.action == 'test':
        run_tests()
    elif args.action == 'fuzz':
        run_fuzz_tests()

if __name__ == "__main__":
    main()
```

When calling the `test` and `fuzz` as arguments, your code (example as shown above) will return something similar to the following:

```bash
python3 tests/my_code.py test
```

```bash
python3 tests/my_code.py fuzz
```

PyVeritas aims to simplify advanced testing scenarios without requiring users to write extensive boilerplate code or understand complex concepts.
