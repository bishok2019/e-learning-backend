from .course import (
    CourseBaseSchema,
    CourseCreateSchema,
    CourseListSchema,
    CourseRetrieveSchema,
    CourseUpdateSchema,
)
from .lessons import (
    LessonBaseSchema,
    LessonCreateSchema,
    LessonListSchema,
    LessonRetrieveSchema,
    LessonUpdateSchema,
)

__all__ = [
    # courses
    "CourseBaseSchema",
    "CourseCreateSchema",
    "CourseListSchema",
    "CourseRetrieveSchema",
    "CourseUpdateSchema",
    # lessons
    "LessonBaseSchema",
    "LessonCreateSchema",
    "LessonListSchema",
    "LessonRetrieveSchema",
    "LessonUpdateSchema",
]
