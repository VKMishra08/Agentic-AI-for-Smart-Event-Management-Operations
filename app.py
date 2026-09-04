import os
from datetime import datetime
from fastapi import FastAPI,Depends,HTTPException,Query,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import Base,engine,get_db
from models import Attendee,Venue,Speaker,Session as EventSession,Sponsor,Incident,Alert
from schemas import AttendeeCreate,CheckInRequest,VenueCreate,SpeakerCreate,SessionCreate,SponsorCreate,IncidentCreate,IncidentUpdate,ImportAttendees
from registration_agent import analyze_attendees
from venue_agent import recommend_venues
from speaker_agent import find_speakers
from agents import sponsorship_agent,incident_agent
from workflows import execute_incident_workflow
from intelligence import build_intelligence
from orchestrator import run_orchestration
from auth import require_read, require_write
from logging_config import configure_logging
from monitoring import record_request, metrics
import logging, time, uuid
from backup import backup

configure_logging()
logger = logging.getLogger('eventops.api')

Base.metadata.create_all(bind=engine)
app=FastAPI(title='Event Intelligence & Enterprise Platform',version='4.0.0',description='Integrated AI-powered event operations and decision-support platform with enterprise deployment controls', dependencies=[Depends(require_read)])
origins=[x.strip() for x in os.getenv('CORS_ORIGINS','http://localhost:5173,http://localhost:5178').split(',') if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])

@app.middleware('http')
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Cache-Control'] = 'no-store' if request.url.path.startswith('/api/') else 'no-cache'
    return response

@app.exception_handler(Exception)
async def unhandled_exception(request: Request, exc: Exception):
    logger.exception('Unhandled application exception')
    return JSONResponse(status_code=500, content={'success':False,'error':'Internal server error','request_id':request.headers.get('X-Request-ID')})

@app.middleware('http')
async def observability_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    started = time.perf_counter()
    try:
        response = await call_next(request)
        record_request(time.perf_counter() - started, response.status_code)
        response.headers['X-Request-ID'] = request_id
        return response
    except Exception:
        record_request(time.perf_counter() - started, 500)
        logger.exception('Unhandled request error', extra={'request_id': request_id})
        raise
    finally:
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        logger.info('%s %s %s %sms', request.method, request.url.path, request_id, duration_ms, extra={'request_id': request_id})

def serialize(obj):
    out={c.name:getattr(obj,c.name) for c in obj.__table__.columns}
    return {k:(v.isoformat() if isinstance(v,datetime) else v) for k,v in out.items()}

def models(): return (Attendee,Venue,Speaker,EventSession,Sponsor,Incident,Alert)

@app.get('/')
def root(): return {'success':True,'message':'Event Intelligence & Enterprise Platform is running','version':'4.0.0','auth_enabled':os.getenv('AUTH_ENABLED','false').lower()=='true'}
@app.get('/api/health')
def health(db:Session=Depends(get_db)): 
    db.execute(__import__('sqlalchemy').text('SELECT 1'))
    return {'status':'healthy','database':'connected','timestamp':datetime.utcnow().isoformat(),'uptime_seconds':metrics()['uptime_seconds']}

# Enterprise deployment operations
@app.get('/api/monitoring', dependencies=[Depends(require_read)])
def monitoring_endpoint():
    return metrics()

@app.post('/api/admin/backup', dependencies=[Depends(require_write)])
def create_backup():
    target = backup()
    return {'success':True,'backup_file':str(target)}

@app.get('/api/performance', dependencies=[Depends(require_read)])
def performance(db:Session=Depends(get_db)):
    started=time.perf_counter()
    counts={m.__tablename__:db.query(m).count() for m in models()}
    elapsed=round((time.perf_counter()-started)*1000,2)
    return {'success':True,'query_time_ms':elapsed,'records':counts,'workers':int(os.getenv('WEB_CONCURRENCY','2'))}

# Registration Intelligence
@app.get('/api/attendees')
def attendees(db:Session=Depends(get_db)): return [serialize(x) for x in db.query(Attendee).order_by(Attendee.id.desc()).all()]
@app.post('/api/attendees',status_code=201,dependencies=[Depends(require_write)])
def add_attendee(data:AttendeeCreate,db:Session=Depends(get_db)):
    if db.query(Attendee).filter(Attendee.email==data.email).first(): raise HTTPException(409,'Attendee email already registered')
    x=Attendee(**data.model_dump()); db.add(x); db.commit(); db.refresh(x); return {'success':True,'attendee':serialize(x)}
@app.post('/api/registration/import',dependencies=[Depends(require_write)])
def import_attendees(data:ImportAttendees,db:Session=Depends(get_db)):
    added=skipped=0
    for item in data.attendees:
        if db.query(Attendee).filter(Attendee.email==item.email).first(): skipped+=1; continue
        db.add(Attendee(**item.model_dump())); added+=1
    db.commit(); return {'success':True,'source':'External Registration System','added':added,'skipped':skipped}
@app.patch('/api/attendees/{attendee_id}/check-in',dependencies=[Depends(require_write)])
def attendee_checkin(attendee_id:int,data:CheckInRequest,db:Session=Depends(get_db)):
    x=db.get(Attendee,attendee_id)
    if not x: raise HTTPException(404,'Attendee not found')
    x.checked_in=1 if data.checked_in else 0; x.status='Checked In' if data.checked_in else 'Registered'; x.checked_in_at=datetime.utcnow() if data.checked_in else None
    db.commit(); db.refresh(x); return {'success':True,'attendee':serialize(x),'message':'Check-in status updated in real time'}
@app.get('/api/registration/analytics')
def registration_analytics(db:Session=Depends(get_db)): return analyze_attendees(db.query(Attendee).all())
@app.post('/api/agents/registration/analyze')
def registration_agent(db:Session=Depends(get_db)): return {'success':True,'agent':'Registration Agent','analysis':analyze_attendees(db.query(Attendee).all())}

# Venue operations
@app.get('/api/venues')
def venues(db:Session=Depends(get_db)): return [serialize(x) for x in db.query(Venue).all()]
@app.post('/api/venues',status_code=201,dependencies=[Depends(require_write)])
def add_venue(data:VenueCreate,db:Session=Depends(get_db)):
    x=Venue(**data.model_dump()); db.add(x); db.commit(); db.refresh(x); return {'success':True,'venue':serialize(x)}
@app.post('/api/venue-agent/recommend',dependencies=[Depends(require_write)])
def venue_agent(payload:dict,db:Session=Depends(get_db)):
    return {'success':True,'agent':'Venue Agent','recommendations':recommend_venues(db.query(Venue).all(),int(payload.get('attendees',0)),payload.get('equipment',[]))}
@app.get('/api/venue-analytics')
def venue_analytics(db:Session=Depends(get_db)):
    vs=db.query(Venue).all(); return {'total':len(vs),'capacity':sum(v.capacity for v in vs),'average_utilization':round(sum(v.utilization or 0 for v in vs)/len(vs),1) if vs else 0,'available':sum(v.status.lower()=='available' for v in vs),'booked':sum(v.status.lower()=='booked' for v in vs)}

# Speaker/scheduling
@app.get('/api/speakers')
def speakers(db:Session=Depends(get_db)): return [serialize(x) for x in db.query(Speaker).all()]
@app.post('/api/speakers',status_code=201,dependencies=[Depends(require_write)])
def add_speaker(data:SpeakerCreate,db:Session=Depends(get_db)):
    x=Speaker(**data.model_dump()); db.add(x); db.commit(); db.refresh(x); return {'success':True,'speaker':serialize(x)}
@app.post('/api/speaker-agent/search',dependencies=[Depends(require_write)])
def speaker_agent(payload:dict,db:Session=Depends(get_db)): return {'success':True,'agent':'Speaker Agent','results':find_speakers(db.query(Speaker).all(),payload.get('expertise',''))}
@app.get('/api/sessions')
def sessions(db:Session=Depends(get_db)): return [serialize(x) for x in db.query(EventSession).all()]
@app.post('/api/sessions',status_code=201,dependencies=[Depends(require_write)])
def add_session(data:SessionCreate,db:Session=Depends(get_db)):
    if data.start_time>=data.end_time: raise HTTPException(400,'End time must be after start time')
    conflicts=db.query(EventSession).filter(EventSession.venue==data.venue,EventSession.start_time<data.end_time,EventSession.end_time>data.start_time).all()
    if conflicts: raise HTTPException(409,f'Schedule conflict detected for venue {data.venue}')
    x=EventSession(**data.model_dump()); db.add(x); db.commit(); db.refresh(x); return {'success':True,'session':serialize(x),'conflicts':[]}
@app.get('/api/schedule/conflicts')
def schedule_conflicts(db:Session=Depends(get_db)):
    ss=db.query(EventSession).all(); conflicts=[]
    for i,a in enumerate(ss):
        for b in ss[i+1:]:
            if a.venue==b.venue and a.start_time<b.end_time and a.end_time>b.start_time: conflicts.append({'session_a':a.title,'session_b':b.title,'venue':a.venue})
    return {'count':len(conflicts),'conflicts':conflicts}

# Sponsorship
@app.get('/api/sponsors')
def sponsors(db:Session=Depends(get_db)): return [serialize(x) for x in db.query(Sponsor).order_by(Sponsor.id.desc()).all()]
@app.post('/api/sponsors',status_code=201,dependencies=[Depends(require_write)])
def add_sponsor(data:SponsorCreate,db:Session=Depends(get_db)):
    x=Sponsor(**data.model_dump()); db.add(x); db.commit(); db.refresh(x); return {'success':True,'sponsor':serialize(x)}
@app.get('/api/agents/sponsorship/analyze/{sponsor_id}')
def sponsor_analysis(sponsor_id:int,db:Session=Depends(get_db)):
    x=db.get(Sponsor,sponsor_id)
    if not x: raise HTTPException(404,'Sponsor not found')
    return {'success':True,'agent':'Sponsorship Agent','analysis':sponsorship_agent(x)}
@app.get('/api/sponsors/analytics/summary')
def sponsor_summary(db:Session=Depends(get_db)):
    ss=db.query(Sponsor).all(); value=sum(x.contract_value or 0 for x in ss); paid=sum(x.amount_paid or 0 for x in ss); return {'total':len(ss),'contract_value':value,'amount_paid':paid,'payment_rate':round(paid/value*100,1) if value else 0,'average_engagement':round(sum(x.engagement_score or 0 for x in ss)/len(ss),1) if ss else 0,'total_leads':sum(x.leads or 0 for x in ss)}

# Incidents / alerts / workflow
@app.get('/api/incidents')
def incidents(db:Session=Depends(get_db)): return [serialize(x) for x in db.query(Incident).order_by(Incident.id.desc()).all()]
@app.post('/api/incidents',status_code=201,dependencies=[Depends(require_write)])
def add_incident(data:IncidentCreate,db:Session=Depends(get_db)):
    x=Incident(**data.model_dump()); db.add(x); db.commit(); db.refresh(x); workflow=execute_incident_workflow(db,x); return {'success':True,'incident':serialize(x),'workflow':workflow}
@app.get('/api/agents/incident/analyze/{incident_id}')
def incident_analysis(incident_id:int,db:Session=Depends(get_db)):
    x=db.get(Incident,incident_id)
    if not x: raise HTTPException(404,'Incident not found')
    return {'success':True,'agent':'Incident Agent','analysis':incident_agent(x)}
@app.patch('/api/incidents/{incident_id}',dependencies=[Depends(require_write)])
def update_incident(incident_id:int,data:IncidentUpdate,db:Session=Depends(get_db)):
    x=db.get(Incident,incident_id)
    if not x: raise HTTPException(404,'Incident not found')
    for k,v in data.model_dump(exclude_none=True).items(): setattr(x,k,v)
    x.updated_at=datetime.utcnow(); db.commit(); db.refresh(x); return {'success':True,'incident':serialize(x)}
@app.get('/api/alerts')
def alerts(db:Session=Depends(get_db)): return [serialize(x) for x in db.query(Alert).order_by(Alert.id.desc()).all()]
@app.get('/api/alerts/active')
def active_alerts(db:Session=Depends(get_db)): return [serialize(x) for x in db.query(Alert).filter(Alert.resolved==0).order_by(Alert.id.desc()).all()]
@app.patch('/api/alerts/{alert_id}/resolve',dependencies=[Depends(require_write)])
def resolve_alert(alert_id:int,db:Session=Depends(get_db)):
    x=db.get(Alert,alert_id)
    if not x: raise HTTPException(404,'Alert not found')
    x.resolved=1; db.commit(); return {'success':True,'alert':serialize(x)}

# Enterprise intelligence
@app.get('/api/intelligence')
def intelligence(db:Session=Depends(get_db)): return build_intelligence(db,models())
@app.get('/api/orchestration')
def orchestration(db:Session=Depends(get_db)): return run_orchestration(db,models())
@app.post('/api/orchestration/run',dependencies=[Depends(require_write)])
def run_orchestration_api(db:Session=Depends(get_db)): return {'success':True,'result':run_orchestration(db,models())}
@app.get('/api/executive/dashboard')
def executive_dashboard(db:Session=Depends(get_db)): return {'success':True,'intelligence':build_intelligence(db,models()),'orchestration':run_orchestration(db,models())}
