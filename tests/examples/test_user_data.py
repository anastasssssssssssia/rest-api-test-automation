def test_user_data_id_is_one(user_data):
    assert user_data["id"] == 1


def test_user_data_name_is_anna(user_data):
    assert user_data["name"] == "Anna"


def test_user_data_email_is_str(user_data):
    assert isinstance(user_data["email"], str)


def test_user_data_age_is_int(user_data):
    assert type(user_data["age"]) is int


def test_user_data_active_is_bool(user_data):
    assert isinstance(user_data["active"], bool)


def test_user_data_has_required_keys(user_data):
    for key in ("id", "name", "email", "age", "active"):
        assert key in user_data


def test_user_data_age_is_greater_than_18(user_data):
    assert user_data["age"] > 18
