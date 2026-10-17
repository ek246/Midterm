from dataclasses import dataclass
from typing import Any
from decimal import Decimal, InvalidOperation
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError

@dataclass
class InputValidators:

    @staticmethod
    def validate_input(value: Any, config: CalculatorConfig) -> Decimal:
        try:
            if isinstance(value, str):
                value = value.strip()
            number = Decimal(str(value))
            if abs(number) > config.max_value:
                raise ValidationError(f"Input value {number} exceeds the maximum allowed value of {config.max_value}.")
            return number.normalize()
        except (InvalidOperation) as e:
            raise ValidationError(f"Invalid input: {value}. Please enter a valid number.") from e