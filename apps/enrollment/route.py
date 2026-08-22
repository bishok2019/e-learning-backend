from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.authentication.models import CustomUser
from apps.course.models import Course
from apps.database import get_db
from base.pagination import get_pagination_params, paginate
from base.route import StandardResponse
from base.utils.query_utils import generic_list_handler

from .models import Enrollment
from .schemas import EnrollmentBaseSchema

router = APIRouter()


@router.post(
    "/create", response_model=StandardResponse, status_code=status.HTTP_201_CREATED
)
def create_enrollment(enrollment: EnrollmentBaseSchema, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user exists already

    if not CustomUser.id == enrollment.student_id:
        StandardResponse.error_response(
            message="Invalid Student ID",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if not Course.id == enrollment.course_id:
        StandardResponse.error_response(
            message="Invalid Course ID",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    existing_enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == enrollment.student_id,
            Enrollment.course_id == enrollment.course_id,
        )
        .first()
    )
    if existing_enrollment:
        StandardResponse.error_response(
            message="Already enrolled for this student for selected course .",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Create new user
    add_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        is_completed=enrollment.is_completed,
        completed_at=enrollment.completed_at,
    )
    db.add(add_enrollment)
    db.commit()
    db.refresh(add_enrollment)

    return StandardResponse.success_response(
        data=EnrollmentBaseSchema.model_validate(add_enrollment),
        message="User created successfully.",
    )
