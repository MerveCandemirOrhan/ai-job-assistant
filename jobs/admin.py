from django.contrib import admin

from .models import Job, CV


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = ("title", "company", "location", "job_type", "created_at")


@admin.register(CV)
class CVAdmin(admin.ModelAdmin):

    list_display = ("name", "uploaded_at")