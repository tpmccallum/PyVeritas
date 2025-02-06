
# PyVeritas - Easy Testing for Python

Welcome to PyVeritas, a user-friendly testing framework that leverages JSON for defining tests, making it perfect for both beginners and seasoned developers. This framework supports both unit testing and fuzzing, ensuring your code is reliable and secure.

# Installation

Install PyVeritas using pip:

```bash
pip install pyveritas
```

# Getting Started

PyVeritas uses JSON for test case definitions, which are simple and intuitive even if you're new to JSON or Python.

# Basics of a Test Case

- **Name**: A descriptive name for your test.

- **Function**: The Python function you're testing.

- **Input**: Parameters to pass to the function.

- **Output**: Expected results.

- **Iterations**: Number of test runs for fuzzing (optional).

- **Exception**: Expected exceptions (optional).

# JSON Structure Example

Here's how a test case looks in JSON:

```json
{
  "enabled": 1,
  "function_name": "your_function",
  "description": "What this test checks",
  "input": [
    {"name": "parameter_name", "value": "parameter_value", "type": "type_of_parameter"}
  ],
  "output": [
    {"name": "return_value_name", "value": "expected_return_value", "type": "type_of_return"}
  ],
  "iterations": 100,
  "exception": "ExpectedExceptionType",
  "exception_message": "Expected error message"
}
```

# Types of Inputs

**Value**: Direct value to use.

**Regular Expression**: For generating values matching a pattern.

**Range**: For generating numbers within specified limits.

# Precedence:

`value` (highest priority)
`regular_expression` (second highest priority)
`range` (third highest priority)
Items, within the `input` tuple that are without `value`, `regular_expression` and `range` will be automatically assigned a random `value` on the proviso that the item does have a `type` i.e. `"int"`, `"float"`.

# Example Test Cases

Below are a few test case examples.

# Basic Function

Here is a function converting Celsius to Fahrenheit:

```python
def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32
```

## Example 1: Explicit Value

The following test has one item in the `input` tuple. The item has a `value` of `0`:

```json
{
  "enabled": 1,
  "function_name": "celsius_to_fahrenheit",
  "description": "Convert 0°C to Fahrenheit",
  "input": [{"name": "celsius", "value": 0, "type": "float"}],
  "output": [{"name": "result", "value": 32, "type": "float"}]
}
```

## Example 2: Fuzzing with Range

The following test has one item in the `input` tuple. The item has no `value` set. Therefore, PyVeritas will automatically create a random value within the `range` of `min` -100 and `max` 100:

```json
{
  "enabled": 1,
  "function_name": "celsius_to_fahrenheit",
  "description": "Fuzz test for various temperatures",
  "input": [
    {"name": "celsius", "type": "float", "range": {"min": -100, "max": 100}}
  ],
  "output": [],
  "iterations": 1000
}
```

When a random value is automatically created, PyVeritas repeats the random value creation and testing for the function one thousand times (as defined in the `iterations` field). This is fuzzing and is great for discovering edge cases without you needing to hand write hundreds of tests with a different `value`.

## Example 3: Using Regular Expressions

The following test has one item in the `input` tuple. The item has no `value` set. Therefore, PyVeritas will automatically create a random value that adheres to the `regular_expression` (in this case a random email string):

```json
{
  "enabled": 1,
  "function_name": "validate_email",
  "description": "Check if email matches regex",
  "input": [
    {"name": "email", "regular_expression": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$", "type": "string"}
  ],
  "output": [{"name": "is_valid", "value": true, "type": "bool"}],
  "iterations": 50
}
```

Again, when a random value is automatically created, PyVeritas repeats the random value creation and testing for the function one thousand times (as defined in the `iterations` field). This is fuzzing and is great for discovering edge cases without you needing to hand write hundreds of tests with a different `value`.

# Running Tests
Here's how to set up and run your tests. Let's use the temperature conversion function from above. Create a file called `my_tests.py`, and add the following code:

```python
import argparse
from pyveritas.unit import VeritasUnitTester


def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

def original_script_logic():
    print(f"0°C in Fahrenheit: {celsius_to_fahrenheit(0):.2f}")

def run_unit_tests():
    # Create an instance of the testing suite
    tester = VeritasUnitTester("My Test Suite")

    # Add your individual test cases here
    tester.add(
        {
            "enabled": 1,
            "function_name": "celsius_to_fahrenheit",
            "description": "Convert 0°C to Fahrenheit",
            "input": [{"name": "celsius", "value": 0, "type": "float"}],
            "output": [{"name": "result", "value": 32, "type": "float"}],
        },
        {
            "enabled": 1,
            "function_name": "celsius_to_fahrenheit",
            "description": "Fuzz test for various temperatures",
            "input": [
                {"name": "celsius", "type": "float", "range": {"min": -100, "max": 100}}
            ],
            "output": [],
            "iterations": 1000,
        },
    )

    tester.run()
    tester.summary()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run functions or perform tests")
    parser.add_argument("--unit", action="store_true", help="Run tests")
    args = parser.parse_args()

    if args.unit:
        run_unit_tests()
    else:
        original_script_logic()

```


