import pytest
from unittest.mock import Mock, patch
from app.calculation import Calculation
from app.history import LoggingObserver, AutoSaveObserver
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig

# Sample setup for mock calculation
calculation_mock = Mock(spec=Calculation)
calculation_mock.operation = "multiplication"
calculation_mock.operand1 = 5
calculation_mock.operand2 = 3
calculation_mock.outcome = 15

# Test cases for LoggingObserver

def test_logging_observer_no_calculation(match = "There cannot be no calculation provided."):
    observer = LoggingObserver()
    with pytest.raises(AttributeError):
        observer.update(None)  # Passing None should raise an exception as there's no calculation

def test_autosave_observer_invalid_calculator():
    with pytest.raises(TypeError):
        AutoSaveObserver(None)  # Passing None should raise a TypeError

def test_autosave_observer_no_calculation():
    calculator_mock = Mock(spec=Calculator)
    calculator_mock.config = Mock(spec=CalculatorConfig)
    calculator_mock.config.auto_save = True
    observer = AutoSaveObserver(calculator_mock)
    
    with pytest.raises(AttributeError):
        observer.update(None)  # Passing None should raise an exception