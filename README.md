# PyVeritas: The Declarative Data Contract Engine for Python

[![License](https://img.shields.io/badge/license-Apache2-blue.svg)](LICENSE)  
[![PyPI Version](https://img.shields.io/pypi/v/pyveritassvg)](https://pypi.org/project/pyveritas/) 

PyVeritas empowers you to define and enforce data contracts in Python with a declarative, code-centric approach. Ensure data integrity, simplify integrations, and build robust applications by defining your data's expected structure and constraints **as code**.

## Key Features

*   **Declarative Data Contracts:** Define data contracts as Python classes, making them readable, maintainable, and testable.
*   **Composable Rules:** Build complex validation logic by combining simple rules using logical operators (AND, OR, NOT).
*   **Extensible Architecture:** Easily create custom rules to handle specific validation requirements.
*   **Clear Error Reporting:** Get detailed error messages that pinpoint the exact cause of validation failures.
*   **Framework Integrations:** (Future) Seamlessly integrate with popular Python frameworks like Pydantic, Flask, FastAPI, and Django REST Framework.
*   **Fuzzing Support:** (In Progress) Generate realistic test data based on your data contracts to uncover potential vulnerabilities.

## Getting Started

Follow the steps below to get started.

### Installation

Create a Python environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install PyVeritas:

```bash
pip install pyveritas
```

Install dependencies:

```bash
# Standard use - (MANDATORY)
pip install -r requirements.txt
# For contributing developers only - (OPTIONAL)
pip install -r dev-requirements.txt
```

