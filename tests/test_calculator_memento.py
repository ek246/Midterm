import pytest
from app.calculator_memento import Memento
from decimal import Decimal
from app.calculation import Calculation
def test_to_dict():
    calc = Calculation(operation="multiplication", operand1=2, operand2=3)

    momento = Memento(calcHistory=[calc])
    result = momento.to_dict()
    import inspect

    print(inspect.getfile(Memento))
    print(inspect.getsource(Memento.to_dict))
    assert result["calcHistory"] == [calc.to_dict()]
    assert "calcTime" in result
    assert isinstance(result["calcTime"], str)
    assert result["calcTime"] == momento.timestamp.isoformat()
def test_from_dict():
    calc = Calculation(operation="addition", operand1=5, operand2=7)
    momento = Memento(calcHistory=[calc])
    data = momento.to_dict()
    new_momento = Memento.from_dict(data)
    assert new_momento.calcHistory[0].operation == "addition"
    assert new_momento.calcHistory[0].operand1 == 5
    assert new_momento.calcHistory[0].operand2 == 7
    assert new_momento.timestamp == momento.timestamp