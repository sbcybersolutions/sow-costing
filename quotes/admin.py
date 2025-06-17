from django.contrib import admin
from .models import Course, LiveVideo, AnimatedVideo, Studio, Talent, TechnicalStaff
from .models import CourseResource, VideoTypeRate, FixedCost, StudioRate
from .models import TechnicalRate, TalentRate

admin.site.register(Course)
admin.site.register(LiveVideo)
admin.site.register(AnimatedVideo)
admin.site.register(Studio)
admin.site.register(Talent)
admin.site.register(TechnicalStaff)
admin.site.register(CourseResource)
admin.site.register(VideoTypeRate)
admin.site.register(FixedCost)
admin.site.register(StudioRate)
admin.site.register(TechnicalRate)  
admin.site.register(TalentRate)
