from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Contract
from app.schemas import ContractCreate


router = APIRouter(prefix="/contracts", tags=["Contracts"])

@router.post("/")
def create_contract(contract: ContractCreate, db: Session = Depends(get_db)):
    contract_dict = contract.model_dump()
    new_contract = Contract(**contract_dict)

    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)


    return new_contract