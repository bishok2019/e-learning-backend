from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class CourseBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = True
    instructor_id: Optional[int] = None


class CourseListSchema(CourseBaseSchema):
    id: int


class CourseCreateSchema(CourseBaseSchema):
    pass


class CourseUpdateSchema(CourseBaseSchema):
    pass


class CourseRetrieveSchema(CourseBaseSchema):
    id: int


class LessonBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    content: str
    order: int


class LessonListSchema(LessonBaseSchema):
    pass


class LessonRetrieveSchema(LessonBaseSchema):
    pass


class LessonUpdateSchema(LessonBaseSchema):
    pass


class LessonCreateSchema(LessonBaseSchema):
    course_id: int
