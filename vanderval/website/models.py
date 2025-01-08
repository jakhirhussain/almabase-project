from django.db import models


# Create your models here.
class Site(models.Model):
    RECORD_CAPACITY_VERY_LOW = 0 # user records between 0-500
    RECORD_CAPACITY_LOW = 1  # user records between 500-10000
    RECORD_CAPACITY_MEDIUM = 2  # user records between 10000-50000
    RECORD_CAPACITY_HIGH = 3  # user records between 50000-200000
    RECORD_CAPACITY_VERY_HIGH = 4 # user records more than 200000

    RECORD_CAPACITY_CHOICES = (
        (RECORD_CAPACITY_VERY_LOW, "Very Low"),
        (RECORD_CAPACITY_LOW, "Low"),
        (RECORD_CAPACITY_MEDIUM, "Medium"),
        (RECORD_CAPACITY_HIGH, "High"),
        (RECORD_CAPACITY_VERY_HIGH, "Very High"),
    )

    # Fields
    name = models.CharField(max_length=100)
    domain = models.URLField()
    url = models.URLField()
    description = models.TextField()
    record_capacity = models.IntegerField(choices=RECORD_CAPACITY_CHOICES, default=RECORD_CAPACITY_VERY_LOW)

    def update_record_capacity(self):
        active_record_count = self.user_records.filter(is_active=True).count()

        if 0 <= active_record_count < 500:
            return self.RECORD_CAPACITY_VERY_LOW
        elif 500 <= active_record_count < 1000:
            return self.RECORD_CAPACITY_LOW
        elif 1000 <= active_record_count < 50000:
            return self.RECORD_CAPACITY_MEDIUM
        elif 50000 <= active_record_count < 200000:
            return self.RECORD_CAPACITY_HIGH
        else:
            return self.RECORD_CAPACITY_VERY_HIGH
        
    def save(self, *args, **kwargs):
        self.record_capacity = self.update_record_capacity()
        super().save(*args, **kwargs)


# you can choose to reuse the User model from django.contrib.auth.models
class UserRecords(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="user_records")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    dob = models.DateField()
    is_active = models.BooleanField(default=True)  # do not count for active records if false
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tasks(models.Model):
    # Task Statuses
    PENDING = "PENDING" 
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    
    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
        (FAILED, "Failed"),
    )

    # Fields
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="tasks")
    user_record = models.ForeignKey(
        UserRecords, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    task_name = models.CharField(max_length=255)
    execution_time = models.IntegerField(help_text="Estimated execution time in seconds")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=PENDING
    )
    failure_reason = models.TextField(null=True, blank=True)


    def get_task_priority(self):
        priority_map = {
            Site.RECORD_CAPACITY_VERY_LOW: 'low_priority',   
            Site.RECORD_CAPACITY_LOW: 'low_priority',        
            Site.RECORD_CAPACITY_MEDIUM: 'medium_priority',  
            Site.RECORD_CAPACITY_HIGH: 'high_priority',      
            Site.RECORD_CAPACITY_VERY_HIGH: 'high_priority', 
        }
        
        return priority_map.get(self.site.record_capacity, 'low_priority')

