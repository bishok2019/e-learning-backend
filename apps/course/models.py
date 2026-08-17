import enum as PyEnum  # Purpose: Define enum values

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy import Enum as SQLEnum  # Purpose: Store enum values in DB
from sqlalchemy.orm import relationship

from base.models import BaseModel


class CourseStatus(PyEnum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"
    UNDER_REVIEW = "UNDER_REVIEW"


class Course(BaseModel):
    __tablename__ = "courses"
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(CourseStatus), default=CourseStatus.DRAFT, nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    instructor = relationship("CustomUser", back_populates="courses")
    lessons = relationship(
        "Lesson",
        back_populates="course",
        cascade="all, delete-orphan",
    )
    enrollments = relationship(
        "Enrollment", back_populates="course", cascade="all, delete-orphan"
    )

    @property
    def is_published(self):
        return self.status == CourseStatus.PUBLISHED

    @property
    def total_lessons(self):
        return len(self.lessons)


class Lesson(BaseModel):
    __tablename__ = "lessons"

    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    order = Column(Integer, default=0)

    course = relationship("Course", back_populates="lessons")
    completions = relationship(
        "Progress", back_populates="lesson", cascade="all, delete-orphan"
    )
