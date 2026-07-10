import os
from app.contract_extractor import extract_contract_data


def test_should_extract_data_from_pdf():
    current_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(current_dir, "fixtures", "test_contract.pdf")
    
    assert os.path.exists(pdf_path), f"File not found at: {pdf_path}"
    
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
    assert result.get("old_contract_number") in ["", None]
    assert result.get("postal_code") in ["", None]
    assert result.get("city") in ["", None]
    assert result.get("street") in ["", None]
    assert result.get("phone") in ["", None]