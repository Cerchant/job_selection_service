import pydantic
import uuid

class vacancy(pydantic.BaseModel):
    id: uuid.UUID
    title: str
    city: str
    salary: str
    skills: list[str]
