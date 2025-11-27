from django.db import models
from django.conf import settings

class Announcement(models.Model):
    """
    Announcements for different user groups
    """
    AUDIENCE_CHOICES = [
        ('ALL', 'Everyone'),
        ('PARENTS', 'Parents Only'),
        ('TEACHERS', 'Teachers Only'),
        ('STUDENTS', 'Students Only'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    audience = models.CharField(max_length=10, choices=AUDIENCE_CHOICES, default='ALL')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    
    # Publishing
    is_published = models.BooleanField(default=True)
    publish_date = models.DateTimeField()
    expiry_date = models.DateTimeField(blank=True, null=True)
    
    # Attachments
    attachment = models.FileField(upload_to='announcements/', blank=True, null=True)
    
    # Meta
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_announcements'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-publish_date']
    
    def __str__(self):
        return self.title