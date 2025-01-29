import argparse
from pyveritas import VeritasTestSuite, VeritasFuzzer

# Function to test
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