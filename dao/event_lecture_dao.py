from sqlalchemy.orm import Session
from model.models import EventLecture

def get_available_events(db: Session):
    return db.query(EventLecture).all()

def get_event_by_id(db: Session, event_id: int):
    return db.query(EventLecture).filter(EventLecture.id == event_id).first()

def increase_participants(db: Session, event_id: int):
    event = get_event_by_id(db, event_id)
    if event and event.current_participants < event.max_participants:
        event.current_participants += 1
        return True
    return False
