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
    # role_id = 1 - обычный пользователь
    # role_id = 2 - администратор
    role_id: int


class UserUpdate(pydantic.BaseModel):
    auth: Creds
    mail: str
