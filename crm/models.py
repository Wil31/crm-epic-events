from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


class Client(models.Model):
    class ClientStatus(models.TextChoices):
        POTENTIAL = "PTN"
        ACTUAL = "ACT"

    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT
    )
    client_status = models.CharField(choices=ClientStatus.choices, max_length=3)

    def __str__(self):
        return self.email


class Contract(models.Model):
    client = models.ForeignKey(
        to=Client, on_delete=models.PROTECT, related_name="client_contract"
    )
    status = models.BooleanField(default=True)
    amount = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)
    payment_due = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client} - Contract ID: {self.id}"


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
    attendees = models.PositiveIntegerField(null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client} - Event ID: {self.id}"
