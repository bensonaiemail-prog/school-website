from django.db import models

class SchoolInfo(models.Model):
    """
    General school information (singleton model)
    """
    school_name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True, null=True)
    about = models.TextField()
    mission = models.TextField()
    vision = models.TextField()
    
    # Contact
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    
    # Social media
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    # Images
    logo = models.ImageField(upload_to='school/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='school/', blank=True, null=True)
    
    # Working hours
    working_days = models.CharField(max_length=100, default='Monday - Friday')
    working_hours = models.CharField(max_length=100, default='8:00 AM - 4:00 PM')
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'School Information'
        verbose_name_plural = 'School Information'
    
    def __str__(self):
        return self.school_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class News(models.Model):
    """
    School news and updates
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    excerpt = models.CharField(max_length=300)
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    
    is_published = models.BooleanField(default=True)
    publish_date = models.DateTimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'News'
        ordering = ['-publish_date']
    
    def __str__(self):
        return self.title