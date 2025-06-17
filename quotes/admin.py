from django.contrib import admin
from .models import Course, LiveVideo, AnimatedVideo, Studio, Talent, TechnicalStaff

admin.site.register(Course)
admin.site.register(LiveVideo)
admin.site.register(AnimatedVideo)
admin.site.register(Studio)
admin.site.register(Talent)
admin.site.register(TechnicalStaff)
