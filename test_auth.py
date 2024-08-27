from fastapi.testclient import TestClient
from pytest import fixture
from helpers.getdb import get_db
from main import app
"""from config.app import Config
from router.web import web
from router.api import api
from router.apipublic import api as api_public
from router.auth import auth

app = Config().add_middleware()
app.include_router(auth)
app.include_router(web)
app.include_router(api)
app.include_router(api_public)"""

client = TestClient(app=app)


@fixture()
def test_db():
    return get_db()

def test_root(test_db):
    response = client.get("/admin/api/")
    
    assert response.status_code == 200