import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm as orm
from sqlalchemy.sql import False_
from sqlalchemy.sql.lambdas import NullLambdaStatement

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=True, unique=True)
    nickname = sa.Column(sa.String(length=24), nullable=False)
    timestamp_created = sa.Column(sa.DateTime, nullable=False)
class Credentials(Base):
    __tablename__ = "credentials_v1"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=True, unique=True)
    user_id = orm.relationship(User)
    username = sa.Column(sa.String(length=24), nullable=False)
    email = sa.Column(sa.Text, nullable=True, unique=True)
    password_hash = sa.Column(sa.String(length=32), nullable=False)
    timestamp_created = sa.Column(sa.DateTime, nullable=False)
class Car_Model(Base):
    __tablename__ = "car_model_v1"
    id = sa.Column(sa.Integer, nullable=False, autoincrement=True, unique=True)
    name = sa.Column(sa.String(length=32), nullable=False)
    description = sa.Column(sa.Text, nullable=False, default = "")
    timestamp_created = sa.Column(sa.DateTime, nullable=False)
class Car_Manufacturer(Base):
    __tablename__ = "car_manufacturer_v2"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = sa.Column(sa.String(length=32), nullable=True)
    description = sa.Column(sa.Text, nullable=False, default = "")
    timestamp_created = sa.Column(sa.DateTime, nullable=False)
class Create_Car_Entry(Base):
    __tablename__ = "create_car_entry_v1"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    license_plate = sa.Column(sa.String(length=12), nullable=True)
    manufacturer = orm.relationship(Car_Manufacturer)
    model = orm.relationship(Car_Model)
    description = sa.Column(sa.Text, nullable=False, default="")
    vin_code = sa.Column(sa.Text, nullable=False, default="")
    timestamp_created = sa.Column(sa.DateTime, nullable=False)
    owner = orm.relationship(User)
    creator = orm.relationship(User)
    def __repr__(self):
        return "<Create_Car_Entry(id='{}', description='{}', vin_code='{}')>".format(self.id, self.description, self.vin_code)
