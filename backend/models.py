from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    bookings = relationship("Booking", back_populates="user")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    providers = relationship("Provider", back_populates="service")


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rating = Column(Float, nullable=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    service = relationship("Service", back_populates="providers")
    bookings = relationship("Booking", back_populates="provider")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    status = Column(String, default="pending")
    user = relationship("User", back_populates="bookings")
    provider = relationship("Provider", back_populates="bookings")
