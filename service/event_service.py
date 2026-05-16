from sqlalchemy.orm import Session
from dao import event_lecture_dao, event_registration_dao
from model.schemas import EventLectureResponse, EventRegistrationCreate, EventRegistrationResponse
from fastapi import HTTPException

def get_available_events(db: Session):
    events = event_lecture_dao.get_available_events(db)
    return [EventLectureResponse.model_validate(event) for event in events]

def register_event(db: Session, registration: EventRegistrationCreate):
    event = event_lecture_dao.get_event_by_id(db, registration.event_id)
    if not event:
        raise HTTPException(status_code=404, detail="活动不存在")
    if event.current_participants >= event.max_participants:
        raise HTTPException(status_code=400, detail="活动名额已满")

    event_lecture_dao.increase_participants(db, registration.event_id)
    db_registration = event_registration_dao.create_registration(db, registration)
    db.commit()
    db.refresh(db_registration)
    return EventRegistrationResponse.model_validate(db_registration)
