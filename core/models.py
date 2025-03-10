from django.db import models

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.position}"

    class Meta:
        ordering = ['order']

class Technology(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('devops', 'DevOps'),
        ('mobile', 'Mobile'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="Font Awesome icon class")
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    class Meta:
        ordering = ['category', 'order']
        verbose_name_plural = "Technologies"

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    project_url = models.URLField(blank=True, null=True)
    github_repo = models.CharField(max_length=200, blank=True, null=True)
    technologies = models.ManyToManyField(Technology, related_name="projects")
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} from {self.name}"

    class Meta:
        ordering = ['-created_at']
