from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "due_date", "status", "created_at")
    list_filter = ("status", "due_date")
    search_fields = ("title", "description", "user__username")