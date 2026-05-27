import os
from app.contract_extractor import extract_contract_data


def test_should_extract_data_from_pdf():
    current_dir = os.path.dirname(__file__)

    pdf_path = os.path.join(current_dir, "fixtures", "test_contract.pdf")
    
    assert os.path.exists(pdf_path), f"Brak pliku w lokacji: {pdf_path}"
    
    with open(pdf_path, "rb") as file_stream:
        result = extract_contract_data(file_stream)
        
        print(result)

    print("\nWynik parsera:", result)
    assert result is not None