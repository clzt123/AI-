from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Type, Dict, Any, Optional, List
from model.student_models import (
    StudentAdminService,
    StudentPsychProfile,
    StudentPsychAlert,
    StudentFeedbackTicket,
    StudyAbroadProgress
)

MODEL_MAP = {
    'student_admin_service': StudentAdminService,
    'student_psych_profile': StudentPsychProfile,
    'student_psych_alert': StudentPsychAlert,
    'student_feedback_ticket': StudentFeedbackTicket,
    'study_abroad_progress': StudyAbroadProgress
}


class BaseDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, model: Type, data: Dict[str, Any]) -> Any:
        filtered_data = {k: v for k, v in data.items() if v is not None}
        db_obj = model(**filtered_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, model: Type, id: int, data: Dict[str, Any]) -> Optional[Any]:
        filtered_data = {k: v for k, v in data.items() if v is not None}
        if not filtered_data:
            return None
        
        result = self.db.query(model).filter(model.id == id).update(filtered_data)
        self.db.commit()
        
        if result > 0:
            return self.db.query(model).filter(model.id == id).first()
        return None

    def update_by_student_id(self, model: Type, student_id: int, data: Dict[str, Any]) -> Optional[Any]:
        filtered_data = {k: v for k, v in data.items() if v is not None}
        if not filtered_data:
            return None
        
        result = self.db.query(model).filter(model.student_id == student_id).update(filtered_data)
        self.db.commit()
        
        if result > 0:
            return self.db.query(model).filter(model.student_id == student_id).first()
        return None

    def delete(self, model: Type, id: int) -> bool:
        result = self.db.query(model).filter(model.id == id).delete()
        self.db.commit()
        return result > 0

    def get_by_id(self, model: Type, id: int) -> Optional[Any]:
        return self.db.query(model).filter(model.id == id).first()

    def execute_raw_sql(self, sql: str) -> List[Dict[str, Any]]:
        result = self.db.execute(text(sql))
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result]

    def get_model_by_table_name(self, table_name: str) -> Optional[Type]:
        return MODEL_MAP.get(table_name)