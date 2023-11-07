from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from applications.common.models import TimeStampedModel

User = get_user_model()


class PeriodModel(models.Model):
    date_from = models.DateField(verbose_name=_("date from"), blank=False)
    date_to = models.DateField(verbose_name=_("date to"), blank=True, null=True)

    class Meta:
        abstract = True

    def clean(self):
        if self.date_to and self.date_from > self.date_to:
            raise ValidationError(_("Date from cannot be later than ending date."))

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Department(models.Model):
    name = models.CharField(
        verbose_name=_("name"), max_length=150, blank=False, null=False, unique=True
    )
    short_name = models.CharField(
        verbose_name=_("short name"), max_length=20, blank=True
    )
    manager = models.ForeignKey(
        User,
        verbose_name=_("manager"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def __str__(self):
        return f"{self.name}"


class Position(models.Model):
    class PositionType(models.TextChoices):
        CORE = (
            "core",
            _("core position"),
        )

        HELPER = (
            "helper",
            _("helper position"),
        )

    name = models.CharField(
        verbose_name=_("name"), max_length=150, blank=False, null=False
    )
    code = models.PositiveIntegerField(verbose_name=_("position code"), blank=True)
    position_type = models.CharField(
        verbose_name=_("position_type"),
        choices=PositionType.choices,
        default=PositionType.CORE,
        max_length=10,
    )

    class Meta:
        verbose_name = _("Posision")
        verbose_name_plural = _("Positions")

    def __str__(self):
        return f"{self.name}"


class WorkingTime(PeriodModel):
    employee = models.ForeignKey("profiles.EmployeeProfile", on_delete=models.CASCADE)
    working_time = models.DecimalField(
        _("working time"), max_digits=3, decimal_places=2, default=1
    )

    class Meta:
        verbose_name = _("WorkingTime")
        verbose_name_plural = _("WorkingTime")

    def __str__(self):
        return f"{self.working_time} - {self.date_from}"


# class AbsenceType(PeriodModel):
#     name = models.CharField(_("name"), max_length=100, blank=False, null=False)


class EmployeeDepartment(PeriodModel):
    employee = models.ForeignKey(
        "profiles.EmployeeProfile",
        on_delete=models.CASCADE,
        related_name="employee_department_value_ec",
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="employee_department_value_d"
    )

    class Meta:
        unique_together = ("employee", "department")
        db_table = "tbl_employee_department"


class EmployeePosition(PeriodModel):
    employee = models.ForeignKey(
        "profiles.EmployeeProfile",
        on_delete=models.CASCADE,
        related_name="employee_position_value_e",
    )
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="employee_position_value_p"
    )

    class Meta:
        unique_together = ("employee", "position")
        db_table = "tbl_employee_position"


class EmployeeProfile(TimeStampedModel):
    class CompanyTree(models.TextChoices):
        CEO = (
            "CEO",
            _("CEO"),
        )

        TOP_MANAGER = (
            "TM",
            _("Top Manager"),
        )
        MANAGER = (
            "M",
            _("Manager"),
        )
        NOT_MANAGER = ("N", _("Not Manager"))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    gender = models.CharField(
        verbose_name=_("gender"),
        choices=(("W", _("woman")), ("M", _("man")), ("N", _("not specified"))),
        max_length=2,
        default="N",
    )
    work_email = models.EmailField(_("work email"), null=True, blank=True)
    position = models.ManyToManyField(
        Position, through=EmployeePosition, related_name="employee_position_value"
    )

    is_manager = models.CharField(
        verbose_name=_("is manager"),
        choices=CompanyTree.choices,
        default=CompanyTree.NOT_MANAGER,
        max_length=3,
    )
    workplace = models.ManyToManyField(
        Department,
        verbose_name=_("department"),
        through=EmployeeDepartment,
        related_name="employee_department_value",
    )
    annual_leave = models.PositiveIntegerField(
        _("annual leave entitlement"), default=26
    )
    current_leave = models.IntegerField(_("current leave entitlement"), default=0)
    date_hire = models.DateField(_("hire date"), null=True, blank=True)
    contract_end = models.DateField(_("contract end"), null=True, blank=True)
    # absence_info = models.ForeignKey(
    #     AbsenceType, blank=True, null=True, on_delete=models.SET_NULL
    # )
    additional_info = models.CharField(
        _("additional information"), blank=True, max_length=150
    )

    class Meta:
        verbose_name = _("Employee Profile")
        verbose_name_plural = _("Employees Profiles")

    def __str__(self):
        return f"_({self.user.first_name} {self.user.last_name}'s Employment Details)"

    def clean(self):
        if self.date_hire and self.contract_end and self.date_hire > self.contract_end:
            raise ValidationError(_("Contract end cannot be later than hire date."))

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
