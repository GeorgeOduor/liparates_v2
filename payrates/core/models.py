from django.db import models
from django.conf import settings
from .scripts import search_location

# Service Model
class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    base_fee = models.DecimalField(max_digits=10, decimal_places=2)  # Optional: Base service fee

    def __str__(self):
        return self.name


# Property Model
class Property(models.Model):
    TITLE_TYPE_CHOICES = [
        ('FREEHOLD', 'Freehold'),
        ('LEASEHOLD', 'Leasehold'),
        ('OTHER', 'Other'),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('LAND', 'Land'),
        ('BUILDING', 'Building'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')
    county = models.CharField(max_length=100)  # Specify the county
    town = models.CharField(max_length=100)  # Specify the town
    locality = models.CharField(max_length=255)  # Additional location details
    title_type = models.CharField(max_length=20, choices=TITLE_TYPE_CHOICES, default='FREEHOLD')  # Type of land title
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='LAND')  # Land or Building
    lr_number = models.CharField(max_length=50, unique=True, blank=True)  # Land Registration Number
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Latitude for map
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Longitude for map
    area_size = models.FloatField()  # In acres or square meters
    property_documents = models.FileField(upload_to='property_documents/')  # Upload property documents

    def __str__(self):
        return f"{self.lr_number} - {self.property_type} in {self.county}, {self.town}"
    
    def fetch_lat_long(self):
        # Fetch latitude and longitude using the search_location function
        location = search_location(city=self.town, county=self.county, country='Kenya')
        if location:
            self.latitude = location[0]['lat']
            self.longitude = location[0]['lon']
            self.save()


# Application Model
class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('UNDER_REVIEW', 'Under Review'),
        # ('INVOICED', 'Invoiced'),
        ('COMPLETED', 'Completed'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='applications')
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Application {self.id} for {self.client.email}"


# Intermediate Model: ApplicationService
class ApplicationService(models.Model):
    application = models.ForeignKey('Application', on_delete=models.CASCADE, related_name='application_services')
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='application_services')
    quantity = models.PositiveIntegerField(default=1)  # Number of times this service is requested
    requested_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the service was added

    def __str__(self):
        return f"{self.service.name} in Application {self.application.id} (x{self.quantity})"


# Payment Model
class Payment(models.Model):
    application = models.ForeignKey('Application', on_delete=models.CASCADE, related_name='payments')
    mpesa_transaction_id = models.CharField(max_length=50, unique=True)
    total_amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50, default="SUCCESS")  # e.g., SUCCESS, FAILED

    def __str__(self):
        return f"Payment {self.mpesa_transaction_id} - {self.total_amount_paid}"


# Intermediate Model: PaymentService
class PaymentService(models.Model):
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, related_name='payment_services')
    application_service = models.ForeignKey('ApplicationService', on_delete=models.CASCADE, related_name='payment_services')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment for {self.application_service.service.name} in Payment {self.payment.mpesa_transaction_id}"


# Invoice Model
class Invoice(models.Model):
    application = models.OneToOneField('Application', on_delete=models.CASCADE, related_name='invoice')
    invoice_document = models.FileField(upload_to='invoices/')
    issued_date = models.DateTimeField(auto_now_add=True)
    payment_instructions = models.TextField()  # Instructions for client to pay the county

    def __str__(self):
        return f"Invoice for Application {self.application.id}"

# Company Profile Model
class CompanyProfile(models.Model):
    name          = models.CharField(max_length=255, unique=True)  # Company name
    address       = models.TextField(null=True, blank=True)  # Physical address
    phone_number  = models.CharField(max_length=15, null=True, blank=True)  # Contact number
    email         = models.EmailField(null=True, blank=True)  # Contact email
    mpesa_paybill = models.CharField(max_length=20, null=True, blank=True)  # MPESA Paybill number
    mpesa_till    = models.CharField(max_length=20, null=True, blank=True)  # MPESA Till number
    created_at    = models.DateTimeField(auto_now_add=True)  # Record creation time
    updated_at    = models.DateTimeField(auto_now=True)  # Last update time

    def __str__(self):
        return self.name

