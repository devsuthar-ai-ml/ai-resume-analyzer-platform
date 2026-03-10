def test_register_and_login(client):
    register_payload = {
        "email": "john@example.com",
        "full_name": "John Doe",
        "password": "StrongPassword123",
    }
    register_response = client.post("/api/auth/register", json=register_payload)

    assert register_response.status_code == 200
    register_body = register_response.json()
    assert "access_token" in register_body
    assert register_body["user"]["email"] == register_payload["email"]

    login_payload = {"email": "john@example.com", "password": "StrongPassword123"}
    login_response = client.post("/api/auth/login", json=login_payload)

    assert login_response.status_code == 200
    login_body = login_response.json()
    assert login_body["token_type"] == "bearer"


def test_login_invalid_password(client):
    register_payload = {
        "email": "badpass@example.com",
        "full_name": "Bad Pass",
        "password": "StrongPassword123",
    }
    client.post("/api/auth/register", json=register_payload)

    response = client.post(
        "/api/auth/login",
        json={"email": "badpass@example.com", "password": "wrong"},
    )
    assert response.status_code == 401
