import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Car(Base):
    __tablename__ = "car_v1"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    description = sa.Column(sa.Text, nullable=False, default="")
    vin_code = sa.Column(sa.Text, nullable=False, default="")
class Maintenance_Event(Base):
    __tablename__ = "maintenance_event_v1"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    physical_car_id = sa.Column(sa.Integer, nullable=True, default=0)
    description = sa.Column(sa.Text, nullable=False, default="")
    maintenance_task_id = sa.Column(sa.Integer, nullable=False, default=0)
class Maintenance_Task(Base):
    __tablename__ = "maintenance_task_v1"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    description = sa.Column(sa.Text, nullable=False, default="")
    task_type_id = sa.Column(sa.Integer, nullable=False, default=0)
class Maintenance_Task_Type(Base):
    __tablename__ = "maintenance_task_type_v1"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    description = sa.Column(sa.Text, nullable=False, default="")