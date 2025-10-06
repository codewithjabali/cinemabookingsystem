from django.db import models
from django.utils import timezone

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    password = models.CharField(max_length=128)  # Hash later

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Advisor(models.Model):
    # Advisor info
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    # Customer info (when account creation fails)
    customer_first_name = models.CharField(max_length=50, blank=True, null=True)
    customer_last_name = models.CharField(max_length=50, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=15, blank=True, null=True)

    assigned_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.customer_first_name} {self.customer_last_name}) {self.customer_email} {self.customer_phone} {self.assigned_at}"
    
class Booking(models.Model):
    customer_email = models.EmailField(unique=False)
    advisor = models.CharField(max_length=100, blank=True, null=True)
    productions_name = models.CharField(max_length=100)
    production_type = models.CharField(max_length=100)
    booked_at = models.DateTimeField(auto_now_add=True)
    seat_preference = models.IntegerField()

    def __str__(self):
        return f"Booking for {self.customer_email} with {self.advisor} on {self.booked_at}"

class perfomance(models.Model):
    no_tickets_sold = models.IntegerField()
    date_of_perfomance = models.DateField()
    
    def __str__(self):
        return f"{self.date_of_perfomance}  {self.no_tickets_sold}"
    
    
class production(models.Model):
    production_name = models.CharField(max_length=100)
    production_type = models.CharField(max_length=100) #concert/play/movie
    start_date = models.DateField()
    
    def __str__(self):
        return f"{self.production_name} ({self.production_type})  {self.start_date}"    