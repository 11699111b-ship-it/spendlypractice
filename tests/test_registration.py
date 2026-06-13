from werkzeug.security import check_password_hash


def test_register_get(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Create your account" in response.data


def test_register_empty_fields(client):
    response = client.post("/register", data={
        "name": "",
        "email": "",
        "password": ""
    })
    assert response.status_code == 200
    assert b"All fields are required" in response.data


def test_register_short_password(client):
    response = client.post("/register", data={
        "name": "Test User",
        "email": "test@example.com",
        "password": "short"
    })
    assert response.status_code == 200
    assert b"Password must be at least 8 characters" in response.data


def test_register_duplicate_email(client, app):
    with app.app_context():
        from app import get_db
        from werkzeug.security import generate_password_hash
        conn = get_db()
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Existing", "taken@example.com", generate_password_hash("password123"))
        )
        conn.commit()
        conn.close()

    response = client.post("/register", data={
        "name": "New User",
        "email": "taken@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert b"An account with that email already exists" in response.data


def test_register_success_redirects_to_login(client):
    response = client.post("/register", data={
        "name": "Anurag Gupta",
        "email": "anurag@example.com",
        "password": "securepass"
    }, follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_register_success_stores_hashed_password(client, app):
    client.post("/register", data={
        "name": "Anurag Gupta",
        "email": "anurag@example.com",
        "password": "securepass"
    })
    with app.app_context():
        from app import get_db
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?", ("anurag@example.com",)
        ).fetchone()
        conn.close()
    assert user is not None
    assert user["password_hash"] != "securepass"
    assert check_password_hash(user["password_hash"], "securepass")


def test_register_error_prefills_name_and_email(client):
    response = client.post("/register", data={
        "name": "Anurag Gupta",
        "email": "anurag@example.com",
        "password": "sh"
    })
    assert b"Anurag Gupta" in response.data
    assert b"anurag@example.com" in response.data
