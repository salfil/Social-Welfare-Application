from django.contrib import admin
from django.contrib import admin

# admin file registers the models 
from .models import Post, Category, Staff, Comment, Programme, ProgrammeType, AppointmentBooking
admin.site.register(Post)
admin.site.register(Programme)
admin.site.register(ProgrammeType)
admin.site.register(Category)
admin.site.register(Staff)
admin.site.register(Comment)
admin.site.register(AppointmentBooking)



 
