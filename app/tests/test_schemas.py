import pytest
from pydantic import ValidationError
from app.schemas import ContractCreate

VALID_DATA = {
    "name": "Jan Kowalski",
    "old_contract_number": "S/1",
    "pesel": "85031212345",
    "phone": "+48111222333",
    "postal_code": "04-350",
    "city": "Warszawa",
    "street": "Nowy Świat 1"
}

def test_schema_accepts_valid_data():
    contract = ContractCreate(**VALID_DATA)
    assert contract.name == "Jan Kowalski"

@pytest.mark.parametrize("field, bad_value", [
    ("pesel", "12345"),
    ("pesel", "abcdefghijk"),
    ("postal_code", "32350"),
    ("phone", "123"),
    ("name", "A"),
])
def test_schema_rejects_invalid_data(field, bad_value):
    invalid_data = {**VALID_DATA, field: bad_value}
    
    with pytest.raises(ValidationError):
        ContractCreate(**invalid_data)