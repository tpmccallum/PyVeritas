# PyVeritas: The Declarative Data Contract Engine for Python

[![License](https://img.shields.io/badge/license-Apache2-blue.svg)](LICENSE)  

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

Create a new file called `validate_user.py` and fill with the following code:

```python
from pyveritas.contracts import UserContract
from pyveritas.validator import Validator

user_contract = UserContract()
validator = Validator(user_contract)

user_data = {"name": "John", "email": "test@example.com", "age": 30}

if validator.is_valid(user_data):
    print("User data is valid!")
else:
    print("User data is invalid:")
    errors = validator.validate(user_data)
    for error in errors:
        print(f"- {error}")
```

Then run the file:

```python
python3 validate_user.py 
```

The above command will produce the following result:

```console
User data is valid!
```

---

# Contributing (contributions welcome)

If you'd like to contribute to PyVeritas, please follow these steps:

1.  Fork the repository on GitHub.
2.  Clone your fork to your local machine:

```bash
git clone git@github.com:tpmccallum/PyVeritas.git
```

3.  Create a new branch:

```bash
git checkout -b my_new_branch
```
4.  Create a new upstream:

```bash
git remote add upstream https://github.com/tpmccallum/PyVeritas
```

5.  Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate.bat  # On Windows
```

4.  Install the development dependencies:

```bash
pip install -r dev-requirements.txt
```

5.  Make your changes.

6.  Generate documentation:

```bash
cd PyVeritas/docs
make html
```

7. Push changes to the GitHub repository:

```bash
git add .
git commit -m "Your Message"
git push -u origin my_new_branch
```

# Cutting a new release

Update the version/release (increment the `version` in the `pyproject.toml` file):

```toml
version = "x.x.x"
```

Push changes to the GitHub repository:

```bash
git add .
git commit -m "Your Message"
git push -u origin my_new_branch
```

Use flit to build and publish:

```bash
cd PyVeritas
flit build
flit publish
```

# Testing in place (without cutting a new release for each change)

If you are making changes to the versioned files (while testing in a non-versioned area) then do the following:

```bash
pip3 uninstall PyVeritas -y
rm -rf ./build ./dist ./PyVeritas.egg-info 
rm -rf ./__pycache__ 
python -c "import sys; print(sys.path)" 
pip3 install -e ~/PyVeritas 
```

After all, you want to extensively test locally before pushing to pypi, right?

# Future development

The following is a list of future developments needed:

- A comprehensive library of pre-built rules for common data validation tasks ( which will prevent developers from having to write the same validation logic over and over again)
- Collaboration between developers by providing a common language for defining data contracts
- Demonstrations about using PyVeritas to validate data coming from external APIs.
- Demonstrations about using PyVeritas to validate data as it flows through a data pipeline.
- Instructions and examples of how to use PyVeritas rules within pytest tests.
- Instructions on creating your own custom validation rules.
- Pydantic Integration.
- More detailed error messages that clearly indicate which rule failed and why.
- The ability to customize error messages.
- Lots of real-world examples showing how to use PyVeritas to solve different data validation problems.


