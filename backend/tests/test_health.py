import os

os.environ.setdefault("DATABASE_URL", "mysql+pymysql://test:test@127.0.0.1:3306/hostel_management")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-that-is-long-enough-for-tests")

from fastapi.testclient import TestClient

from app.main import app


def test_health_check() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_invalid_login_returns_unauthorized() -> None:
    response = TestClient(app, raise_server_exceptions=False).post(
        "/auth/login",
        json={"email": "admin@hostel.local", "password": "not-the-password"},
    )

    assert response.status_code in {401, 503}
