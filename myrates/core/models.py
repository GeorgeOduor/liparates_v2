from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Towns(models.Model):
    county = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Services(models.Model):
    title        = models.CharField(max_length=100)
    description  = models.TextField()
    requirements = models.TextField()
    
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class ServiceRequirements(models.Model):
    requirement = models.TextField()
    service     = models.ForeignKey(Services, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
class Prices(models.Model):
    service    = models.ForeignKey(Services, on_delete=models.CASCADE)
    town       = models.ForeignKey(Towns, on_delete=models.CASCADE)
    amount     = models.DecimalField(max_digits=10, decimal_places=2)
    approved   = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    
    
class ApplicationRecords(models.Model):
    user                 = models.ForeignKey(User, on_delete=models.CASCADE)
    service              = models.ForeignKey(Services, on_delete=models.CASCADE)
    amount               = models.DecimalField(max_digits=10, decimal_places=2)
    # balance              = models.DecimalField(max_digits=10, decimal_places=2)
    paymentStatus        = models.TextField(max_length=30,choices=[('Pending','Pending'),('Approved','Approved'),('Unpaid','Unpaid'),('Declined','Declined')])
    transactioncode      = models.CharField(max_length=100)
    resolution           = models.TextField(max_length=100,choices=[('New','New'),('Queued','Queued'),('Closed','Closed')])
    remarks              = models.TextField(null=True)
    filesUploaded        = models.CharField(null=True,max_length=1024)
    invoice              = models.CharField(null=True,max_length=1024)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    
    # def __str__(self):
    #     return self.service
    
    

class ApplicationFiles(models.Model):
    application = models.ForeignKey(ApplicationRecords, on_delete=models.CASCADE)
    file        = models.FileField( upload_to='files/')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.file
    
    
class CompanyProfile(models.Model):
    name        = models.CharField(max_length=100)
    address     = models.TextField()
    mobile      = models.CharField(max_length=12)
    email       = models.EmailField()
    paybill     = models.CharField(max_length=100)
    accountno   = models.CharField(max_length=100)
    tillno      = models.CharField(max_length=100)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    

class MpesaTransactions(models.Model):
    phone           = models.CharField(max_length=12)
    amount          = models.DecimalField(max_digits=10, decimal_places=2)
    transction_code = models.CharField(max_length=100,unique=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    title       = models.CharField(max_length=100)
    description = models.TextField()
    type        = models.CharField(max_length=100,choices=[('New','New'),('Queued','Queued'),('Closed','Closed')])
    sender      = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
