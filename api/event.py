from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from service import event_service
from model.schemas import EventLectureResponse, EventRegistrationCreate, EventRegistrationResponse
from typing import List

router = APIRouter()

@router.get("/available", response_model=List[EventLectureResponse], summary="获取可报名的活动列表")
def get_available_events(db: Session = Depends(get_db)):
    return event_service.get_available_events(db)

@router.post("/register", response_model=EventRegistrationResponse, summary="活动报名")
def register_event(registration: EventRegistrationCreate, db: Session = Depends(get_db)):
    try:
        return event_service.register_event(db, registration)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"报名失败：{str(e)}")