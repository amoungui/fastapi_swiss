from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from auths.auth import get_db
from config.database import Base

from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


@pytest.fixture
def header_token(client: TestClient):
    test_name = "admin"
    test_pass = "admin"
    data = {"username": test_name, "password": test_pass}
    response = client.post("/auth/token", data=data)
    print(response.status_code)
    print(response.text)
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
