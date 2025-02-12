# tests/test_contracts.py
import pytest
from pyveritas.contracts import UserContract
from pyveritas.validator import Validator

@pytest.fixture
def user_contract():
    return UserContract()

@pytest.fixture
def validator(user_contract):
    return Validator(user_contract)

def test_valid_user_data(validator):
    user_data = {"name": "John", "email": "test@example.com", "age": 30}
    assert validator.is_valid(user_data)

def test_invalid_email(validator):
    user_data = {"name": "John", "email": "invalid-email", "age": 30}
    assert not validator.is_valid(user_data)
    errors = validator.validate(user_data)
    assert "Field 'email' must match the regular expression" in errors[0]

def test_invalid_age(validator):
    user_data = {"name": "John", "email": "test@example.com", "age": "invalid"}
    assert not validator.is_valid(user_data)
    errors = validator.validate(user_data)
    assert "Field 'age' must be of type <class 'int'>" in errors[0]

def test_missing_age(validator):
    user_data = {"name": "John", "email": "test@example.com"}
    assert not validator.is_valid(user_data)
    errors = validator.validate(user_data)
    assert "Field 'age' is required" in errors[0]