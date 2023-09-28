from datetime import date
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
import models.models as models
import schemas.schemas as schemas


def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def get_group_by_name(db: Session, name: str):
    return db.query(models.Group).filter(models.Group.name == name).first()


def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()


def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


# Modify a groupe
def update_group(db: Session, group_id: int, group: schemas.GroupCreate):
    db_group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    db_group.name = group.name
    db.commit()
    db.refresh(db_group)
    return db_group


# delete a groupe
def delete_group(db: Session, group_id: int):
    db_group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(db_group)
    db.commit()
    return db_group


# get a battery
def get_batteries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Battery).offset(skip).limit(limit).all()


def create_group_battery(db: Session, item: schemas.BatteryCreate, group_id: int):
    db_item = models.Battery(**item.dict(), group_id=group_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Modify a battery
def update_group_battery(
    db: Session, battery_id: int, item: schemas.BatteryCreate, group_id: int
):
    db_item = (
        db.query(models.Battery)
        .filter(models.Battery.id == battery_id, models.Battery.group_id == group_id)
        .first()
    )
    if db_item is None:
        raise HTTPException(status_code=404, detail="Battery not found")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


# delete a battery
def delete_group_battery(db: Session, battery_id: int, group_id: int):
    db_item = (
        db.query(models.Battery)
        .filter(models.Battery.id == battery_id, models.Battery.group_id == group_id)
        .first()
    )
    if db_item is None:
        raise HTTPException(status_code=404, detail="Battery not found")
    db.delete(db_item)
    db.commit()
    return db_item


def get_specific_battery(
    db: Session, capacity: int, charge_level: int, installation_date: date
):
    return (
        db.query(models.Battery)
        .filter(
            models.Battery.capacity == capacity,
            models.Battery.charge_level == charge_level,
            models.Battery.installation_date == installation_date,
        )
        .first()
    )
