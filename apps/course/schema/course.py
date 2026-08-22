from typing import Optional

from pydantic import BaseModel, ConfigDict

from .lessons import LessonCreateSchema, LessonRetrieveSchema


class CourseBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    description: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = True
    instructor_id: Optional[int] = None


class CourseListSchema(CourseBaseSchema):
    title: str
    id: int


class CourseRetrieveSchema(CourseBaseSchema):
    id: int
    lessons: list[LessonRetrieveSchema] = []


class CourseCreateSchema(CourseBaseSchema):
    title: str
    lessons: Optional[list[LessonCreateSchema]] = []


class CourseUpdateSchema(CourseBaseSchema):
    title: Optional[str] = None
