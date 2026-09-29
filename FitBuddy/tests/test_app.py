import os
os.environ['DEMO_MODE']='true'
os.environ.pop('GOOGLE_API_KEY',None)
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_home():
    r=client.get('/');assert r.status_code==200 and 'FitBuddy' in r.text
def test_generate():
    r=client.post('/generate-workout',data={'name':'Test User','user_id':'TEST001','age':'21','weight':'60','goal':'general wellness','intensity':'medium'});assert r.status_code==200 and '7-Day' in r.text
def test_feedback():
    client.post('/generate-workout',data={'name':'Feedback User','user_id':'TEST002','age':'22','weight':'65','goal':'muscle gain','intensity':'low'})
    r=client.post('/submit-feedback',data={'user_id':'TEST002','feedback':'Make it gentler and add mobility.'});assert r.status_code==200 and 'updated' in r.text.lower()
def test_api():
    r=client.get('/api/users');assert r.status_code==200 and isinstance(r.json(),list)
def test_admin():
    r=client.get('/view-all-users');assert r.status_code==200 and 'All users' in r.text
