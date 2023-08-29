from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm as orm
from sqlalchemy.sql import False_
from sqlalchemy.sql.lambdas import NullLambdaStatement
from pydantic import BaseModel
import pydantic as pyd
import typing

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=True, unique=True)
    # credentials_id = sa.Column(sa.Integer, sa.ForeignKey(Credentials.id), nullable=True)
    # nickname = sa.Column(sa.String(length=24), nullable=False)
    timestamp_created = sa.Column(sa.DateTime, nullable=False)
    email_verified = sa.Column(sa.Boolean, nullable=False, default=False)
    deleted = sa.Column(sa.DateTime, nullable=True, default=False)
    username = sa.Column(sa.String(length=24), nullable=False)
    password = sa.Column(sa.String(length=32), nullable=False)

# class Credentials(Base):
#     __tablename__ = "credentials_v1"
#     id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=True, unique=True)
#     # user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
#     username = sa.Column(sa.String(length=24), nullable=False)
#     email = sa.Column(sa.Text, nullable=True, unique=True)
#     password_hash = sa.Column(sa.String(length=32), nullable=False)
#     timestamp_created = sa.Column(sa.DateTime, nullable=False)


class Car_Manufacturer_Validator(BaseModel):
    id: int = 1
    name: str = "Škoda"
    description: str = "My favorite manufacturer"
    __tablename__ = "user"
# FIXME: don't default name on manufacturer and model
class Car_Manufacturer(Base):
    __tablename__ = "car_manufacturer_v2"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = sa.Column(sa.String(length=32), nullable=True)
    description = sa.Column(sa.Text, nullable=False, default = "")
    timestamp_created = sa.Column(sa.DateTime, nullable=False)

    # create_car_entry = orm.relationship("create_car_entry_v1", back_populates="manufacturer")

class Car_Model_Validator(BaseModel):
    id: int = 1
    name: str = "Octavia"
    description: str = "My favorite model"
    manufacturer: Car_Manufacturer_Validator
class Car_Model(Base):
    __tablename__ = "car_model_v1"
    id = sa.Column(sa.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = sa.Column(sa.String(length=32), nullable=False)
    car_manufacturer_id = sa.Column(sa.Integer, sa.ForeignKey(Car_Manufacturer.id))
    description = sa.Column(sa.Text, nullable=False, default="")
    timestamp_created = sa.Column(sa.DateTime, nullable=False)

class Create_Car_Entry_Validator(BaseModel):
    # model_config = pyd.ConfigDict(from_attributes=True)

    id: int = 1
    license_plate: str = "6U6 6666"
    # manufacturer: Car_Manufacturer_Validator
    model: Car_Model_Validator
    owner_id: int = 1
    description: str = ""
    vin_code: str = "dontknowwhattoputhere"
    timestamp_created: datetime

    # class Config:
        # orm_mode = True
        # arbitrary_types_allowed = True
class Create_Car_Entry(Base):
    __tablename__ = "create_car_entry_v1"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    manufacturer_id = sa.Column(sa.Integer, sa.ForeignKey(Car_Manufacturer.id))
    model_id = sa.Column(sa.Integer, sa.ForeignKey(Car_Model.id))
    owner_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    creator_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    license_plate = sa.Column(sa.String(length=12), nullable=True)
    # model = orm.relationship(Car_Model)
    description = sa.Column(sa.Text, nullable=False, default="")
    vin_code = sa.Column(sa.Text, nullable=False, default="")
    timestamp_created = sa.Column(sa.DateTime, nullable=False)

    # manufacturer: orm.Mapped[typing.List[Car_Manufacturer]] = orm.relationship(Car_Manufacturer, back_populates="create_car_entry")
    # model = orm.relationship(Car_Model)
    # owner = orm.relationship(User)
    # creator = orm.relationship(User)
    def __repr__(self):
        return "<Create_Car_Entry(id='{}', description='{}', vin_code='{}')>".format(self.id, self.description, self.vin_code)
