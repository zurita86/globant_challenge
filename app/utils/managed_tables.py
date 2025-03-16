from enum import Enum


class TableEnum(str, Enum):
    DEPARTMENTS = "departments"
    JOBS = "jobs"
    EMPLOYEES = "hired_employees"
