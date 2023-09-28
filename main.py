from datetime import date
from fastapi import FastAPI, Header, status, Depends, HTTPException
from pydantic import BaseModel
from controllers.controller import (
    create_group,
    create_group_battery,
    delete_group,
    delete_group_battery,
    get_batteries,
    get_group,
    get_group_by_name,
    get_groups,
    get_specific_battery,
    update_group,
    update_group_battery,
)
import models.models as models
from config.database import Base, engine
from typing import Annotated
from sqlalchemy.orm import Session
import auths.auth as auth
from auths.auth import get_current_user, get_db, oauth2_bearer
from schemas.schemas import Battery, BatteryCreate, Group, GroupCreate

app = FastAPI()

app.include_router(auth.router)

Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/user/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failled")
    return {"User": user}


# crud for groupes
@app.post("/groups/", response_model=Group)
async def create_a_group(group: GroupCreate, user: user_dependency, db: db_dependency):
    db_group = get_group_by_name(db, name=group.name)
    if db_group:
        raise HTTPException(status_code=400, detail="name already registered")
    return create_group(db=db, group=group)


@app.get("/groups/", response_model=list[Group])
async def read_all_groups(
    db: db_dependency, user: user_dependency, skip: int = 0, limit: int = 100
):
    groups = get_groups(db, skip=skip, limit=limit)
    return groups


@app.get("/groups/{group_id}", response_model=Group)
async def read_a_group(group_id: int, user: user_dependency, db: db_dependency):
    db_group = get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group


@app.put("/groups/{group_id}", response_model=Group)
async def update_a_group(
    group_id: int, group: GroupCreate, user: user_dependency, db: db_dependency
):
    db_group = update_group(db, group_id=group_id, group=group)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group


@app.delete("/groups/{group_id}", response_model=Group)
async def delete_a_group(group_id: int, user: user_dependency, db: db_dependency):
    del_group = delete_group(db, group_id)
    return del_group


# crud for batteries
@app.post("/groups/{group_id}/batteries/", response_model=Battery)
async def create_battery_for_group(
    group_id: int, item: BatteryCreate, user: user_dependency, db: db_dependency
):
    return create_group_battery(db=db, item=item, group_id=group_id)


@app.get("/batteries/", response_model=list[Battery])
async def read_batteries(
    db: db_dependency, user: user_dependency, skip: int = 0, limit: int = 100
):
    items = get_batteries(db, skip=skip, limit=limit)
    return items


@app.put("/groups/{group_id}/batteries/{battery_id}", response_model=Battery)
async def update_battery(
    battery_id: int,
    group_id: int,
    item: BatteryCreate,
    user: user_dependency,
    db: db_dependency,
):
    return update_group_battery(db, battery_id, item, group_id)


@app.delete("/groups/{group_id}/batteries/{battery_id}", response_model=Battery)
async def delete_battery(
    battery_id: int,
    group_id: int,
    user: user_dependency,
    db: db_dependency,
):
    return delete_group_battery(db, battery_id, group_id)


@app.get(
    "/batteries/{capacity}/{installation_date}/{charge_level}", response_model=Battery
)
async def find_specific_battery(
    capacity: int,
    charge_level: int,
    installation_date: date,
    user: user_dependency,
    db: db_dependency,
):
    battery = get_specific_battery(db, capacity, charge_level, installation_date)
    if battery is None:
        raise HTTPException(status_code=404, detail="Battery not found")
    return battery
