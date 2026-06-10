from sqlalchemy import Column, Integer, String, DateTime
from database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    provider_id = Column(Integer, nullable=False, index=True)
    scheduled_at = Column(DateTime, nullable=False)
    status = Column(String, default="pending", nullable=False)
