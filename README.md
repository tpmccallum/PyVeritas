# PyVeritas

Revolutionizing Python testing with adaptive, intelligent, and developer-friendly tools.

# 🚀 Overview

PyVeritas is an advanced software testing framework designed to push the boundaries of Python testing. By combining the precision of unit testing, the randomness of fuzzing, and the adaptability of AI, PyVeritas helps developers create robust, reliable, and high-quality Python code effortlessly.

PyVeritas is code-aware, behavior-driven, and environment-adaptive. It doesn’t just test your code—it learns from it, evolves with it, and ensures every corner is thoroughly validated.

# 🌟 Features

Intelligent Fuzzing: Automatically generates meaningful fuzzing inputs tailored to your specific code logic.
Behavioral Validation: Compare your program's outputs against expected behaviors using AI models.
Dynamic Test Optimization: Keeps your test suite lean and relevant by analyzing historical failures and code changes.
Cross-Environment Simulation: Test across multiple Python versions and runtime environments.
Actionable Insights: Provides real-time feedback on test coverage, bottlenecks, and high-risk areas.

# 🛠️ Installation

PyVeritas is easy to install via pip:

```bash
pip install pyveritas
```

# ✨ Quick Start

Example, Testing a Calculator Function:

```python
from pyveritas import VeritasTestSuite, VeritasFuzzer

# Define the function to test
def calculate(operation: str, a: float, b: float) -> float:
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        return a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")

# Create and run a test suite
with VeritasTestSuite("CalculatorTests") as suite:
    suite.test("Addition works", lambda: calculate("add", 2, 3) == 5)
    suite.test("Division by zero", lambda: calculate("divide", 10, 0), should_raise=ValueError)

# Fuzz the function
VeritasFuzzer(calculate).run(
    input_spec={
        "operation": VeritasFuzzer.choice(["add", "subtract", "multiply", "divide", "unknown"]),
        "a": VeritasFuzzer.float_range(-1e6, 1e6),
        "b": VeritasFuzzer.float_range(-1e6, 1e6),
    },
    iterations=1000
)
```

# 🧠 How It Works

## Code Analysis

PyVeritas inspects your code for patterns, structure, and dependencies.

## Test Generation

Automatically generates tests based on code analysis and input specifications.

## Execution

Runs the tests with real-time metrics on coverage and edge-case detection.

# Insights

Provides actionable feedback, including risk areas and potential optimizations.

# 🛡️ Why PyVeritas?
PyVeritas doesn’t just test—it thinks. By leveraging machine learning, dynamic adaptation, and intelligent fuzzing, PyVeritas ensures you catch bugs that other tools miss. Whether you’re developing simple scripts or large-scale applications, PyVeritas is your ultimate testing companion.

# 🏗️ Roadmap
- [ ] Build the foundational test suite framework.
- [ ] Integrate intelligent fuzzing with customizable input specifications.
- [ ] Develop AI-driven behavioural models for output validation.
- [ ] Add cross-environment compatibility testing.
- [ ] Create a comprehensive feedback and insights dashboard.
- [ ] Write comprehensive documentation
- [ ] Create contribution guide

# 📚 Documentation

Comprehensive documentation is available at PyVeritas Docs.

# 🖤 Contributing
Contributions are welcome! Please read our CONTRIBUTING.md for guidelines on how to get started.

# 📝 License

This project is licensed under the Apache2 License. See the LICENSE file for details.
