from django.db import models

# Create your models here.

class FAQ(models.Model):
    question = models.CharField(max_length=200,unique=True)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['created_at']
        
        
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)  # User's name
    mobile = models.CharField(max_length=12)  # User's email
    subject = models.CharField(max_length=255)  # Optional subject
    message = models.TextField()  # Message content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the message was created

    def __str__(self):
        return f"Message from {self.name} - {self.mobile}"        

