from django.contrib import admin
from .models import (
    Profile, Course_Category, DifficultyLevel, CourseStatus,
    Course, LessonType, Lesson, EnrollmentStatus, Enrollment,
    LessonProgress, Comment
)


# ==================== INLINE ADMINS ====================

class LessonInline(admin.TabularInline):
    """Inline para lecciones en el admin de cursos"""
    model = Lesson
    extra = 1
    fields = ['title', 'lesson_type', 'order_index', 'duration_minutes', 'is_published', 'is_free']


class LessonProgressInline(admin.TabularInline):
    """Inline para progreso de lecciones en el admin de inscripciones"""
    model = LessonProgress
    extra = 0
    readonly_fields = ['lesson', 'is_completed', 'completed_at', 'time_spent_minutes']
    can_delete = False


# ==================== PROFILE ====================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_instructor', 'phone', 'created_at']
    list_filter = ['is_instructor', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Información personal', {
            'fields': ('bio', 'birth_date', 'phone', 'avatar')
        }),
        ('Permisos', {
            'fields': ('is_instructor',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ==================== CATEGORIES & LOOKUPS ====================

@admin.register(Course_Category)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(DifficultyLevel)
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ['level_name', 'level_order']
    ordering = ['level_order']


@admin.register(CourseStatus)
class CourseStatusAdmin(admin.ModelAdmin):
    list_display = ['status_name', 'description']


@admin.register(LessonType)
class LessonTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'icon']


@admin.register(EnrollmentStatus)
class EnrollmentStatusAdmin(admin.ModelAdmin):
    list_display = ['status_name', 'description']


# ==================== COURSES ====================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'difficulty_level', 
                    'status', 'price', 'published_at', 'created_at']
    list_filter = ['category', 'difficulty_level', 'status', 'language', 
                   'published_at', 'created_at']
    search_fields = ['title', 'description', 'instructor__username']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [LessonInline]
    
    fieldsets = (
        ('Información básica', {
            'fields': ('title', 'slug', 'description', 'instructor', 'category')
        }),
        ('Configuración del curso', {
            'fields': ('difficulty_level', 'status', 'language', 'price', 'duration_hours')
        }),
        ('Contenido', {
            'fields': ('thumbnail', 'requirements', 'learning_objectives')
        }),
        ('Publicación', {
            'fields': ('published_at',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('instructor', 'category', 'difficulty_level', 'status')


# ==================== LESSONS ====================

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'lesson_type', 'order_index', 
                    'duration_minutes', 'is_published', 'is_free', 'created_at']
    list_filter = ['lesson_type', 'is_published', 'is_free', 'created_at', 'course']
    search_fields = ['title', 'description', 'content', 'course__title']
    date_hierarchy = 'created_at'
    ordering = ['course', 'order_index']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('course', 'title', 'description', 'lesson_type')
        }),
        ('Contenido', {
            'fields': ('content', 'video_url', 'attachments')
        }),
        ('Configuración', {
            'fields': ('order_index', 'duration_minutes', 'is_published', 'is_free')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('course', 'lesson_type')


# ==================== ENROLLMENTS ====================

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'status', 'progress_percentage', 
                    'enrolled_at', 'completed_at']
    list_filter = ['status', 'enrolled_at', 'completed_at']
    search_fields = ['user__username', 'course__title']
    date_hierarchy = 'enrolled_at'
    ordering = ['-enrolled_at']
    readonly_fields = ['enrolled_at', 'last_accessed_at']
    inlines = [LessonProgressInline]
    
    fieldsets = (
        ('Inscripción', {
            'fields': ('user', 'course', 'status')
        }),
        ('Progreso', {
            'fields': ('progress_percentage', 'current_lesson', 'notes')
        }),
        ('Fechas', {
            'fields': ('enrolled_at', 'completed_at', 'last_accessed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'course', 'status', 'current_lesson')


# ==================== LESSON PROGRESS ====================

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'is_completed', 'time_spent_minutes', 
                    'completed_at', 'last_accessed_at']
    list_filter = ['is_completed', 'completed_at', 'last_accessed_at']
    search_fields = ['enrollment__user__username', 'lesson__title']
    date_hierarchy = 'last_accessed_at'
    ordering = ['-last_accessed_at']
    readonly_fields = ['last_accessed_at']
    
    fieldsets = (
        ('Progreso', {
            'fields': ('enrollment', 'lesson', 'is_completed', 'time_spent_minutes')
        }),
        ('Fechas', {
            'fields': ('completed_at', 'last_accessed_at'),
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('enrollment__user', 'lesson')


# ==================== COMMENTS ====================

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'rating', 'is_review', 'created_at']
    list_filter = ['rating', 'is_review', 'created_at']
    search_fields = ['user__username', 'course__title', 'content']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Comentario', {
            'fields': ('user', 'course', 'content', 'rating', 'is_review')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'course')