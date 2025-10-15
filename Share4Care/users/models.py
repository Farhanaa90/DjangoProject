from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    USER_TYPES = (
        ('donor', 'Donor'),
        ('collector', 'Collector'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # ← ADD THIS LINE
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class Donation(models.Model):
    CATEGORY_CHOICES = (
        ('food', 'Food'),
        ('clothing', 'Clothing'),
        ('furniture', 'Furniture'),
        ('other', 'Other'),
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('claimed', 'Claimed'),
        ('collected', 'Collected'),
        ('expired', 'Expired'),
    )
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    pickup_address = models.TextField()
    city = models.CharField(max_length=100)
    expiration_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='donations/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        if self.expiration_date and self.expiration_date < timezone.now().date():
            return True
        return False

    def __str__(self):
        return f"{self.title} by {self.donor.username}"

class DonationClaim(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('collected', 'Collected'),
    )
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='claims')
    collector = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    claimed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['donation', 'collector']

    def __str__(self):
        return f"{self.collector.username} claimed {self.donation.title}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.name}"