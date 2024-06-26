import pydantic
import uuid

class Creds(pydantic.BaseModel):
    mail: str
    password: str


class User(pydantic.BaseModel):
    id: uuid.UUID
    mail: str
    password: str
    CVes: list[uuid.UUID]
    vacancies: list[uuid.UUID]


class UserUpdate(pydantic.BaseModel):
    auth: Creds
    mail: str
