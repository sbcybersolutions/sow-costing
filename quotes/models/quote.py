from django.db import models
from django.contrib.auth.models import User

class Quote(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Sent', 'Sent'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    client_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')  # ✅ new!
    is_archived = models.BooleanField(default=False)  # ✅ new!
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.project_name} ({self.date})"
