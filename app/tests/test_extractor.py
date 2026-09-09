import os
from unittest.mock import patch
from app.contract_extractor import extract_contract_data


MOCK_AI_EXTRACTED = {
    "name": "Jan Kowalski",
    "old_contract_number": "VERT/2026/001",
    "pesel": "90010112345",
    "phone": "+48 600 700 800",
    "email": "jan.kowalski@example.com",
    "postal_code": "00-001",
    "city": "Warszawa",
    "street": "Prosta 10",
}


def test_should_extract_data_via_acroform_when_present():
    current_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(current_dir, "fixtures", "test_contract.pdf")
    
    assert os.path.exists(pdf_path), f"File not found at: {pdf_path}"
    
    with open(pdf_path, "rb") as file_stream:
        result = extract_contract_data(file_stream)
        
    assert result is not None
    assert result["pesel"] == "85031212345"
    assert "old_contract_number" in result
    assert "name" in result


@patch("app.contract_extractor._extract_from_acroform", return_value=None)
@patch("app.contract_extractor.extract_contract_data_with_ai")
def test_should_fallback_to_ai_when_acroform_missing(mock_ai, mock_acroform):
    mock_ai.return_value = MOCK_AI_EXTRACTED

    current_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(current_dir, "fixtures", "test_contract.pdf")
    
    with open(pdf_path, "rb") as file_stream:
        result = extract_contract_data(file_stream)
        
    assert result is not None
    assert result["pesel"] == "90010112345"
    assert result["name"] == "Jan Kowalski"
    mock_ai.assert_called_once()
    mock_acroform.assert_called_once()


@patch("app.contract_extractor._extract_from_acroform", return_value=None)
@patch("app.contract_extractor.extract_contract_data_with_ai")
def test_should_fallback_to_regex_when_ai_fails(mock_ai, mock_acroform):
    mock_ai.side_effect = Exception("Gemini API connection error")

    current_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(current_dir, "fixtures", "test_contract.pdf")
    
    with open(pdf_path, "rb") as file_stream:
        result = extract_contract_data(file_stream)
        
    assert result is not None
    assert "pesel" in result
    assert "old_contract_number" in result
    assert "name" in result


def test_extract_empty_document():
    current_dir = os.path.dirname(__file__)
    empty_pdf_path = os.path.join(current_dir, "fixtures", "empty_contract.pdf")
    
    assert os.path.exists(empty_pdf_path), f"File not found at: {empty_pdf_path}"

    with open(empty_pdf_path, "rb") as file_stream:
        result = extract_contract_data(file_stream)

    assert result is not None
    assert result.get("email") is None
    assert result.get("pesel") in ["", None]
    assert result.get("name") in ["", None]