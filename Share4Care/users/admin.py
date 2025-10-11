from django.contrib import admin
from .models import UserProfile, Donation, DonationClaim, ContactMessage

class DonationAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'donor', 'city', 'created_at']
    list_filter = ['category', 'status', 'city']

class ClaimAdmin(admin.ModelAdmin):
    list_display = ['donation', 'collector', 'status', 'claimed_at']
    list_filter = ['status']

admin.site.register(UserProfile)
admin.site.register(Donation, DonationAdmin)
admin.site.register(DonationClaim, ClaimAdmin)
admin.site.register(ContactMessage)