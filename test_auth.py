from fastapi.testclient import TestClient
from json import dumps
from config.app import Config 

client = TestClient(app=Config().add_middleware(), base_url="http://127.0.0.1:8000")



def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_login_fail():
    response = client.post("/auth/token", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 404


def test_access_token():
    response = client.get("/", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXY0QHRlc3QuaW8iLCJleHAiOjE3MjI0NDE0MTV9.qhaluJN086H6oCG6mjssYZCp1rhaVx7nftF8I9KwT_o"})
    assert response.status_code == 200