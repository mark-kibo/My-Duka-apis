import pytest
from api.signup.signupapi import app, db, bcrypt
from api.models.users import User, Store

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    client = app.test_client()

    with app.app_context():
        db.create_all()
        bcrypt.init_app(app)
        yield client

def test_signup_user(client):
    data = {
        "username": "test_user",
        "password": "test_password",
        "email": "test@example.com",
        "full_name": "Test User",
        "role": "clerk",
        "store_id": 1,
    }

    # Create a test store
    store = Store(store_name="Test Store", location="Test Location")
    store.save()

    response = client.post('/signup/', json=data)

    assert response.status_code == 201
    assert response.json['message'] == 'Clerk registered successfully'

    user = User.query.filter_by(username="test_user").first()
    assert user is not None
    assert user.role == 'clerk'

    # Clean up
    db.session.delete(user)
    db.session.delete(store)
    db.session.commit()

def test_signup_user_invalid_store(client):
    data = {
        "username": "test_user",
        "password": "test_password",
        "email": "test@example.com",
        "full_name": "Test User",
        "role": "clerk",
        "store_id": 99,  # Invalid store_id
    }

    response = client.post('/signup/', json=data)

    assert response.status_code == 400
    assert response.json['message'] == 'Invalid store_id'

def test_signup_user_duplicate_username_email(client):
    # Create a test user
    test_user = User(username="existing_user", password="password", email="existing@example.com", full_name="Existing User", role="clerk", store_id=1)
    test_user.save()

    data = {
        "username": "existing_user",
        "password": "test_password",
        "email": "test@example.com",
        "full_name": "Test User",
        "role": "clerk",
        "store_id": 1,
    }

    response = client.post('/signup/', json=data)

    assert response.status_code == 409
    assert response.json['message'] == 'Username or email already exists'

    # Clean up
    db.session.delete(test_user)
    db.session.commit()

def test_signup_user_superuser(client):
    data = {
        "username": "superuser",
        "password": "super_password",
        "email": "super@example.com",
        "full_name": "Super User",
        "role": "merchant",
        "store_id": 1,
    }

    # Create a test store
    store = Store(store_name="Test Store", location="Test Location")
    store.save()

    response = client.post('/signup/superuser/', json=data)

    assert response.status_code == 201
    assert response.json['message'] == 'Superuser registered successfully'

    user = User.query.filter_by(username="superuser").first()
    assert user is not None
    assert user.role == 'merchant'

    # Clean up
    db.session.delete(user)
    db.session.delete(store)
    db.session.commit()

if __name__ == '__main__':
    pytest.main()
