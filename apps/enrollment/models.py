from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from base.models import BaseModel


class Enrollment(BaseModel):
    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uq_student_course"),
    )

    student_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    is_completed = Column(Boolean, default=False, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    student = relationship("CustomUser", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    completed_lessons = relationship(
        "Progress", back_populates="enrollment", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"{self.student.full_name} - {self.course.title}"

    @property
    def total_lessons(self):
        return self.course.total_lessons

    @property
    def completed_lessons_count(self):
        return len(self.completed_lessons)

    @property
    def completion_percentage(self):
        total = self.total_lessons
        if total == 0:
            return 0
        return round((self.completed_lessons_count / total) * 100, 2)


class Progress(BaseModel):
    __tablename__ = "lesson_completions"
    __table_args__ = (
        UniqueConstraint("enrollment_id", "lesson_id", name="uq_enrollment_lesson"),
    )

    enrollment_id = Column(
        Integer, ForeignKey("enrollments.id", ondelete="CASCADE"), nullable=False
    )
    lesson_id = Column(
        Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False
    )

    enrollment = relationship("Enrollment", back_populates="completed_lessons")
    lesson = relationship("Lesson", back_populates="completions")

    def __str__(self):
        return f"{self.enrollment.student.full_name} - {self.lesson.title}"
