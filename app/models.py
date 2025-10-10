from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_instructor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

class Course_Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class DifficultyLevel(models.Model):
    level_name = models.CharField(max_length=20, unique=True)
    level_order = models.PositiveSmallIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.level_name

    class Meta:
        ordering = ['level_order']

class CourseStatus(models.Model):
    status_name = models.CharField(max_length=20, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.status_name

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Course_Category, on_delete=models.CASCADE)
    difficulty_level = models.ForeignKey(DifficultyLevel, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(CourseStatus, on_delete=models.SET_NULL, null=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration_hours = models.PositiveIntegerField()
    language = models.CharField(max_length=2, default='en')
    requirements = models.TextField()
    learning_objectives = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class LessonType(models.Model):
    type_name = models.CharField(max_length=20, unique=True)
    icon = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.type_name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField()
    lesson_type = models.ForeignKey(LessonType, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField()
    order_index = models.PositiveIntegerField()
    is_published = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    attachments = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order_index']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class EnrollmentStatus(models.Model):
    status_name = models.CharField(max_length=20, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.status_name

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    status = models.ForeignKey(EnrollmentStatus, on_delete=models.SET_NULL, null=True)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    current_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

class LessonProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    time_spent_minutes = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['enrollment', 'lesson']

    def __str__(self):
        return f"{self.enrollment.user.username} - {self.lesson.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_review = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s comment on {self.course.title}"


