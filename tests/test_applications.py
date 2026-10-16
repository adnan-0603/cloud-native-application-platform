import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import JobApplication


test_engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    with TestingSessionLocal() as db:
        db.execute(delete(JobApplication))
        db.commit()

    yield

    with TestingSessionLocal() as db:
        db.execute(delete(JobApplication))
        db.commit()


def test_create_application():
    response = client.post(
        "/applications",
        json={
            "company": "Siemens",
            "role": "DevOps Engineer",
            "application_date": "2026-10-16",
            "status": "Applied",
            "notes": "Automated test",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["company"] == "Siemens"
    assert data["role"] == "DevOps Engineer"
    assert data["status"] == "Applied"
    assert data["notes"] == "Automated test"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Example Corp",
            "role": "Platform Engineer",
            "application_date": "2026-10-16",
        },
    )

    application_id = create_response.json()["id"]

    response = client.get(f"/applications/{application_id}")

    assert response.status_code == 200
    assert response.json()["id"] == application_id
    assert response.json()["company"] == "Example Corp"


def test_get_missing_application():
    response = client.get("/applications/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}


def test_list_applications_with_limit():
    client.post(
        "/applications",
        json={
            "company": "First Corp",
            "role": "Cloud Engineer",
            "application_date": "2026-10-16",
        },
    )

    client.post(
        "/applications",
        json={
            "company": "Second Corp",
            "role": "DevOps Engineer",
            "application_date": "2026-10-16",
        },
    )

    response = client.get("/applications?limit=1")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["company"] == "Second Corp"


@pytest.mark.parametrize("limit", [0, 101])
def test_invalid_application_limit(limit):
    response = client.get(f"/applications?limit={limit}")

    assert response.status_code == 422


def test_update_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Siemens",
            "role": "DevOps Engineer",
            "application_date": "2026-10-16",
        },
    )

    application_id = create_response.json()["id"]

    response = client.patch(
        f"/applications/{application_id}",
        json={
            "status": "Interview",
            "notes": "Technical interview scheduled",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Interview"
    assert data["notes"] == "Technical interview scheduled"
    assert data["company"] == "Siemens"


def test_update_missing_application():
    response = client.patch(
        "/applications/999999",
        json={"status": "Interview"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}


def test_delete_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Delete Corp",
            "role": "Cloud Engineer",
            "application_date": "2026-10-16",
        },
    )

    application_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/applications/{application_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/applications/{application_id}"
    )

    assert get_response.status_code == 404


def test_delete_missing_application():
    response = client.delete("/applications/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Application not found"}


def test_invalid_status():
    response = client.post(
        "/applications",
        json={
            "company": "Example Corp",
            "role": "Engineer",
            "application_date": "2026-10-16",
            "status": "Unknown",
        },
    )

    assert response.status_code == 422
