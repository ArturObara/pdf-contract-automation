from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from app.database import get_db
from app.models import Contract
from app.schemas import ContractCreate, UpsellRequest
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
    

template_env = Environment(loader=FileSystemLoader("app/templates"))


@router.post("/generate-upsell")
def generate_upsell(request: UpsellRequest, db: Session = Depends(get_db)):
    
    client_contract = db.query(Contract).filter(Contract.old_contract_number == request.old_contract_number).first()
    
    if not client_contract:
        raise HTTPException(status_code=404, detail="Brak starej umowy w bazie danych!")
    
    client_data = {
        "name": client_contract.name,
        "street": client_contract.street,
        "postal_code": client_contract.postal_code,
        "city": client_contract.city,
        "phone": client_contract.phone,
        "email": client_contract.email,
        "old_contract_number": client_contract.old_contract_number
    }
    
    template = template_env.get_template("upsell_contract_template.html")
    rendered_html = template.render(**client_data)
    
    safe_contract_number = request.old_contract_number.replace("/", "_")
    file_name = f"Umowa_Upsell_{safe_contract_number}.pdf"
    
    HTML(string=rendered_html).write_pdf(file_name)
    
    return FileResponse(
        path=file_name,
        filename=file_name,
        media_type="application/pdf"
    )