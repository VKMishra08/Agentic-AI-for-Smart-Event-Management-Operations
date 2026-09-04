from registration_agent import analyze_attendees
from agents import sponsorship_agent, incident_agent

def build_intelligence(db, models):
    Attendee,Venue,Speaker,Session,Sponsor,Incident,Alert=models
    attendees=db.query(Attendee).all(); venues=db.query(Venue).all(); speakers=db.query(Speaker).all(); sessions=db.query(Session).all(); sponsors=db.query(Sponsor).all(); incidents=db.query(Incident).all(); alerts=db.query(Alert).filter(Alert.resolved==0).all()
    reg=analyze_attendees(attendees)
    capacity=sum(v.capacity for v in venues); avg_util=round(sum(v.utilization or 0 for v in venues)/len(venues),1) if venues else 0
    critical=sum(1 for i in incidents if (i.priority or '').lower()=='critical' or (i.severity or '').lower()=='critical')
    high=sum(1 for i in incidents if (i.priority or '').lower()=='high' or (i.severity or '').lower()=='high')
    avg_sponsor=round(sum(s.engagement_score or 0 for s in sponsors)/len(sponsors),1) if sponsors else 0
    capacity_pressure=max(0,(reg['total']-capacity)/max(capacity,1)*100)
    risk=min(100,round(critical*28+high*14+len(alerts)*8+max(0,70-reg['check_in_rate'])*0.35+max(0,avg_util-85)*1.1+capacity_pressure*0.3))
    health=max(0,min(100,round(100-risk*0.62)))
    recommendations=[]
    if reg['pending']>0: recommendations.append(f"Registration desk should prepare for {reg['pending']} pending check-ins.")
    if capacity_pressure>0: recommendations.append('Attendance exceeds current venue capacity; reallocate rooms or enable overflow capacity.')
    elif capacity and reg['total']>capacity*.8: recommendations.append('Capacity utilization is above 80%; monitor room allocation and queue times.')
    if critical or high: recommendations.append(f'{critical} critical and {high} high-priority incidents require active operational oversight.')
    if avg_sponsor<60 and sponsors: recommendations.append('Sponsor engagement is below target; trigger sponsor success actions and follow-up.')
    if avg_util>85: recommendations.append('Venue utilization is high; run Venue Agent optimization before schedule changes.')
    if not recommendations: recommendations.append('Event operations are stable. Continue real-time monitoring.')
    top_sponsors=sorted([sponsorship_agent(s) for s in sponsors],key=lambda x:x['performance_score'],reverse=True)[:3]
    recent_incidents=sorted([incident_agent(i) for i in incidents],key=lambda x:x['risk_score'],reverse=True)[:3]
    return {'event_health_score':health,'risk_score':risk,'status':'Critical' if risk>=75 else 'Attention' if risk>=45 else 'Healthy','generated_at':__import__('datetime').datetime.utcnow().isoformat(),'registrations':reg,'venue':{'total':len(venues),'capacity':capacity,'average_utilization':avg_util},'speakers':{'total':len(speakers),'scheduled_sessions':len(sessions),'available':sum(1 for s in speakers if s.availability.lower()=='available')},'sponsors':{'total':len(sponsors),'average_engagement':avg_sponsor,'top_performers':top_sponsors},'incidents':{'total':len(incidents),'critical':critical,'high':high,'open':sum(1 for i in incidents if i.status not in ('Resolved','Closed')),'top_risks':recent_incidents},'active_alerts':len(alerts),'recommendations':recommendations}
