from werkzeug.security import generate_password_hash


def _create_user(app, name="Test User", email="test@example.com", password="password123"):
    with app.app_context():
        from app import get_db
        conn = get_db()
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, generate_password_hash(password)),
        )
        conn.commit()
        conn.close()


def test_login_get(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Sign in" in response.data


def test_login_blank_fields_rejected(client):
    response = client.post("/login", data={"email": "", "password": ""})
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_login_wrong_password_rejected(client, app):
    _create_user(app)
    response = client.post("/login", data={
        "email": "test@example.com",
        "password": "wrongpassword",
    })
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_login_nonexistent_email_rejected(client):
    response = client.post("/login", data={
        "email": "nobody@example.com",
        "password": "password123",
    })
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_login_success_redirects(client, app):
    _create_user(app)
    response = client.post("/login", data={
        "email": "test@example.com",
        "password": "password123",
    }, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_login_success_sets_session(client, app):
    _create_user(app, name="Anurag")
    with client:
        client.post("/login", data={
            "email": "test@example.com",
            "password": "password123",
        })
        from flask import session
        assert session["user_id"] is not None
        assert session["user_name"] == "Anurag"


def test_login_error_prefills_email(client, app):
    _create_user(app)
    response = client.post("/login", data={
        "email": "test@example.com",
        "password": "wrongpassword",
    })
    assert b"test@example.com" in response.data


def test_logout_clears_session(client, app):
    _create_user(app)
    with client:
        client.post("/login", data={
            "email": "test@example.com",
            "password": "password123",
        })
        client.get("/logout")
        from flask import session
        assert "user_id" not in session
        assert "user_name" not in session


def test_logout_redirects_to_landing(client, app):
    _create_user(app)
    client.post("/login", data={
        "email": "test@example.com",
        "password": "password123",
    })
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_logged_in_user_redirected_from_login(client, app):
    _create_user(app)
    client.post("/login", data={"email": "test@example.com", "password": "password123"})
    response = client.get("/login", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_logged_in_user_redirected_from_register(client, app):
    _create_user(app)
    client.post("/login", data={"email": "test@example.com", "password": "password123"})
    response = client.get("/register", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "/"
