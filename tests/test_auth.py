
data = {"username": "admin", "password": "admin"}

def test_create_user(client):
    response = client.post("/auth/", json=data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201
