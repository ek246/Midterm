import pytest
from decimal import Decimal

from tomlkit import value
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidators  # adjust as per your file structure

# Sample configuration with a max input value of 1 million for testing purposes
config = CalculatorConfig(max_input_value=Decimal('1000000'))

# Test cases for InputValidator.validate_number

def test_validate_number_exceeds_max_value():
    with pytest.raises(ValidationError, match=f"Input value number exceeds the maximum allowed value of {config.max_input_value}."):
        InputValidators.validate_input(Decimal('1000001'), config)