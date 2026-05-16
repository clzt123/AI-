from sqlalchemy.orm import Session
from model.models import EventRegistration
from model.schemas import EventRegistrationCreate

def create_registration(db: Session, registration: EventRegistrationCreate):
    db_registration = EventRegistration(**registration.model_dump())
    db.add(db_registration)
    return db_registration
