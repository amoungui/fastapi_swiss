from datetime import date

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class BatteryBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    installation_date: date
    capacity: int
    charge_level: int


class BatteryCreate(BatteryBase):
    pass


class Battery(BatteryBase):
    id: int
    group_id: int

    class Config:
        from_attributes = True


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int
    is_active: bool
    batteries: list[Battery] = []

    class Config:
        from_attributes = True
