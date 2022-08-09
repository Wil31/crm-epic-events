from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


# class ClientStatus(models.Model):
#     status = models.CharField(max_length=25, unique=True, default="Potential")


class Client(models.Model):
    class ClientStatus(models.TextChoices):
        POTENTIAL = "PTN"
        ACTUAL = "ACT"

    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=25)
    phone = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20, null=True)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT
    )
    client_status = models.CharField(choices=ClientStatus.choices, max_length=3)


class Contract(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.PROTECT)
    status = models.BooleanField(default=True)
    amount = models.FloatField(validators=[MinValueValidator(0)], null=True)
    payment_due = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Event(models.Model):
    class EventStatus(models.TextChoices):
        TO_BE_PLANNED = "TBP"
        IN_PROGRESS = "INP"
        PLANNING_DONE = "PLD"

    client = models.ForeignKey(to=Client, on_delete=models.PROTECT)
    event_status = models.CharField(choices=EventStatus.choices, max_length=3)
    support_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT
    )
    attendees = models.PositiveIntegerField(null=True)
    event_date = models.DateTimeField(null=True)
    notes = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
