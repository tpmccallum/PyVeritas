import argparse
from pyveritas.unit import VeritasUnitTester
from pyveritas.fuzz import VeritasFuzzer


def convert_celsius_to_fahrenheit(celsius):
    """Convert temperature from Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def print_arguments(one, two, three, four):
    # Print the arguments for testing purposes
    print(f"Arguments: {one}, {two}, {three}, {four}")


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two points on earth in kilometers."""
    from math import radians, sin, cos, sqrt, atan2

    R = 6371  # Earth radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def validate_ip_address(ip):
    """Validate if the given string is a valid IP address."""
    import re

    pattern = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    )
    return bool(pattern.match(ip))


def validate_email(email):
    """Validate if the given string is a valid email address."""
    import re

    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return bool(pattern.match(email))


def original_script_logic():
    """Demonstrates the functionality of each function with example parameters."""
    print(
        f"Distance between Berlin and London: {calculate_distance(52.5200, 13.4050, 51.5074, -0.1278):.2f} km"
    )
    print(f"Email 'invalid.email@' valid: {validate_email('invalid.email@')}")


def run_unit_tests():
    """Runs unit tests for the IoT functions."""
    unit_tester = VeritasUnitTester("Print Arguments Unit Tests")

    unit_tester.add(
        {
            "enabled": 1,
            "function_name": "print_arguments",
            "description": "Check for combinations of arguments",
            "input": [
                # Explicit int value
                {"name": "zero", "value": 52, "type": "int"},
                # Explicit float value
                {"name": "one", "value": 52.52, "type": "float"},
                # Explicit type float with range - no explicit value
                {"name": "two", "type": "float", "range": {"min": -50, "max": 50}},
                # Explicit type float - no range - no explicit value
                {"name": "three", "type": "float"},
                # Explicit type int with range - no explicit value
                {"name": "four", "type": "int", "range": {"min": 40, "max": 43}},
                # Explicit type int - no range - no explicit value
                {"name": "five", "type": "int"},
                # Explicit type string with value
                {"name": "six", "type": "string", "value": "Hello"},
                # Regular expression for int no range
                {
                    "name": "seven",
                    "regular_expression": r'^\d+$',
                    "type": "int",
                },
                # Regular expression for int with range
                {
                    "name": "eight",
                    "regular_expression": r'^\d+$',
                    "type": "int",
                    "range": {"min": -30000, "max": 300000}
                },
                # Regular expression for int (specifying digits) with no range
                {
                    "name": "nine",
                    "regular_expression": r'^\d{5}$',
                    "type": "int",
                },
                # Regular expression for int (specifying digits) with range
                {
                    "name": "ten",
                    "regular_expression": r'^\d{5}$',
                    "type": "int",
                    "range": {"min": -30000, "max": 300000}
                },
                # Regular expression for int (specifying digits) with regex taking precedence   
                {
                    "name": "eleven",
                    "regular_expression": r'^\d{5}$',
                    "type": "int",
                    "range": {"min": -1000, "max": 2000}
                },
                # Regular expression for float no range
                {
                    "name": "twelve",
                    "regular_expression": r'^-?\d+\.\d+$',
                    "type": "float",
                },
                # Regular expression for float with range
                {
                    "name": "thirteen",
                    "regular_expression": r'^-?\d+\.\d+$',
                    "type": "float",
                    "range": {"min": -3000.00, "max": 300.00}
                },
                # Regular expression for float (specifying digits before decimal) no range
                {
                    "name": "fourteen",
                    "regular_expression": r'^-?\d{5}\.\d+$',
                    "type": "float",
                },
                # Regular expression for float (specifying digits before and after decimal) no range
                {
                    "name": "fifteen",
                    "regular_expression": r'^-?\d{5}\.\d{5}$',
                    "type": "float",
                },
                # Regular expression for float (specifying digits only after decimal) no range
                {
                    "name": "sixteen",
                    "regular_expression": r'^-?\d+\.\d{6}$',
                    "type": "float",
                },
                # Regular expression for float (not specifying digits) with range
                {
                    "name": "seventeen",
                    "regular_expression": r'^-?\d+\.\d+$',
                    "type": "float",
                    "range": {"min": -3000.00, "max": 300.00}
                },
                # Regular expression for float (not specifying digits) without range
                {
                    "name": "eighteen",
                    "regular_expression": r'^-?\d+\.\d+$',
                    "type": "float"
                },
                # Regular expression for float (specifying digits before decimal) with range
                {
                    "name": "nineteen",
                    "regular_expression": r'^-?\d{4}\.\d+$',
                    "type": "float",
                    "range": {"min": -9999.00, "max": 9999.00}
                },
                # Regular expression for float (specifying digits after decimal) with range
                {
                    "name": "twenty",
                    "regular_expression": r'^-?\d+\.\d{7}$',
                    "type": "float",
                    "range": {"min": 3000.0, "max": 3000.9999999}
                },
                # # Regular expression for float with range
                # {
                #     "name": "seven",
                #     "regular_expression": r"[-+]*(?:\d+\.\d*|\.?\d+)(?:[eE][-+]?\d+)?",
                #     "type": "float",
                #     "range": {"min": 0, "max": 100},
                # },
                # # Regular expression for float TODO
                # {
                #     "name": "seven",
                #     "regular_expression": r"[-+]*(?:\d+\.\d*|\.?\d+)(?:[eE][-+]?\d+)?",
                #     "type": "float",
                # },
                # # Regular expression for float
                # {
                #     "name": "seven",
                #     "regular_expression": r"[-+]*(?:\d+\.\d*|\.?\d+)(?:[eE][-+]?\d+)?",
                #     "type": "float",
                # },
                # # Regular expression for float
                # {
                #     "name": "seven",
                #     "regular_expression": r"[-+]*(?:\d+\.\d*|\.?\d+)(?:[eE][-+]?\d+)?",
                #     "type": "float",
                # },
            ],
            "output": [{"name": "distance", "value": 925.8, "type": "float"}],
            "exception": "",
            "exception_message": "",
            "iterations": 1000,
        }
    )

    # unit_tester.add(
    #     {
    #         "enabled": 1,
    #         "function_name": "calculate_distance",
    #         "description": "Calculate distance between two points on earth",
    #         "input": [
    #             {"name": "lat1", "value": 52.52, "type": "float"},
    #             {"name": "lon1", "value": 13.405, "type": "float"},
    #             {"name": "lat2", "value": 51.5074, "type": "float"},
    #             {"name": "lon2", "value": -0.1278, "type": "float"},
    #         ],
    #         "output": [{"name": "distance", "value": 925.8, "type": "float"}],
    #         "exception": "",
    #         "exception_message": "",
    #         "iterations": 1000,
    #     }
    # )

    unit_tester.run()
    unit_tester.summary()


def run_fuzz_tests():
    """Runs fuzz tests for the IoT functions."""
    fuzz_tester = VeritasFuzzer("IoT Fuzz Tests")

    fuzz_tester.add(
        {
            "enabled": 1,
            "function_name": "calculate_stock_on_hand",
            "description": "Test for generating sales report summary",
            "input": [
                {
                    "name": "sales_data",
                    "value": '[{"product": "Gadget", "units": 100}, {"product": "Widget", "units": 50}]',
                    "type": "str",
                    "regular_expression": '[{"product": "[A-Za-z]+", "units": "\\d+"}(,{"product": "[A-Za-z]+", "units": "\\d+"})*]',
                },
                {
                    "name": "report_type",
                    "value": "Summary",
                    "type": "str",
                    "regular_expression": "^(Summary|Detailed)$",
                },
                {
                    "name": "customer_id",
                    "value": 12345,
                    "type": "int",
                    "regular_expression": "[A-Za-z0-9]{5,10}",
                },
                {
                    "name": "price",
                    "value": 100,
                    "type": "float",
                    "range": {"min": 50, "max": 100},
                },
            ],
            "output": [
                {"name": "total_units", "value": 150, "type": "int"},
                {
                    "name": "company_id",
                    "value": 12345,
                    "type": "int",
                    "regular_expression": "[A-Za-z0-9]{5,10}",
                },
                {
                    "name": "price",
                    "value": 100,
                    "type": "float",
                    "range": {"min": 50, "max": 100},
                },
            ],
            "exception": "ValueError",
            "exception_message": "Invalid sales data format or report type",
            "iterations": 1000,
        }
    )
    fuzz_tester.run()
    fuzz_tester.summary()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run IoT functions or perform tests")
    parser.add_argument("--unit", action="store_true", help="Run unit and fuzz tests")
    parser.add_argument("--fuzz", action="store_true", help="Run unit and fuzz tests")
    args = parser.parse_args()

    if args.unit:
        run_unit_tests()
    elif args.fuzz:
        run_fuzz_tests()
    else:
        original_script_logic()
