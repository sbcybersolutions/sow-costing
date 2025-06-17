from django.db import models
from .livevideo import LiveVideo

class Talent(models.Model):
    TALENT_CHOICES = [
        ('Sarah', 'Sarah'),
        ('Sam', 'Sam'),
        ('Matt', 'Matt'),
        ('Nicolette', 'Nicolette'),
        ('Drew', 'Drew'),
        ('Warrick', 'Warrick'),
        ('Neil', 'Neil'),
    ]

    ROLE_TYPE_CHOICES = [
        ('Live Actor', 'Live Actor'),
        ('Puppeteer', 'Puppeteer'),
    ]

    name = models.CharField(max_length=50, choices=TALENT_CHOICES)
    role_type = models.CharField(max_length=20, choices=ROLE_TYPE_CHOICES, blank=True)
    rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    live_video = models.ForeignKey(
        LiveVideo,
        on_delete=models.CASCADE,
        related_name='talents'  # ✅ FIXED: now .talents is valid
    )

    def save(self, *args, **kwargs):
        """
        Automatically sets rate and role_type based on selected name.
        """
        rate_map = {
            'Sarah': (540, 'Live Actor'),
            'Sam': (1015, 'Live Actor'),
            'Matt': (915, 'Live Actor'),
            'Nicolette': (880, 'Live Actor'),
            'Drew': (880, 'Live Actor'),
            'Warrick': (810, 'Puppeteer'),
            'Neil': (810, 'Puppeteer'),
        }

        if self.name in rate_map:
            self.rate, self.role_type = rate_map[self.name]

        super().save(*args, **kwargs)

    def get_internal_cost(self):
        return float(self.rate or 0)

    def get_retail_cost(self):
        return self.get_internal_cost() * 2

    def __str__(self):
        return f"{self.name} ({self.role_type})"
