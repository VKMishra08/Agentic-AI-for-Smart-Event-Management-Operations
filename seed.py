from database import Base,engine,SessionLocal
from models import Attendee,Venue,Speaker,Session,Sponsor,Incident,Alert
Base.metadata.create_all(bind=engine)
db=SessionLocal()
if db.query(Attendee).count()==0:
 db.add_all([Attendee(name='Aarav Singh',email='aarav@example.com',organization='Tech University',category='Student',age_group='18-25',source='Web'),Attendee(name='Neha Kapoor',email='neha@example.com',organization='DataWorks',category='Professional',age_group='26-35',source='Partner Portal'),Attendee(name='Rohan Mehta',email='rohan@example.com',organization='AI Labs',category='Professional',age_group='26-35',source='Mobile App',checked_in=1,status='Checked In'),Attendee(name='Priya Verma',email='priya@example.com',organization='Innovation Club',category='Student',age_group='18-25',source='Web',checked_in=1,status='Checked In'),Attendee(name='Kabir Shah',email='kabir@example.com',organization='CloudSphere',category='Speaker',age_group='36-45',source='Partner Portal',checked_in=1,status='Checked In'),Attendee(name='Meera Joshi',email='meera@example.com',organization='FutureTech',category='Professional',age_group='26-35',source='Mobile App')])
if db.query(Venue).count()==0:
 db.add_all([Venue(name='Grand Hall',capacity=500,venue_type='Auditorium',location='Block A',equipment='Projector,Stage,AV',utilization=72),Venue(name='Innovation Lab',capacity=120,venue_type='Workshop',location='Block B',equipment='Projector,Whiteboard,Wi-Fi',utilization=58),Venue(name='Tech Room 1',capacity=80,venue_type='Seminar',location='Block C',equipment='Projector,Wi-Fi',status='Booked',utilization=86)])
if db.query(Speaker).count()==0:
 db.add_all([Speaker(name='Dr. Rahul Sharma',role='Keynote Speaker',company='AI Labs',expertise='AI, Machine Learning, Deep Learning',rating=4.9),Speaker(name='Priya Verma',role='Industry Speaker',company='DataWorks',expertise='Artificial Intelligence, Data Science',rating=4.8),Speaker(name='Arjun Mehta',role='Cloud Architect',company='CloudSphere',expertise='Generative AI, Cloud Computing',rating=4.7)])
if db.query(Session).count()==0:
 db.add_all([Session(title='AI in Enterprise',speaker='Dr. Rahul Sharma',venue='Grand Hall',start_time='10:00',end_time='11:00',attendees=300,status='Confirmed'),Session(title='Generative AI Workshop',speaker='Arjun Mehta',venue='Innovation Lab',start_time='11:15',end_time='12:15',attendees=90,status='Confirmed')])
if db.query(Sponsor).count()==0:
 db.add_all([Sponsor(name='TechNova',tier='Platinum',contract_value=150000,amount_paid=135000,leads=320,engagement_score=92),Sponsor(name='CloudSphere',tier='Gold',contract_value=90000,amount_paid=60000,leads=180,engagement_score=76),Sponsor(name='AI Labs',tier='Silver',contract_value=45000,amount_paid=20000,leads=65,engagement_score=48),Sponsor(name='DataWorks',tier='Gold',contract_value=85000,amount_paid=80000,leads=240,engagement_score=84)])
if db.query(Incident).count()==0:
 db.add_all([Incident(title='Speaker Cancellation',category='Speaker',description='Keynote speaker cancelled before session.',severity='High',affected_people=120,owner='Speaker Operations'),Incident(title='Projector Failure',category='Technical',description='Projector stopped working in Room A.',severity='Medium',affected_people=25,owner='Venue Operations')])
db.commit(); db.close(); print('Seed data ready')
