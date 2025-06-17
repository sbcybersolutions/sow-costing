from django.db import models

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
        PreProduction ($375) + Music & Graphics ($100)
        """
        return 375 + 100

    def get_variable_internal_cost(self):
        """
        Per-second rate for chosen video type.
        """
        rate_map = {
            'Explainer 1': 35.00,
            'Explainer 2': 37.30,
            'Explainer 3': 57.60,
        }

        rate = rate_map.get(str(self.video_type), 0)
        return self.num_seconds * rate

    def get_total_internal_cost(self):
        return self.get_fixed_internal_cost() + self.get_variable_internal_cost()

    def get_total_retail_cost(self):
        return self.get_total_internal_cost() * 2

    def __str__(self):
        return f"{self.video_type} ({self.num_seconds}s): {self.description}"
