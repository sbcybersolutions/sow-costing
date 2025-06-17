from django.db import models

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
        PreProduction ($375) + Music & Graphics ($100)
        """
        return 375 + 100

    def get_variable_internal_cost(self):
        """
        Per-second rate for chosen video type.
        """
        rate_map = {
            'Newsdesk': 8.50,
            'Course Video': 12.60,
            'Bespoke Video': 15.40,
            'Music Video': 18.70,
        }

        rate = rate_map.get(str(self.video_type), 0)
        return self.num_seconds * rate

    def get_talent_internal_cost(self):
        """
        Sum internal cost for all attached talents.
        The related_name 'talents' comes from Talent model.
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
