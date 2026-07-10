from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import ValidationError

from app.database import get_db
from app.models import Contract
from app.schemas import ContractCreate, UpsellRequest
from app.contract_extractor import extract_contract_data
from app.contract_generator import generate_upsell_pdf

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
        raise HTTPException(status_code=400, detail="Uploaded file must be a PDF.")
    
    try:
        extracted_data = extract_contract_data(file.file)
        contract_schema = ContractCreate(**extracted_data)
        
        new_contract = Contract(**contract_schema.model_dump())
        db.add(new_contract)
        db.commit()
        db.refresh(new_contract)

        return new_contract
        
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Critical error processing PDF file: {str(e)}")

@router.post("/generate-upsell")
def generate_upsell(request: UpsellRequest, db: Session = Depends(get_db)):
    # NOWOCZESNE ZAPYTANIE SQLALCHEMY 2.0
    stmt = select(Contract).where(Contract.old_contract_number == request.old_contract_number)
    client_contract = db.execute(stmt).scalars().first()
    
    if not client_contract:
        raise HTTPException(status_code=404, detail="Old contract not found in the database.")

    client_data = {
        "name": client_contract.name,
        "street": client_contract.street,
        "postal_code": client_contract.postal_code,
        "city": client_contract.city,
        "pesel": client_contract.pesel,
        "phone": client_contract.phone,
        "email": client_contract.email,
        "old_contract_number": client_contract.old_contract_number
    }
    
    pdf_bytes = generate_upsell_pdf(client_data)
    
    safe_contract_number = request.old_contract_number.replace("/", "_")
    file_name = f"Umowa_Upsell_{safe_contract_number}.pdf"
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'}
    )