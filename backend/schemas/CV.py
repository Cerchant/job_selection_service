import pydantic
from datetime import datetime
import uuid

class CV(pydantic.BaseModel):
    id: uuid.UUID
    title: str
    surname: str
    name: str
    patronymic: str
    date_of_birth: str
    gender: str
    city: str
    salary: str
    skills: list[str]
