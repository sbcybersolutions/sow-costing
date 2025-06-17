from django.db import models
from .rates import VideoTypeRate, FixedCost  # ✅ dynamic rates

class AnimatedVideo(models.Model):
    VIDEO_TYPE_CHOICES = [
        ('Explainer 1', 'Explainer 1'),
        ('Explainer 2', 'Explainer 2'),
        ('Explainer 3', 'Explainer 3'),
    ]

    video_type = models.CharField(max_length=50, choices=VIDEO_TYPE_CHOICES)
    num_seconds = models.PositiveIntegerField()
    description = models.CharField(max_length=255)

    def get_fixed_internal_cost(self):
        """
        Sum all FixedCost rows.
        """
        total = sum(f.amount for f in FixedCost.objects.all())
        return total

    def get_variable_internal_cost(self):
        """
        Lookup per-second rate for this Animated video type.
        """
        rate = VideoTypeRate.objects.get(category="Animated", type_name=self.video_type).rate_per_second
        return self.num_seconds * rate

    def get_total_internal_cost(self):
        return self.get_fixed_internal_cost() + self.get_variable_internal_cost()

    def get_total_retail_cost(self):
        return self.get_total_internal_cost() * 2

    def __str__(self):
        return f"{self.video_type} ({self.num_seconds}s): {self.description}"

