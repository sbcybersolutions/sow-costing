from django.db import models
from .rates import TechnicalRate  # ✅ pulls dynamic rates
from quotes.models.quote import Quote  # Assuming Quote model exists

class TechnicalStaff(models.Model):
    quote = models.ForeignKey(
        Quote, 
        on_delete=models.CASCADE, 
        related_name='technical_staff',
        null =True, 
        blank=True, 
    )
    filming_days = models.PositiveIntegerField(default=1)
    editing_days = models.PositiveIntegerField(default=0)

    def get_technical_internal_cost(self):
        """
        Sum daily rates for all technical roles × filming days.
        """
        total = sum(r.daily_rate for r in TechnicalRate.objects.all())
        return total * self.filming_days

    def get_editing_internal_cost(self):
        """
        Editing days × editing rate — store Editing in TechnicalRate too!
        """
        editing = TechnicalRate.objects.get(role_name="Editing").daily_rate
        return self.editing_days * editing

    def get_total_internal_cost(self):
        return self.get_technical_internal_cost() + self.get_editing_internal_cost()

    def get_total_retail_cost(self):
        return self.get_total_internal_cost() * 2

    def __str__(self):
        return f"Technical: {self.filming_days} filming, {self.editing_days} editing"