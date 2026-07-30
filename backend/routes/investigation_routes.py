from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database.dependency import get_db

from services.investigation_service import InvestigationService


router = APIRouter(
    prefix="/api/investigations",
    tags=["Investigations"]
)



@router.post("/")
def create_investigation(
    contract_id: int,
    goal: str = "Investigate SLA breach",
    db: Session = Depends(get_db)
):

    service = InvestigationService(
        db
    )


    report = service.investigate(
        contract_id=contract_id,
        goal=goal
    )


    return report