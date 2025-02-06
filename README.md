
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
- Name: A descriptive name for your test.
- Function: The Python function you're testing.
- Input: Parameters to pass to the function.
- Output: Expected results.
- Iterations: Number of test runs for fuzzing (optional).
- Exception: Expected exceptions (optional).

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
Value: Direct value to use.
Regular Expression: For generating values matching a pattern.
Range: For generating numbers within specified limits.

# Precedence:
Value (highest priority)
Regular Expression
Range

# Example Test Cases
Below are a few test case examples.

## Example 1: Basic Unit Test
For a function converting Celsius to Fahrenheit:

```python
def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32
```

### The test case:

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
Fuzz testing the same function over a range of temperatures:

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

## Example 3: Using Regular Expressions
Testing email validation:

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

# Running Tests
Here's how to set up and run your tests. Create a file called `my_tests.py`, and add the following code:

```python
from pyveritas.unit import VeritasUnitTester

def run_tests():
    tester = VeritasUnitTester("My Test Suite")
    
    # Add your test cases here
    tester.add({
        "enabled": 1,
        "function_name": "celsius_to_fahrenheit",
        "description": "Convert 0°C to Fahrenheit",
        "input": [{"name": "celsius", "value": 0, "type": "float"}],
        "output": [{"name": "result", "value": 32, "type": "float"}]
    })

    tester.run()
    tester.summary()

if __name__ == "__main__":
    run_tests()
```


