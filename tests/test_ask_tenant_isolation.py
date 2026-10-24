
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.jwt_handler import create_access_token
from app.main import app

client = TestClient(app)


def test_ask_uses_tenant_and_role_from_authenticated_token():
    token = create_access_token(
        user_id=3,
        tenant_id=1,
        role="intern",
    )

    with patch(
        "app.main.ask_question",
        return_value="Authorized test answer",
    ) as mock_ask:
        response = client.post(
            "/ask",
            headers={"Authorization": f"Bearer {token}"},
            json={"question": "What is RAG?"},
        )

    assert response.status_code == 200

    mock_ask.assert_called_once_with(
        question="What is RAG?",
        tenant_id=1,
        role="intern",
    )
    