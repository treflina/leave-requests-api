import pytest
from pytest_factoryboy import register

from applications.profiles.tests.factories import (
    DepartmentFactory,
    EmployeeProfileFactory,
    PositionFactory,
    EmployeePositionFactory,
    WorkingTimeFactory
)
from applications.users.tests.factories import UserFactory

register(EmployeeProfileFactory)
register(UserFactory)
register(DepartmentFactory)
register(PositionFactory)
register(EmployeePositionFactory)
register(WorkingTimeFactory)


@pytest.fixture
def normal_user(db, user_factory):
    new_user = user_factory.create()
    return new_user


@pytest.fixture
def super_user(db, user_factory):
    new_user = user_factory.create(is_superuser=True, is_staff=True)
    return new_user
