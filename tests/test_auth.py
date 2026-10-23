from fastapi.testclient import TestClient
from app.jwt_handler import create_access_token
from app.main import app
from app.main import check_tenant_access, check_admin_access
from fastapi import HTTPException
import pytest

client = TestClient(app)

def test_protected_endpoint_without_token():
    response = client.get("/protected")

    assert response.status_code == 401

def test_protected_endpoint_with_invalid_token():
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer invalid.token.value"},
    )

    assert response.status_code == 401

def test_protected_endpoint_with_valid_token():
    token = create_access_token(
        user_id=3,
        tenant_id=1,
        role="intern",
    )

    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


def test_same_tenant_access_allowed():
    current_user = {"tenant_id": 1, "role": "intern"}

    check_tenant_access(current_user, 1)


def test_cross_tenant_access_denied():
    current_user = {"tenant_id": 1, "role": "intern"}

    with pytest.raises(HTTPException) as exc:
        check_tenant_access(current_user, 2)

    assert exc.value.status_code == 403


def test_intern_denied_admin_access():
    current_user = {"tenant_id": 1, "role": "intern"}

    with pytest.raises(HTTPException) as exc:
        check_admin_access(current_user)

    assert exc.value.status_code == 403


def test_admin_allowed_admin_access():
    current_user = {"tenant_id": 1, "role": "admin"}

    check_admin_access(current_user)