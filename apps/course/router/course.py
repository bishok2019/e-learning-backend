from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.authentication.models import CustomUser
from apps.authentication.utils import hash_password
from apps.database import get_db
from base.pagination import get_pagination_params
from base.route import StandardResponse
from base.utils.query_utils import generic_list_handler

from .. import schemas
from ..models import Course

router = APIRouter()


@router.get("/list", response_model=StandardResponse)
def get_courses(
    search: str = "",
    instructor_id: int = None,
    status: str = None,
    db: Session = Depends(get_db),
    pagination=Depends(get_pagination_params),
):
    """Get all courses with pagination"""
    result = generic_list_handler(
        search_fields=["title"],
        filter_fields=["instructor_id", "status"],
        model=Course,
        schema=schemas.CourseListSchema,
        pagination=pagination,
        status=status,
        instructor_id=instructor_id,
        db=db,
    )
    return StandardResponse.success_response(
        data=result.data,
        message="Courses fetched successfully.",
        meta=result.meta,
    )


@router.post(
    "/create", response_model=StandardResponse, status_code=status.HTTP_201_CREATED
)
def create_course(
    course: schemas.CourseCreateSchema,
    db: Session = Depends(get_db),
):
    """Create a new course"""
    existing_course = db.query(Course).filter(Course.title == course.title).first()
    if existing_course:
        return StandardResponse.error_response(
            message="Course with this title already exists.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    valid_instructor = (
        db.query(CustomUser)
        .filter(
            CustomUser.user_type == "TEACHER",
            CustomUser.id == course.instructor_id,
        )
        .first()
    )
    if not valid_instructor:
        return StandardResponse.error_response(
            message="Instructor user_type must be TEACHER",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    db_course = Course(
        title=course.title,
        description=course.description,
        status=course.status,
        is_active=course.is_active,
        instructor_id=course.instructor_id,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return StandardResponse.success_response(
        data=schemas.CourseRetrieveSchema.model_validate(db_course),
        message="Course created successfully.",
    )


@router.get("/retrieve/{course_id}", response_model=StandardResponse)
def retrieve_course(
    course_id: int,
    db: Session = Depends(get_db),
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        StandardResponse.error_response(
            message="Course not Found.", status_code=status.HTTP_404_NOT_FOUND
        )
    return StandardResponse.success_response(
        data=schemas.CourseRetrieveSchema.model_validate(course),
        message="Course retrieved successfully.",
    )
