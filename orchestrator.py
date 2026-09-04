from datetime import datetime

def run_orchestration(db,models):
    Attendee,Venue,Speaker,Session,Sponsor,Incident,Alert=models
    checks={
      'Registration Agent':db.query(Attendee).count(),
      'Venue Agent':db.query(Venue).count(),
      'Speaker Agent':db.query(Speaker).count(),
      'Sponsorship Agent':db.query(Sponsor).count(),
      'Incident Agent':db.query(Incident).count(),
    }
    return {'orchestrator':'Event Operations Orchestrator','status':'Active','last_run':datetime.utcnow().isoformat(),'agents':[{'name':k,'status':'Active','records_analyzed':v} for k,v in checks.items()],'sequence':['Ingest operational data','Run specialized agents','Correlate cross-domain signals','Calculate event health & risk','Generate recommendations','Publish alerts and executive insights']}
