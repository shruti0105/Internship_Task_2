from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str

class Organisation(BaseModel):
    name: str

class Permissions(BaseModel):
    user_id : str
    org_id: str
    access_level: str