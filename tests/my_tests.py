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
        })
    tester.add(
        {
            "enabled": 1,
            "function_name": "celsius_to_fahrenheit",
            "description": "Fuzz test for various temperatures",
            "input": [
                {"name": "celsius", "type": "float", "range": {"min": -100, "max": 100}}
            ],
            "output": [],
            "iterations": 1000,
        })

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
