
#def test_get_manager(test_client, manager_user):
#    resp = test_client.get("/api/users/user-by-username/manager1")
#    assert resp.json["email"] == manager_user.email


def test_add_user(test_client, manager_user):

    auth_header = {
        'Authorization': f'Bearer {manager_user.token}'
    }
    data = {"username": "test-user-01", "password": "secret", "email": "test-user-01@example.com"}
    r = test_client.post("/api/users", json=data, headers=auth_header)
    
    assert r.status_code == 201

    #import ipdb;ipdb.set_trace()
    #user = database.session.query(User).filter_by(username="u").one()
    #assert user is not None
