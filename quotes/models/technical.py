from django.db import models

class TechnicalStaff(models.Model):
    filming_days = models.PositiveIntegerField(default=1)
    editing_days = models.PositiveIntegerField(default=0)

    def get_technical_internal_cost(self):
        """
        Sum of Filming & Directing, Sound Monitoring, Lighting & Autocue,
        Travel, Food & Water per filming day.
        """
        per_day = (
            600 +  # Filming & Directing
            600 +  # Sound Monitoring
            470 +  # Lighting & Autocue
            100 +  # Travel to Studio
            100    # Food & Water
        )
        return self.filming_days * per_day

    def get_editing_internal_cost(self):
        """
        Editing days × $475.
        """
        return self.editing_days * 475

    def get_total_internal_cost(self):
        return self.get_technical_internal_cost() + self.get_editing_internal_cost()

    def get_total_retail_cost(self):
        return self.get_total_internal_cost() * 2

    def __str__(self):
        return f"Technical Staff: {self.filming_days} filming days, {self.editing_days} editing days"
