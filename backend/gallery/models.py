from django.db import models
from django.conf import settings

class GalleryCategory(models.Model):
    """
    Categories for gallery images
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Gallery Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """
    Gallery images for public view
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='gallery/')
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='images'
    )
    
    # Publishing
    is_published = models.BooleanField(default=True)
    event_date = models.DateField(blank=True, null=True)
    
    # Meta
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_images'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title