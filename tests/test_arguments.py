# tests/test_arguments.py

# proves analyze works when Claude is mocked

from fastapi.testclient import TestClient

from app.main import app
from tests.conftest import create_user_and_token

error_client = TestClient(app, raise_server_exceptions=False)


def fake_successful_analysis(text: str):
    return {
        "main_claim": "Cats are better than dogs",
        "premises": [
            {
                "text": "Cats are more independent",
                "type": "supporting",
                "order": 0,
            }
        ],
        "fallacies": [],
        "argument_strength": "moderate",
        "analysis": "Simple structured argument.",
        "score": 65,
        "model_name": "claude-sonnet-4-20250514",
        "prompt_version": "v1",
        "latency_ms": 123.45,
        "analysis_status": "success",
        "error_type": None,
    }


def test_analyze_returns_structured_result(client, monkeypatch):
    monkeypatch.setattr(
        "app.routers.arguments.analyze_argument_with_claude",
        fake_successful_analysis,
    )

    _, token = create_user_and_token(client)

    response = client.post(
        "/arguments/analyze",
        json={"text": "Cats are better than dogs because they are more independent."},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    body = response.json()
    assert body["main_claim"] == "Cats are better than dogs"
    assert body["argument_strength"] == "moderate"
    assert body["score"] == 65
    assert len(body["premises"]) == 1
    assert body["premises"][0]["text"] == "Cats are more independent"
    assert body["fallacies"] == []
    assert body["model_name"] == "claude-sonnet-4-20250514"
    assert body["prompt_version"] == "v1"
    assert body["latency_ms"] == 123.45
    assert body["analysis_status"] == "success"
    assert body["error_type"] is None


def test_list_arguments_requires_token(client):
    response = client.get("/arguments")
    assert response.status_code in (401, 403)


def test_analyze_rejects_invalid_token(client):
    response = client.post(
        "/arguments/analyze",
        json={"text": "Cats are better than dogs because they are more independent."},
        headers={"Authorization": "Bearer definitely-not-a-real-token"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_analyze_stores_result_and_list_arguments_returns_it(client, monkeypatch):
    monkeypatch.setattr(
        "app.routers.arguments.analyze_argument_with_claude",
        fake_successful_analysis,
    )

    _, token = create_user_and_token(client)

    analyze_response = client.post(
        "/arguments/analyze",
        json={"text": "Cats are better than dogs because they are more independent."},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert analyze_response.status_code == 200

    list_response = client.get(
        "/arguments",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert list_response.status_code == 200
    body = list_response.json()

    assert body["total"] >= 1
    assert len(body["items"]) >= 1
    assert body["items"][0]["main_claim"] == "Cats are better than dogs"


def test_analyze_returns_server_error_when_claude_fails(client, monkeypatch):
    def fake_failure(text: str):
        raise RuntimeError("Claude is down")

    monkeypatch.setattr(
        "app.routers.arguments.analyze_argument_with_claude",
        fake_failure,
    )

    _, token = create_user_and_token(client)

    response = error_client.post(
        "/arguments/analyze",
        json={"text": "Test argument"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 500