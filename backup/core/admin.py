from django.contrib import admin
from .models import TeamMember, Technology, ContactMessage, Project

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order')
    search_fields = ('name', 'position')
    list_filter = ('position',)
    ordering = ('order',)

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order')
    search_fields = ('name', 'category')
    list_filter = ('category',)
    ordering = ('category', 'order')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'order')
    search_fields = ('name', 'description')
    ordering = ('order',)
