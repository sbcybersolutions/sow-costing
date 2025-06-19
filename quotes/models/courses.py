from django.db import models
from .rates import CourseResource  # ✅ NEW: pulls rates from DB
from quotes.models.quote import Quote  # ✅ NEW: import Quote model

class Course(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)
    COMPLEXITY_CHOICES = [
        ('Simple', 'Simple'),
        ('Medium', 'Medium'),
        ('Complex', 'Complex'),
    ]

    complexity = models.CharField(max_length=20, choices=COMPLEXITY_CHOICES)
    description = models.CharField(max_length=255)
    num_languages = models.PositiveIntegerField(default=0)

    def get_base_internal_cost(self):
        """
        Lookup CourseResource rows for this complexity,
        then sum fixed_hours × hourly_rate.
        """
        resources = CourseResource.objects.filter(complexity=self.complexity)
        total = sum(r.fixed_hours * r.hourly_rate for r in resources)
        return total

    def get_base_billing_cost(self):
        """
        Billing cost: base internal cost × 2.
        """
        return self.get_base_internal_cost() * 2

    def get_translation_cost(self):
        """
        Translation cost is internal = $500 per language.
        """
        return self.num_languages * 500

    def get_translation_billing_cost(self):
        """
        Billing version of translation: 2x.
        """
        return self.get_translation_cost() * 2

    def get_total_internal_cost(self):
        """
        Base internal + translation internal.
        """
        return self.get_base_internal_cost() + self.get_translation_cost()

    def get_total_retail_cost(self):
        """
        Always 2x total internal.
        """
        return self.get_total_internal_cost() * 2

    def __str__(self):
        return f"{self.complexity} Course: {self.description}"