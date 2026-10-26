from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation 
import logging
from typing import Any, Dict
from app.exceptions import OperationError
from colorama import Fore, just_fix_windows_console, init
init(autoreset=True)

just_fix_windows_console()

@dataclass
class Calculation:
    operation: str
    operand1: Decimal
    operand2: Decimal
    outcome: Decimal = field(init=False)

    timeOfCalc: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        self.outcome = self.calculate()

    def calculate(self) -> Decimal:
        try:
            if self.operation == 'addition':
                return self.operand1 + self.operand2
            elif self.operation == 'subtraction':
                return self.operand1 - self.operand2
            elif self.operation == 'multiplication':
                return self.operand1 * self.operand2
            elif self.operation == 'division':
                self._raise_division_by_zero(self.operand2)
                return self.operand1 / self.operand2
            elif self.operation == 'power':
                self._raise_negative_power(self.operand1, self.operand2)
                return self.operand1 ** self.operand2
            elif self.operation == 'root':
                self._raise_invalid_root(self.operand1, self.operand2)
                return Decimal(pow(float(self.operand1), 1 / float(self.operand2)))
            elif self.operation == 'modulus':
                self._raise_division_by_zero(self.operand2)
                return self.operand1 % self.operand2
            elif self.operation == 'int_division':
                self._raise_division_by_zero(self.operand2)
                return self.operand1 // self.operand2
            elif self.operation == 'percentage_calculation':
                return (self.operand1 / self.operand2) * Decimal(100)
            elif self.operation == 'absolute_difference':
                return abs(self.operand1 - self.operand2)
            else:
                raise OperationError(Fore.YELLOW +"This operation is not supported")
        except (InvalidOperation, TypeError) as e:
            logging.error(f"Error during calculation: {e}")
            raise OperationError(Fore.RED +f"Error performing {self.operation}: {e}") from e
    @staticmethod
    def _raise_division_by_zero(operand2: Decimal):
        if operand2 == 0:
            raise OperationError(Fore.RED +"You cannot divide by zero.")
    @staticmethod
    def _raise_invalid_root(x: Decimal, y: Decimal):
        if x < 0:
            raise OperationError(Fore.RED +"Cannot take the root of a negative number.")
        if y == 0:
            raise OperationError(Fore.RED +"Root cannot be zero.")

    @staticmethod
    def _raise_negative_power(x: Decimal, y: Decimal):
             if x <0:
                raise OperationError(Fore.YELLOW +"This calculator does not support negative exponents.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "operation": self.operation,
            "operand1": str(self.operand1),
            "operand2": str(self.operand2),
            "outcome": str(self.outcome),
            "timeOfCalc": self.timeOfCalc.isoformat()
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Calculation':
        try:
            output = Calculation(
                operation=data["operation"],
                operand1=Decimal(data["operand1"]),
                operand2=Decimal(data["operand2"]),
                timeOfCalc=datetime.datetime.fromisoformat(data["timeOfCalc"])
            )
        except(ValueError, ArithmeticError) as e:
            raise OperationError(Fore.RED +f"Invalid data for Calculation: {data}") from e
        saved_outcome = Decimal(data["outcome"])
        if output.outcome != saved_outcome:
            logging.warning(f"This is a mismatch: calculated {output.outcome}, saved {saved_outcome}")
        return output
    def __str__(self) -> str:
        return (f"Calculation(operation={self.operation}, "
                f"operand1={self.operand1}, operand2={self.operand2}, "
                f"outcome={self.outcome}, timeOfCalc={self.timeOfCalc})")
    def __repr__(self) -> str:
        return self.__str__()
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Calculation):
            return NotImplemented
        return (self.operation == other.operation and
                self.operand1 == other.operand1 and
                self.operand2 == other.operand2 and
                self.outcome == other.outcome and
                self.timeOfCalc == other.timeOfCalc)
    def format_result(self, precision: int) -> str:
        """
        Format the outcome of the calculation to a specified precision.
        """
        try:
            return str(self.outcome.quantize(Decimal(f"1.{'0'*precision}")))
        except (InvalidOperation, ArithmeticError) as e:
            return str(self.outcome)
    
    