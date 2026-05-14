from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from dao.student_dao import BaseDAO
from model.student_models import (
    StudentAdminService,
    StudentPsychProfile,
    StudentPsychAlert,
    StudentFeedbackTicket,
    StudyAbroadProgress
)


class BaseService:
    def __init__(self, db: Session):
        self.dao = BaseDAO(db)

    def create(self, table_name: str, data: Dict[str, Any]) -> Optional[Any]:
        model = self.dao.get_model_by_table_name(table_name)
        if not model:
            return None
        return self.dao.create(model, data)

    def update(self, table_name: str, id: int, data: Dict[str, Any]) -> Optional[Any]:
        model = self.dao.get_model_by_table_name(table_name)
        if not model:
            return None
        return self.dao.update(model, id, data)

    def update_by_student_id(self, table_name: str, student_id: int, data: Dict[str, Any]) -> Optional[Any]:
        model = self.dao.get_model_by_table_name(table_name)
        if not model:
            return None
        return self.dao.update_by_student_id(model, student_id, data)

    def delete(self, table_name: str, id: int) -> bool:
        model = self.dao.get_model_by_table_name(table_name)
        if not model:
            return False
        return self.dao.delete(model, id)

    def get_by_id(self, table_name: str, id: int) -> Optional[Any]:
        model = self.dao.get_model_by_table_name(table_name)
        if not model:
            return None
        return self.dao.get_by_id(model, id)

    def execute_raw_sql(self, sql: str) -> List[Dict[str, Any]]:
        return self.dao.execute_raw_sql(sql)