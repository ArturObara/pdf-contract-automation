from pydantic import BaseModel, Field

class ContractCreate(BaseModel):
    
    name: str = Field(min_length=1)
    old_contract_number: str = Field(min_length=1)
    phone: str = Field(min_length=1)
    email: str | None = None
    postal_code: str = Field(min_length=1)
    city: str = Field(min_length=1)
    street: str = Field(min_length=1)

class UpsellRequest(BaseModel):

    old_contract_number: str = Field(min_length=1, description="Numer starej umowy, po którym szukamy klienta w bazie")