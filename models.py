from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, UniqueConstraint
from database import Base

class Attendee(Base):
    __tablename__='attendees'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,index=True)
    organization=Column(String,default='')
    category=Column(String,default='Student')
    age_group=Column(String,default='18-25')
    source=Column(String,default='Web')
    status=Column(String,default='Registered')
    checked_in=Column(Integer,default=0)
    created_at=Column(DateTime,default=datetime.utcnow)
    checked_in_at=Column(DateTime,nullable=True)
    __table_args__=(UniqueConstraint('email',name='uq_attendee_email'),)

class Venue(Base):
    __tablename__='venues'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    capacity=Column(Integer,nullable=False)
    venue_type=Column(String,default='Conference')
    location=Column(String,default='Main Campus')
    equipment=Column(String,default='Projector,Wi-Fi')
    status=Column(String,default='Available')
    utilization=Column(Integer,default=0)

class Speaker(Base):
    __tablename__='speakers'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    role=Column(String,default='Speaker')
    company=Column(String,default='')
    expertise=Column(String,default='AI')
    availability=Column(String,default='Available')
    sessions=Column(Integer,default=0)
    rating=Column(Float,default=5.0)

class Session(Base):
    __tablename__='sessions'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    speaker=Column(String,nullable=False)
    venue=Column(String,nullable=False)
    start_time=Column(String,nullable=False)
    end_time=Column(String,nullable=False)
    attendees=Column(Integer,default=0)
    status=Column(String,default='Draft')

class Sponsor(Base):
    __tablename__='sponsors'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    tier=Column(String,default='Standard')
    contract_value=Column(Float,default=0)
    amount_paid=Column(Float,default=0)
    leads=Column(Integer,default=0)
    engagement_score=Column(Float,default=0)
    status=Column(String,default='Active')
    created_at=Column(DateTime,default=datetime.utcnow)

class Incident(Base):
    __tablename__='incidents'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    category=Column(String,default='Operational')
    description=Column(Text,default='')
    severity=Column(String,default='Medium')
    priority=Column(String,default='Medium')
    status=Column(String,default='Open')
    affected_people=Column(Integer,default=0)
    owner=Column(String,default='Operations Team')
    escalation_level=Column(Integer,default=0)
    resolution_notes=Column(Text,default='')
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

class Alert(Base):
    __tablename__='alerts'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    message=Column(Text,nullable=False)
    level=Column(String,default='INFO')
    source=Column(String,default='System')
    resolved=Column(Integer,default=0)
    created_at=Column(DateTime,default=datetime.utcnow)
