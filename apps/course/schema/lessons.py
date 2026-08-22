from typing import Optional

from pydantic import BaseModel, ConfigDict


class LessonBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    content: str
    order: int


class LessonListSchema(LessonBaseSchema):
    pass


class LessonRetrieveSchema(LessonBaseSchema):
    id: int
    pass


class LessonUpdateSchema(LessonBaseSchema):
    pass


class LessonCreateSchema(LessonBaseSchema):
    course_id: Optional[int] = None
