from django.db import models
from quotes.models.livevideo import LiveVideo  # ✅ absolute import
from quotes.models.rates import TalentRate     # ✅ absolute import
from quotes.models.quote import Quote  # Assuming Quote model exists

class Talent(models.Model):
    quote = models.ForeignKey(
        Quote, 
        on_delete=models.CASCADE, 
        related_name='talents',
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=50)
    role_type = models.CharField(max_length=20, blank=True)  # auto-set from TalentRate
    rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    live_video = models.ForeignKey(
        LiveVideo,
        on_delete=models.CASCADE,
        related_name='talents'
    )

    def save(self, *args, **kwargs):
        """
        Look up rate & role type from TalentRate dynamically.
        """
        tr = TalentRate.objects.get(name=self.name)
        self.rate = tr.rate
        self.role_type = tr.role_type
        super().save(*args, **kwargs)

    def get_internal_cost(self):
        return float(self.rate or 0)

    def get_retail_cost(self):
        return self.get_internal_cost() * 2

    def __str__(self):
        return f"{self.name} ({self.role_type})"