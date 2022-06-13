from django.contrib import admin
from .models import Course, Comment, CourseSelection, Episode,Sector

admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(CourseSelection)

admin.site.register(Episode)
admin.site.register(Sector)

