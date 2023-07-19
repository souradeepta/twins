import unittest
import os

# Get the current directory (where test_runner.py is located)
current_dir = os.path.dirname(__file__)

def run_tests():
    # Load all test modules in the "tests" folder
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir=os.path.join(current_dir, "tests"))

    # Create a test runner
    test_runner = unittest.TextTestRunner()

    # Run the tests
    result = test_runner.run(test_suite)

    # Return the test result
    return result

if __name__ == "__main__":
    test_result = run_tests()

    # Check if any failures occurred during the test run
    if test_result.failures or test_result.errors:
        exit(1)
