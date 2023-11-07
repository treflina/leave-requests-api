from decimal import Decimal

import factory
from faker import Factory as FakerFactory

from applications.profiles.models import (
    Department,
    EmployeePosition,
    EmployeeProfile,
    Position,
    WorkingTime,
)
from applications.users.tests.factories import UserFactory

faker = FakerFactory.create()


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department

    name = "Quality Control Department"
    short_name = "QC"
    manager = factory.SubFactory(UserFactory)


class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Position

    name = "Quality Controller"
    code = 345621
    position_type = "core"


class EmployeeProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeeProfile

    user = factory.SubFactory(UserFactory)
    gender = "M"
    work_email = factory.LazyAttribute(lambda x: faker.email())
    is_manager = "M"
    annual_leave = 20
    current_leave = 10
    date_hire = "2023-10-26"
    contract_end = "2023-10-27"
    additional_info = "test additional information"

    @factory.post_generation
    def position(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.position.add(*extracted)

    @factory.post_generation
    def workplace(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.workplace.add(*extracted)


class WorkingTimeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WorkingTime

    employee = factory.SubFactory(EmployeeProfileFactory)
    working_time = Decimal("0.99")


class EmployeePositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmployeePosition

    employee = factory.SubFactory(EmployeeProfileFactory)
    position = factory.SubFactory(PositionFactory)
