from pydantic import BaseModel


class CreateUser(BaseModel):
    name: str


class UpdateUser(CreateUser):
    is_deleted: bool = False
