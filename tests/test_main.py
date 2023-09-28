import json
from controllers.controller import create_group
from main import db_dependency


def test_get_user_Unauthorized(client):
    response = client.get("/user/")
    assert response.status_code == 401


def test_get_user(client, header_token):
    response = client.get("/user/", headers=header_token)
    assert response.status_code == 200


def test_create_a_group(client, header_token):
    data1 = {"name": "Opel groups"}
    data2 = {"name": "Tesla"}
    response1 = client.post("/groups/", json=data1, headers=header_token)
    response2 = client.post("/groups/", json=data2, headers=header_token)
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()["name"] == "Opel groups"
    assert response2.json()["name"] == "Tesla"


def test_read_all_groups(client, header_token):
    response = client.get("/groups/", headers=header_token)
    assert response.status_code == 200


def test_read_a_group(client, header_token):
    response = client.get("/groups/1", headers=header_token)
    assert response.status_code == 200


def test_update_a_group(client, header_token):
    data = {"name": "Opel Ovius"}
    response = client.put("/groups/1", json=data, headers=header_token)
    assert response.status_code == 200
    assert response.json()["name"] == "Opel Ovius"


def test_delete_a_group(client, header_token):
    response = client.delete("/groups/1", headers=header_token)
    assert response.status_code == 200


def test_create_battery_for_group(client, header_token):
    data1 = {
        "name": "Tesla new brand",
        "latitude": 0.02143,
        "longitude": 0.12543,
        "installation_date": "2023-09-27",
        "capacity": 10,
        "charge_level": 5,
    }
    
    data2 = {
        "name": "Tesla Ovius",
        "latitude": 0.02143,
        "longitude": 0.12543,
        "installation_date": "2023-09-27",
        "capacity": 10,
        "charge_level": 10,
    }    

    response1 = client.post("/groups/1/batteries/", json=data1, headers=header_token)
    response2 = client.post("/groups/2/batteries/", json=data2, headers=header_token)
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()["name"] == "Tesla new brand"
    assert response1.json()["latitude"] == 0.02143
    assert response1.json()["longitude"] == 0.12543
    assert response1.json()["installation_date"] == "2023-09-27"
    assert response1.json()["capacity"] == 10
    assert response1.json()["charge_level"] == 5


def test_read_batteries(client, header_token):
    response = client.get("/batteries/", headers=header_token)
    assert response.status_code == 200


# /groups/{group_id}/batteries/{battery_id}
def test_update_battery(client, header_token):
    data = {
        "name": "Tesla Ovius old",
        "latitude": 0.02143,
        "longitude": 0.12543,
        "installation_date": "2023-09-27",
        "capacity": 15,
        "charge_level": 10,
    }    

    response = client.put("/groups/1/batteries/1", json=data, headers=header_token)
    assert response.status_code == 200
    assert response.json()["name"] == "Tesla Ovius old"
    assert response.json()["latitude"] == 0.02143
    assert response.json()["longitude"] == 0.12543
    assert response.json()["installation_date"] == "2023-09-27"
    assert response.json()["capacity"] == 15
    assert response.json()["charge_level"] == 10


# "/groups/{group_id}/batteries/{battery_id}"
def test_delete_battery(client, header_token):
    response = client.delete("/groups/1/batteries/1", headers=header_token)
    assert response.status_code == 200

"/batteries/{capacity}/{installation_date}/{charge_level}"
def test_find_specific_battery(client, header_token):
    response = client.get("/batteries/10/2023-09-27/10", headers=header_token)
    assert response.status_code == 200