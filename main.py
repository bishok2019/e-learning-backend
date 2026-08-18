from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from apps import model_registry
from apps.authentication.router import auth_router, user_router
from apps.course.router import course_router, lesson_router
from base.exceptions import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)

app = FastAPI(
    title="E-Learning FastAPI Project",
    # description="Title",
    version="1.0.0",
    contact={
        "name": "Bishok Paudel",
        "email": "bishokpaudel57@gmail.com",
    },
)
# app.add_middleware(APILoggingMiddleware)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "*"],  # your React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="staticfiles"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
v1_router.include_router(user_router, prefix="/users", tags=["Users"])
v1_router.include_router(course_router, prefix="/courses", tags=["Courses"])
v1_router.include_router(lesson_router, prefix="/lesson", tags=["Lesson"])


app.include_router(v1_router)
