# base/management/permissions_data.py

ALL_PERMISSION_LIST = {
    "auth_app": {
        "custom_user": [
            "create",
            "view",
            "update",
        ],
        "permission_category": [
            "view",
        ],
        "custom_permission": [
            "view",
        ],
        "roles": [
            "create",
            "view",
            "update",
        ],
    },
    "course_app": {
        "courses": [
            "create",
            "view",
            "update",
        ],
        "lessons": [
            "create",
            "view",
            "update",
        ],
    },
    "enroll_app": {
        "enrollments": [
            "create",
            "view",
            "update",
        ],
        "progress": [
            "view",
        ],
    },
    "api_logs": {
        "api_log": [
            "view",
        ],
    },
}
