from django.contrib import admin
from .models import SchoolInfo, News

@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance
        return not SchoolInfo.objects.exists()

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'publish_date']
    list_filter = ['is_published', 'publish_date']
    search_fields = ['title', 'content']