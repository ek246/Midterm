from abc import ABC, abstractmethod
from logging import config
from typing import Any
import logging

from app.calculation import Calculation


class HistoryObserver(ABC):
    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        pass #pragma: no cover
    @abstractmethod
    def notify(self, calculation: Calculation) -> None:
        pass #pragma: no cover

class LoggingObserver(HistoryObserver):
    def update(self, calculation: Calculation) -> None:
        if calculation is not None:
            logging.info(f"Calculation performed: {calculation.operation}"
                         f" with operands {calculation.operand1} and "
                         f"{calculation.operand2}. The result is {calculation.outcome}")
        else:
            raise AttributeError("There cannot be no calculation provided.")
    def notify(self, calculation: Calculation) -> None:
        self.update(calculation)

class AutoSaveObserver(HistoryObserver):
    def __init__(self, calculator: Any) -> None:
        if not hasattr(calculator, 'save_history') or not hasattr(calculator, 'config'):
            raise AttributeError("Calculator must have a 'save_history' method and 'config' attribute.")