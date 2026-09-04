from pydantic import BaseModel, Field, EmailStr, ConfigDict

class AttendeeCreate(BaseModel):
    name:str=Field(min_length=2,max_length=120)
    email:str=Field(min_length=5,max_length=160)
    organization:str=''
    category:str='Student'
    age_group:str='18-25'
    source:str='Web'

class CheckInRequest(BaseModel): checked_in:bool=True
class VenueCreate(BaseModel):
    name:str=Field(min_length=2); capacity:int=Field(ge=1); venue_type:str='Conference'; location:str='Main Campus'; equipment:str='Projector,Wi-Fi'
class SpeakerCreate(BaseModel):
    name:str=Field(min_length=2); role:str='Speaker'; company:str=''; expertise:str='AI'; availability:str='Available'; rating:float=Field(default=5,ge=0,le=5)
class SessionCreate(BaseModel):
    title:str=Field(min_length=2); speaker:str; venue:str; start_time:str; end_time:str; attendees:int=Field(default=0,ge=0); status:str='Draft'
class SponsorCreate(BaseModel):
    name:str=Field(min_length=2); tier:str='Standard'; contract_value:float=Field(default=0,ge=0); amount_paid:float=Field(default=0,ge=0); leads:int=Field(default=0,ge=0); engagement_score:float=Field(default=0,ge=0,le=100)
class IncidentCreate(BaseModel):
    title:str=Field(min_length=2); category:str='Operational'; description:str=''; severity:str='Medium'; affected_people:int=Field(default=0,ge=0); owner:str='Operations Team'
class IncidentUpdate(BaseModel):
    status:str|None=None; severity:str|None=None; resolution_notes:str|None=None
class ImportAttendees(BaseModel): attendees:list[AttendeeCreate]
