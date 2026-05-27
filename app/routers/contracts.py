from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Contract
from app.schemas import ContractCreate
from app.contract_extractor import extract_contract_data


router = APIRouter(prefix="/contracts", tags=["Contracts"])

@router.post("/")
def create_contract(contract: ContractCreate, db: Session = Depends(get_db)):
    contract_dict = contract.model_dump()
    new_contract = Contract(**contract_dict)

    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)
    

    return new_contract


@router.post("/upload")
def upload_contract_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Przesłany plik musi być formatu PDF.")
    try:
        extracted_data = extract_contract_data(file.file)
        contract_schema = ContractCreate(**extracted_data)
        new_contract = Contract(**contract_schema.model_dump())

        db.add(new_contract)
        db.commit()
        db.refresh(new_contract)

        return new_contract
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Błąd podczas procesowania pliku PDF: {str(e)}")