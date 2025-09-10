from django.db import models
from django.utils import timezone

class Alert(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ])
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class Fishery(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    capacity = models.IntegerField()
    current_occupancy = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class PollutionReport(models.Model):
    location = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    reported_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50, default='reported', choices=[
        ('reported', 'Reported'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
    ])
    
    def __str__(self):
        return f"Pollution at {self.location}"

class SafePlace(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    capacity = models.IntegerField()
    contact_info = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class SMSSubscriber(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(default=timezone.now)
    last_notification_sent = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.phone_number

class NotificationLog(models.Model):
    subscriber = models.ForeignKey(SMSSubscriber, on_delete=models.CASCADE)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='sent', choices=[
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ])
    
    def __str__(self):
        return f"Notification to {self.subscriber.phone_number} for {self.alert.title}"