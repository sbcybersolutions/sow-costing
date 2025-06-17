from django.db import models
from .rates import VideoTypeRate, FixedCost  # ✅ pulls dynamic rates

class LiveVideo(models.Model):
    VIDEO_TYPE_CHOICES = [
        ('Newsdesk', 'Newsdesk'),
        ('Course Video', 'Course Video'),
        ('Bespoke Video', 'Bespoke Video'),
        ('Music Video', 'Music Video'),
    ]

    video_type = models.CharField(max_length=50, choices=VIDEO_TYPE_CHOICES)
    num_seconds = models.PositiveIntegerField()
    description = models.CharField(max_length=255)

    def get_fixed_internal_cost(self):
        """
        Sum all FixedCost rows (PreProduction, Music & Graphics, etc)
        """
        total = sum(f.amount for f in FixedCost.objects.all())
        return total

    def get_variable_internal_cost(self):
        """
        Lookup per-second rate for this Live video type.
        """
        rate = VideoTypeRate.objects.get(category="Live", type_name=self.video_type).rate_per_second
        return self.num_seconds * rate

    def get_talent_internal_cost(self):
        """
        Sum all attached Talent costs.
        """
        return sum(talent.get_internal_cost() for talent in self.talents.all()) #type: ignore

    def get_total_internal_cost(self):
        """
        Fixed + Variable + Talent.
        """
        return (
            self.get_fixed_internal_cost()
            + self.get_variable_internal_cost()
            + self.get_talent_internal_cost()
        )

    def get_total_retail_cost(self):
        return self.get_total_internal_cost() * 2

    def __str__(self):
        return f"{self.video_type} ({self.num_seconds}s): {self.description}"
