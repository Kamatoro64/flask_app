import pytest
from app import app, db, User  # Import the app and database

# Create a custom fixture that will setup the test database for each test.
# The test_client fixture is passed to each test function. 
@pytest.fixture
def test_client():
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for tests
    with app.app_context():
        db.create_all()  # Create tables in the test database
        yield app.test_client()  # Flask test client
        db.session.remove()
        db.drop_all()  # Clean up database after tests

def test_create_user(test_client):
    response = test_client.post('/users', json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 201
    assert response.get_json() == {"message": "User created successfully"}

def test_get_users(test_client):
    # Add a test user
    user = User(name="Jane Doe", email="jane@example.com")
    db.session.add(user)
    db.session.commit()

    response = test_client.get('/users')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['name'] == "Jane Doe"

def test_get_user(test_client):
    # Add a test user
    user = User(name="Alice", email="alice@example.com")
    db.session.add(user)
    db.session.commit()

    response = test_client.get(f'/users/{user.id}')
    data = response.get_json()
    assert response.status_code == 200
    assert data['name'] == "Alice"

def test_update_user(test_client):
    # Add a test user
    user = User(name="Bob", email="bob@example.com")
    db.session.add(user)
    db.session.commit()

    response = test_client.put(f'/users/{user.id}', json={"name": "Bobby"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "User updated successfully"}

    # Verify the update
    updated_user = db.session.get(User, user.id)
    assert updated_user.name == "Bobby"

def test_delete_user(test_client):
    # Add a test user
    user = User(name="Charlie", email="charlie@example.com")
    db.session.add(user)
    db.session.commit()

    response = test_client.delete(f'/users/{user.id}')
    assert response.status_code == 200
    assert response.get_json() == {"message": "User deleted successfully"}

    # Verify deletion
    deleted_user = db.session.get(User, user.id)
    assert deleted_user is None
