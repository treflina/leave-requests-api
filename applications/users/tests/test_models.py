import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_create_normal_user(normal_user):
    assert normal_user.first_name is not None
    assert normal_user.last_name is not None
    assert normal_user.username is not None
    assert normal_user.password is not None
    assert normal_user.pkid is not None
    assert not normal_user.is_staff
    assert not normal_user.is_superuser
    assert normal_user.is_active


def test_create_superuser(super_user):
    assert super_user.first_name is not None
    assert super_user.last_name is not None
    assert super_user.username is not None
    assert super_user.password is not None
    assert super_user.pkid is not None
    assert super_user.is_staff
    assert super_user.is_superuser
    assert super_user.is_active


def test_get_full_name(normal_user):
    full_name = normal_user.get_full_name
    expected_full_name = (
        f"{normal_user.first_name.title()} {normal_user.last_name.title()}"
    )
    assert full_name == expected_full_name


def test_get_unique_name(normal_user):
    unique_name = normal_user.get_unique_name
    expected_unique_name = f"""{normal_user.first_name.title()} \
{normal_user.last_name.title()} {normal_user.additional_identifier}"""
    assert expected_unique_name == unique_name


def test_update_user(normal_user):
    new_first_name = "John"
    new_last_name = "Doe"
    normal_user.first_name = new_first_name
    normal_user.last_name = new_last_name
    normal_user.save()

    updated_user = User.objects.get(pk=normal_user.pk)
    assert updated_user.first_name == new_first_name
    assert updated_user.last_name == new_last_name


def test_delete_user(normal_user):
    user_pk = normal_user.pk
    normal_user.delete()

    with pytest.raises(User.DoesNotExist):
        User.objects.get(pk=user_pk)


def test_user_str(normal_user):
    assert (
        str(normal_user)
        == f"{normal_user.first_name.title()} \
{normal_user.last_name.title()} {normal_user.additional_identifier}"
    )


def test_user_str_with_no_additional_identifier(user_factory):
    normal_user = user_factory(additional_identifier=None)
    assert (
        str(normal_user)
        == f"{normal_user.first_name.title()} {normal_user.last_name.title()}"
    )


def test_create_user_with_no_username(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(username=None)
    assert str(err.value) == "Users must have a username."


def test_create_user_with_already_existing_username_should_fail(user_factory):
    user_factory.create(username="test")
    with pytest.raises(IntegrityError):
        user_factory.create(username="test")


def test_create_user_with_no_firstname(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None)
    assert str(err.value) == "Users must have a first name."


def test_create_user_with_no_lastname(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(last_name=None)
    assert str(err.value) == "Users must have a last name."


def test_create_superuser_with_no_username(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(username=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "Users must have a username."


def test_create_superuser_with_no_password(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(password=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "Superuser must have a password."


def test_super_user_is_not_staff(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, is_staff=False)
    assert str(err.value) == "Superuser must have is_staff=True."


def test_user_with_is_staff_is_not_superuser(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=False, is_staff=True)
    assert str(err.value) == "Superuser must have is_superuser=True."
