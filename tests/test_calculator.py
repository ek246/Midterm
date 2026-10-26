import datetime
import logging
from pathlib import Path
import pandas as pd
import pytest 
from unittest.mock import Mock, patch, PropertyMock
from decimal import Decimal
from tempfile import TemporaryDirectory
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver
from app.operations import OperationFactory

@pytest.fixture
def calculator():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir = temp_path)
        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
             patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file, \
             patch.object(CalculatorConfig, 'history_dir', new_callable=PropertyMock) as mock_history_dir, \
             patch.object(CalculatorConfig, 'history_file', new_callable=PropertyMock) as mock_history_file:

         mock_log_dir.return_value = temp_path / "logs"
         mock_log_file.return_value = temp_path / "logs" / "calculator.log"
         mock_history_dir.return_value = temp_path / "history"
         mock_history_file.return_value = temp_path / "history" / "history.csv"
         yield Calculator(config=config)
def test_calculator_initialization(calculator):
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.operation_strategy is None

@patch('app.calculator.logging.info')
def test_logging_setup(logging_info_mock):
    with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
         patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file:
        mock_log_dir.return_value = Path('/tmp/logs')
        mock_log_file.return_value = Path('/tmp/logs/calculator.log')

        calculator = Calculator(CalculatorConfig())
        logging_info_mock.assert_any_call("Initialization complete.")

def test_add_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    assert observer in calculator.observers

def test_remove_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    calculator.remove_observer(observer)
    assert observer not in calculator.observers

def test_set_operation(calculator):
    operation = OperationFactory.create_operation("subtraction")
    calculator.set_operation(operation)
    assert calculator.operation_strategy == operation

def test_perform_operation_addition(calculator):
    operation = OperationFactory.create_operation("addition")
    calculator.set_operation(operation)
    result = calculator.perform_operation(5, 3)
    assert result == 8

def test_perform_operation_validation_error(calculator):
        calculator.set_operation(OperationFactory.create_operation("division"))
        with pytest.raises(ValidationError):
            calculator.perform_operation(5, "invalid")

def test_perform_operation_operation_error(calculator):
        with pytest.raises(OperationError, match = "No operation is set"):
             calculator.perform_operation(3, 3)

def test_history_greater_than_max(monkeypatch):
    config = CalculatorConfig()
    config.max_history = 2
    assert config.max_history == 2

    calculator = Calculator(config=config)
    operation_test = OperationFactory.create_operation("subtraction")
    calculator.set_operation(operation_test)

    calculator.perform_operation(1, 1)
    calculator.perform_operation(2, 1)
    calculator.perform_operation(3, 1)

    assert len(calculator.history) == 2
    assert calculator.history[0].operand1 == 2
    assert calculator.history[1].operand1 == 3

def test_undo(calculator):
     operation = OperationFactory.create_operation("addition")
     calculator.set_operation(operation)
     result = calculator.perform_operation(5, 3)
     assert result == 8
     calculator.undo()
     assert calculator.history == []

def test_undo_restores_older_history(calculator):
        calculator.set_operation(OperationFactory.create_operation("multiplication"))
        calculator.perform_operation(2, 3)
        calculator.set_operation(OperationFactory.create_operation("addition"))
        calculator.perform_operation(2, 3)
        assert len(calculator.history) == 2
        assert calculator.undo() is True
        assert len(calculator.history) == 1
        assert calculator.history[0].operation == "multiplication"
        assert calculator.history[0].outcome == 6

def test_redo_recreates_history(calculator):
    calculator.set_operation(OperationFactory.create_operation("multiplication"))
    calculator.perform_operation(2, 3)
    calculator.set_operation(OperationFactory.create_operation("addition"))
    calculator.perform_operation(2, 3)
    calculator.undo() 
    assert len(calculator.history) == 1
    assert calculator.redo() is True
    assert calculator.history[0].operation == "multiplication"
    assert calculator.history[1].operation == "addition"
    assert calculator.history[1].outcome == 5
def test_new_operation_empties_redo_stack(calculator):
    calculator.set_operation(OperationFactory.create_operation("addition"))
    calculator.perform_operation(3, 3)
    calculator.undo()
    assert calculator.redo_stack
    calculator.set_operation(OperationFactory.create_operation("division"))
    calculator.perform_operation(4, 2)
    assert calculator.redo_stack == []
    assert calculator.redo() is False
def test_redo(calculator):
     operation = OperationFactory.create_operation("addition")
     calculator.set_operation(operation)
     result = calculator.perform_operation(5, 3)
     assert result == 8
     calculator.undo()
     assert calculator.history == []
     calculator.redo()
     assert len(calculator.history) == 1
     assert calculator.history[0].operation == "addition"
     assert calculator.history[0].operand1 == 5
     assert calculator.history[0].operand2 == 3
     assert calculator.history[0].outcome == 8
@patch('app.calculator.pd.DataFrame.to_csv')
def test_save_history(mock_to_csv, calculator):
     operation = OperationFactory.create_operation("addition")
     calculator.set_operation(operation)
     calculator.perform_operation(4, 5)
     calculator.save_history()
     mock_to_csv.assert_called_once()

@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history(mock_exists, mock_read_csv, calculator):
    mock_read_csv.return_value = pd.DataFrame({
         'operation': ['subtraction'],
        'operand1': ['3'],
        'operand2': ['2'],
        'outcome': ['1'],
        'timestamp': [datetime.datetime.now().isoformat()]
    })
    try:
         calculator.load_history()
         assert len(calculator.history) == 1
         assert calculator.history[0].operation == "subtraction"
         assert calculator.history[0].operand1 == 3
         assert calculator.history[0].operand2 == 2
         assert calculator.history[0].outcome == 1
    except OperationError as e:
         pytest.fail(f"Loading history failed: {e}")

def test_calculator_load_history_error(calculator, caplog):
    calculator.config.history_file.parent.mkdir(
        parents=True, exist_ok=True
    )
    calculator.config.history_file.touch()

    with patch(
        "app.calculator.pd.read_csv",
        side_effect=Exception("Load failed")
    ):
        with caplog.at_level(logging.WARNING):
            calculator.load_history()

    assert "Failed to load history" in caplog.text
    assert "Load failed" in caplog.text
def test_clear_history(calculator):
     operation = OperationFactory.create_operation("addition")
     calculator.set_operation(operation)
     calculator.perform_operation(4, 5)
     calculator.clear_history()
     assert calculator.history == []
     assert calculator.undo_stack == []
     assert calculator.redo_stack == []

def test_logging_initialization_failure():
     with patch('app.calculator.logging.basicConfig') as mock_basicConfig, \
          patch('app.calculator.logging.error') as mock_logging_error:
         mock_basicConfig.side_effect = Exception("Initialization failed")
         Calculator(CalculatorConfig())
         mock_logging_error.assert_called_once()
def test_cannot_find_observer():
     with patch('app.calculator.logging.warning') as mock_logging_warning:
        calculator = Calculator(CalculatorConfig())
        class TestObserver:
            pass
        lost_observer = TestObserver()
        calculator.remove_observer(lost_observer)

        mock_logging_warning.assert_called_once_with (
        "Observer not found: TestObserver"
    )

def test_self_history_removal(calculator):
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path, max_history=2)
        calculator = Calculator(config)

        operation = OperationFactory.create_operation("addition")
        calculator.set_operation(operation)
        calculator.perform_operation(4, 5)
        calculator.perform_operation(6, 7)
        assert len(calculator.history) == 2
        assert calculator.history[0].operand1 == 4
        assert calculator.history[0].operand2 == 5
def test_failed_operation(calculator):
    operation = OperationFactory.create_operation("division")
    calculator.set_operation(operation)
    with pytest.raises(OperationError):
        calculator.perform_operation(4, 0)

def test_save_history_error(calculator):
    calculator.clear_history()
    with patch(
        "app.calculator.pd.DataFrame.to_csv", side_effect=Exception("Save failed")
    ):
        with pytest.raises(OperationError, match="Could not save history: Save failed"):
            calculator.save_history()

    
def test_load_history_dataframe(calculator):
    calculator.clear_history()
    operation = OperationFactory.create_operation("addition")
    calculator.set_operation(operation)
    calculator.perform_operation(4, 5)
    df = calculator.load_history_dataframe()
    assert not df.empty
    assert list(df.columns) == ["operation", "operand1", "operand2", "outcome", "timestamp"]
    assert df.iloc[0]["operation"] == "addition"
    assert df.iloc[0]["operand1"] == "4"
    assert df.iloc[0]["operand2"] == "5"
    assert df.iloc[0]["outcome"] == "9"
    assert df.iloc[0]["timestamp"] is not None
def test_load_history_file_does_not_exist(calculator):
    if calculator.config.history_file.exists():
        calculator.config.history_file.unlink()
    calculator.load_history()
    assert calculator.history == []
    
def test_load_history_dataframe_empty(calculator):
    calculator.clear_history()
    df = calculator.load_history_dataframe()
    assert len(df) == 0

def test_no_config():
        calculator = Calculator()
        assert isinstance(calculator.config, CalculatorConfig)
    
