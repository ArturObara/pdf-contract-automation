from pydantic import BaseModel, Field, EmailStr, ValidationError, ConfigDict
from contract_extractor import extract_contract_data

class ContractCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2)
    old_contract_number: str = Field(min_length=1)
    pesel: str = Field(pattern=r"^\d{10,11}$", description="Dokładnie 10 (NIP) lub 11 (PESEL) cyfr")
    phone: str = Field(pattern=r"^[+\d][\d\s\-]{6,}$")
    email: EmailStr | None = None
    postal_code: str = Field(pattern=r"^\d{2}-\d{3}$")
    city: str = Field(min_length=2)
    street: str = Field(min_length=2)

class UpsellRequest(BaseModel):
    old_contract_number: str = Field(
        min_length=1, 
        description="The original contract number used to locate the client in the database"
    )

def handle_uploaded_contract(file_stream):
    try:
        raw_data = extract_contract_data(file_stream)
    except Exception as e:
        return {
            "status": "error", 
            "message": "Błąd odczytu pliku PDF. Plik może być uszkodzony, zaszyfrowany lub nie jest to dokument tekstowy.", 
            "details": str(e)
        }

    try:
        contract = ContractCreate(**raw_data)
        return {"status": "success", "data": contract.model_dump()}
        
    except ValidationError as e:
        return {
            "status": "error", 
            "message": "Błąd walidacji. PDF nie zawiera wszystkich wymaganych danych lub mają one nieprawidłowy format.", 
            "details": e.errors()
        }