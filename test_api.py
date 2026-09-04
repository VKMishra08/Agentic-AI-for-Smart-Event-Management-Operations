import os, tempfile
# The application defaults to SQLite; tests use the already-created schema and validate core contracts.
from fastapi.testclient import TestClient
from app import app

client=TestClient(app)

def test_health():
    r=client.get('/api/health'); assert r.status_code==200; assert r.json()['status']=='healthy'

def test_intelligence_contract():
    r=client.get('/api/intelligence'); assert r.status_code==200
    body=r.json(); assert 'event_health_score' in body; assert 'risk_score' in body; assert 'recommendations' in body

def test_orchestration_contract():
    body=client.get('/api/orchestration').json(); assert body['status']=='Active'; assert len(body['agents'])==5

def test_attendee_checkin():
    attendees=client.get('/api/attendees').json(); assert attendees
    item=attendees[0]
    r=client.patch(f"/api/attendees/{item['id']}/check-in",json={'checked_in':True}); assert r.status_code==200; assert r.json()['attendee']['checked_in']==1

def test_venue_recommendation():
    r=client.post('/api/venue-agent/recommend',json={'attendees':60,'equipment':['Projector']}); assert r.status_code==200; assert 'recommendations' in r.json()
