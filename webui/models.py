import sqlalchemy as sa

Base = sa.ext.declarative.declarative_base()
class Physical_Car(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    description = sa.Column(sa.Text, nullable=False, default="")
class Maintenance_Event(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    physical_car_id = sa.Column(sa.Integer, nullable=False, default=0)
    description = sa.Column(sa.Text, nullable=False, default="")
    maintenance_task_id = sa.Column(sa.Integer, nullable=False, default=0)
class Maintenance_Task(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    description = sa.Column(sa.Text, nullable=False, default="")
    task_type_id = sa.Column(sa.Integer, nullable=False, default=0)
class Maintenance_Task_Type(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    description = sa.Column(sa.Text, nullable=False, default="")
class Car_Papers(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    description = sa.Column(sa.Text, nullable=False, default="")