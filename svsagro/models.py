from svsagro.database import db
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime


class TimestampMixin:
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Customer(db.Model, TimestampMixin):
    __tablename__ = "svs_customer"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)

    def __str__(self):
        return self.name


class Contact(db.Model, TimestampMixin):
    __tablename__ = "svs_contact"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)
    email = Column(String(512), nullable=False)
    customer_id = Column(Integer, ForeignKey("svs_customer.id"))
    customer = relationship("Customer")

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Machine(db.Model, TimestampMixin):
    __tablename__ = "svs_machine"

    id = Column(Integer, primary_key=True)
    number = Column(String(7), nullable=False)
    type = Column(String(10), nullable=False)
    customer_id = Column(Integer, ForeignKey("svs_customer.id"))
    customer = relationship("Customer")

    def __str__(self):
        return self.number
