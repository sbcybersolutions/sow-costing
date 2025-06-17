from django.db import models

class Course(models.Model):
    COMPLEXITY_CHOICES = [
        ('Simple', 'Simple'),
        ('Medium', 'Medium'),
        ('Complex', 'Complex'),
    ]

    complexity = models.CharField(max_length=20, choices=COMPLEXITY_CHOICES)
    description = models.CharField(max_length=255)
    num_languages = models.PositiveIntegerField(default=0)

    def get_cost_map(self):
        return {
            'Simple': {
                'SME': (1, 100),
                'PM': (1, 35),
                'Research & LO': (4, 35),
                'Course Writing': (6, 40),
                'Graphic Design': (2, 70),
            },
            'Medium': {
                'SME': (2, 100),
                'PM': (2, 35),
                'Research & LO': (6, 35),
                'Course Writing': (8, 40),
                'Graphic Design': (2, 70),
            },
            'Complex': {
                'SME': (3, 100),
                'PM': (3, 35),
                'Research & LO': (8, 35),
                'Course Writing': (10, 40),
                'Graphic Design': (2, 70),
            },
        }

    def get_base_internal_cost(self):
        """
        Sum of resource hours × internal hourly rates
        """
        key = str(self.complexity)
        costs = self.get_cost_map().get(key)
        if costs is None:
            return 0

        return sum(hours * rate for hours, rate in costs.values())

    def get_base_billing_cost(self):
        """
        Sum of resource hours × billing rate (2x hourly rate)
        """
        key = str(self.complexity)
        costs = self.get_cost_map().get(key)
        if costs is None:
            return 0

        return sum(hours * (rate * 2) for hours, rate in costs.values())

    def get_translation_cost(self):
        """
        Translation cost is internal = $500 per language,
        billing = 2x ($1000 per language)
        """
        return self.num_languages * 500

    def get_translation_billing_cost(self):
        """
        Billing version of translation cost: 2x
        """
        return self.get_translation_cost() * 2

    def get_total_internal_cost(self):
        """
        Base + translation, internal side
        """
        return self.get_base_internal_cost() + self.get_translation_cost()

    def get_total_retail_cost(self):
        """
        Always 2x the total internal cost.
        """
        return self.get_total_internal_cost() * 2

    def __str__(self):
        return f"{self.complexity} Course: {self.description}"
