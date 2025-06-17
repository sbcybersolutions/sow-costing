from django.db import models

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
        Hire Rate + Studio Staff + Equipment for selected studio.
        """
        cost_map = {
            'Kennington': {'Hire Rate': 945, 'Studio Staff': 270, 'Equipment': 270},
            'SLV Studio 1': {'Hire Rate': 1005, 'Studio Staff': 0, 'Equipment': 640},
            'SLV Studio 2': {'Hire Rate': 540, 'Studio Staff': 0, 'Equipment': 0},
        }

        daily = cost_map.get(str(self.studio_name), {})
        total_daily = sum(daily.values())
        return total_daily

    def get_total_internal_cost(self):
        return self.get_daily_internal_cost() * self.filming_days

    def get_total_retail_cost(self):
        return self.get_total_internal_cost() * 2

    def __str__(self):
        return f"{self.studio_name} ({self.filming_days} days)"
