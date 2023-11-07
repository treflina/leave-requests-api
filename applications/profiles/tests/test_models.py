import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_department_str(department_factory):
    dep = department_factory(name="Test Department")
    assert str(dep) == dep.name


def test_create_department_with_duplicate_name_should_fail(department_factory):
    department_factory(name="Test Department")
    with pytest.raises(IntegrityError):
        department_factory(name="Test Department")


def test_position_str(position_factory):
    pos = position_factory()
    assert str(pos) == pos.name


def test_incorrect_dates_to_should_fail(employee_position_factory):
    with pytest.raises(ValidationError):
        employee_position_factory(date_from="2024-10-01", date_to="2023-10-01")
    assert ValidationError(message="Date from cannot be later than ending date.")


def test_employee_profile_str(employee_profile_factory):
    emp_profile = employee_profile_factory()
    assert (
        str(emp_profile)
        == f"""_({emp_profile.user.first_name} {emp_profile.user.last_name}'s Employment Details)"""  # noqa: E501
    )


def test_working_time_str(working_time_factory):
    wt = working_time_factory(date_from="2024-10-01")
    assert (
        str(wt)
        == f"{wt.working_time} - {wt.date_from}"
    )


def test_date_hire_after_contract_end_should_fail(employee_profile_factory):
    with pytest.raises(ValidationError):
        employee_profile_factory(date_hire="2024-10-01")
