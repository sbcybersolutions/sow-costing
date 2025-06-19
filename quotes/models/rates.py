from django.db import models

class CourseResource(models.Model):
    COMPLEXITY_CHOICES = [
        ('Simple', 'Simple'),
        ('Medium', 'Medium'),
        ('Complex', 'Complex'),
    ]
    complexity = models.CharField(max_length=20, choices=COMPLEXITY_CHOICES)
    role_name = models.CharField(max_length=100)  # e.g. SME, PM, Research & LO
    fixed_hours = models.FloatField()
    hourly_rate = models.FloatField()

    def __str__(self):
        return f"{self.complexity} - {self.role_name}"

class VideoTypeRate(models.Model):
    VIDEO_CATEGORY_CHOICES = [
        ('Live', 'Live'),
        ('Animated', 'Animated'),
    ]
    category = models.CharField(max_length=20, choices=VIDEO_CATEGORY_CHOICES)
    type_name = models.CharField(max_length=100)  # e.g. Newsdesk, Explainer 1
    rate_per_second = models.FloatField()

    def __str__(self):
        return f"{self.category}: {self.type_name}"

class FixedCost(models.Model):
    name = models.CharField(max_length=100)  # e.g. PreProduction
    amount = models.FloatField()

    def __str__(self):
        return f"{self.name} - ${self.amount}"

class StudioRate(models.Model):
    studio_name = models.CharField(max_length=100)
    hire_rate = models.FloatField()
    studio_staff = models.FloatField()
    equipment = models.FloatField()

    def __str__(self):
        return f"{self.studio_name}"

class TechnicalRate(models.Model):
    role_name = models.CharField(max_length=100)  # e.g. Filming & Directing
    daily_rate = models.FloatField()

    def __str__(self):
        return f"{self.role_name}: ${self.daily_rate}/day"

class TalentRate(models.Model):
    TALENT_TYPE_CHOICES = [
        ('Live Actor', 'Live Actor'),
        ('Puppeteer', 'Puppeteer'),
    ]
    name = models.CharField(max_length=100)
    role_type = models.CharField(max_length=20, choices=TALENT_TYPE_CHOICES)
    rate = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.role_type}): ${self.rate}"