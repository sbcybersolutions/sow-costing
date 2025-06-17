from django.db import models
from .rates import StudioRate  # ✅ dynamic daily rates

class Studio(models.Model):
    STUDIO_CHOICES = [
        ('Kennington', 'Kennington'),
        ('SLV Studio 1', 'SLV Studio 1'),
        ('SLV Studio 2', 'SLV Studio 2'),
    ]

    studio_name = models.CharField(max_length=50, choices=STUDIO_CHOICES)
    filming_days = models.PositiveIntegerField(default=1)

    def get_daily_internal_cost(self):
        """
        Lookup StudioRate row and sum Hire + Staff + Equipment.
        """
        studio = StudioRate.objects.get(studio_name=self.studio_name)
        return studio.hire_rate + studio.studio_staff + studio.equipment

    def get_total_internal_cost(self):
        return self.get_daily_internal_cost() * self.filming_days

    def get_total_retail_cost(self):
        return self.get_total_internal_cost() * 2

    def __str__(self):
        return f"{self.studio_name} ({self.filming_days} days)"
