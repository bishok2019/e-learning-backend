from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class EnrollmentBaseSchema(BaseModel):
    student_id: int
    course_id: int
    is_completed: bool
    completed_at: datetime | None = None
