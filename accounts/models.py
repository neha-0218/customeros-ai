from django.db import models
from django.contrib.auth.models import AbstractUser
from core.base_models import BaseModel


class Organization(BaseModel):
    """
    The company using CustomerOS AI (e.g. a SaaS company's product team).
    This is the top of our multi-tenancy hierarchy.
    """
    name = models.CharField(max_length=255)
    plan = models.CharField(
        max_length=50,
        choices=[
            ('free', 'Free'),
            ('pro', 'Pro'),
            ('enterprise', 'Enterprise'),
        ],
        default='free'
    )
    industry = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    A person using CustomerOS AI — PM, Analyst, or CS Lead.
    Extends Django's built-in User so we keep auth (login, password hashing,
    permissions) for free instead of reinventing it.

    NOTE: This is NOT a customer of Acme's product. This is someone on
    Acme's team using OUR platform. Do not confuse with CustomerAccount below.
    """
    ROLE_CHOICES = [
        ('pm', 'Product Manager'),
        ('analyst', 'Product Analyst'),
        ('cs_lead', 'Customer Success Lead'),
        ('admin', 'Admin'),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='pm')

    def __str__(self):
        return f"{self.username} ({self.role})"


class CustomerAccount(BaseModel):
    """
    A B2B customer account belonging to an Organization.
    This is what gets tracked for health score, churn risk, feedback, tickets.

    Example: If "Acme SaaS Inc" (Organization) uses CustomerOS AI,
    then "Globex Corp" (CustomerAccount) is one of Acme's own paying customers.
    """
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='customer_accounts'
    )
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, blank=True)
    plan_tier = models.CharField(
        max_length=50,
        choices=[
            ('starter', 'Starter'),
            ('growth', 'Growth'),
            ('enterprise', 'Enterprise'),
        ],
        default='starter'
    )
    mrr = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Monthly Recurring Revenue — used to weight churn impact"
    )
    contract_start_date = models.DateField(null=True, blank=True)
    contract_renewal_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name