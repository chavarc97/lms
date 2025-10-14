from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Profile, Course_Category, DifficultyLevel, CourseStatus,
    Course, LessonType, Lesson, EnrollmentStatus, Enrollment,
    LessonProgress, Comment
)


# ==================== USER & PROFILE ====================

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer para el perfil de usuario"""
    
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'phone', 'avatar', 'is_instructor', 
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer completo para el modelo User con profile"""
    profile = ProfileSerializer(read_only=True)
    total_courses = serializers.SerializerMethodField()
    total_enrollments = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'date_joined', 'profile', 'total_courses', 'total_enrollments']
        read_only_fields = ['date_joined']
    
    def get_total_courses(self, obj):
        return obj.courses.count()
    
    def get_total_enrollments(self, obj):
        return obj.enrollments.count()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear usuarios"""
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    profile = ProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'profile']
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = User.objects.create_user(**validated_data)
        
        # Crear perfil automáticamente
        Profile.objects.create(user=user, **profile_data)
        
        return user


class UserListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar usuarios"""
    is_instructor = serializers.BooleanField(source='profile.is_instructor', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_instructor']
        

# ==================== CATEGORIES & LOOKUPS ====================

class CourseCategorySerializer(serializers.ModelSerializer):
    """Serializer para categorías de cursos"""
    total_courses = serializers.SerializerMethodField()
    
    class Meta:
        model = Course_Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'is_active', 
                  'created_at', 'total_courses']
        read_only_fields = ['slug', 'created_at']
    
    def get_total_courses(self, obj):
        return obj.course_set.count()


class DifficultyLevelSerializer(serializers.ModelSerializer):
    """Serializer para niveles de dificultad"""
    
    class Meta:
        model = DifficultyLevel
        fields = ['id', 'level_name', 'level_order', 'description']


class CourseStatusSerializer(serializers.ModelSerializer):
    """Serializer para estados de curso"""
    
    class Meta:
        model = CourseStatus
        fields = ['id', 'status_name', 'description']


class LessonTypeSerializer(serializers.ModelSerializer):
    """Serializer para tipos de lección"""
    
    class Meta:
        model = LessonType
        fields = ['id', 'type_name', 'icon', 'description']


class EnrollmentStatusSerializer(serializers.ModelSerializer):
    """Serializer para estados de inscripción"""
    
    class Meta:
        model = EnrollmentStatus
        fields = ['id', 'status_name', 'description']


# ==================== LESSONS ====================

class LessonSerializer(serializers.ModelSerializer):
    """Serializer completo para lecciones"""
    lesson_type_name = serializers.CharField(source='lesson_type.type_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'course_title', 'title', 'description', 
                  'lesson_type', 'lesson_type_name', 'content', 'video_url', 
                  'duration_minutes', 'order_index', 'is_published', 'is_free', 
                  'attachments', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class LessonListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar lecciones"""
    lesson_type_name = serializers.CharField(source='lesson_type.type_name', read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'lesson_type_name', 'duration_minutes', 
                  'order_index', 'is_published', 'is_free']


class LessonProgressSerializer(serializers.ModelSerializer):
    """Serializer para progreso de lecciones"""
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    user_username = serializers.CharField(source='enrollment.user.username', read_only=True)
    
    class Meta:
        model = LessonProgress
        fields = ['id', 'enrollment', 'lesson', 'lesson_title', 'user_username',
                  'is_completed', 'time_spent_minutes', 'completed_at', 
                  'last_accessed_at']
        read_only_fields = ['last_accessed_at']


# ==================== COURSES ====================

class CourseSerializer(serializers.ModelSerializer):
    """Serializer completo para cursos"""
    instructor_name = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    difficulty_name = serializers.CharField(source='difficulty_level.level_name', read_only=True)
    status_name = serializers.CharField(source='status.status_name', read_only=True)
    lessons = LessonListSerializer(many=True, read_only=True)
    total_lessons = serializers.SerializerMethodField()
    total_enrollments = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'instructor', 'instructor_name',
                  'category', 'category_name', 'difficulty_level', 'difficulty_name',
                  'status', 'status_name', 'thumbnail', 'price', 'duration_hours',
                  'language', 'requirements', 'learning_objectives', 'published_at',
                  'lessons', 'total_lessons', 'total_enrollments', 'average_rating',
                  'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def get_instructor_name(self, obj):
        return f"{obj.instructor.first_name} {obj.instructor.last_name}".strip() or obj.instructor.username
    
    def get_total_lessons(self, obj):
        return obj.lessons.count()
    
    def get_total_enrollments(self, obj):
        return obj.enrollments.count()
    
    def get_average_rating(self, obj):
        comments = obj.comments.filter(is_review=True, rating__isnull=False)
        if comments.exists():
            return round(sum(c.rating for c in comments) / comments.count(), 2)
        return None


class CourseListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar cursos"""
    instructor_name = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    difficulty_name = serializers.CharField(source='difficulty_level.level_name', read_only=True)
    total_lessons = serializers.SerializerMethodField()
    total_enrollments = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'instructor_name', 'category_name',
                  'difficulty_name', 'thumbnail', 'price', 'duration_hours',
                  'total_lessons', 'total_enrollments', 'average_rating']
    
    def get_instructor_name(self, obj):
        return f"{obj.instructor.first_name} {obj.instructor.last_name}".strip() or obj.instructor.username
    
    def get_total_lessons(self, obj):
        return obj.lessons.count()
    
    def get_total_enrollments(self, obj):
        return obj.enrollments.count()
    
    def get_average_rating(self, obj):
        comments = obj.comments.filter(is_review=True, rating__isnull=False)
        if comments.exists():
            return round(sum(c.rating for c in comments) / comments.count(), 2)
        return None


class CourseCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear/actualizar cursos"""
    
    class Meta:
        model = Course
        fields = ['title', 'description', 'instructor', 'category', 
                  'difficulty_level', 'status', 'thumbnail', 'price',
                  'duration_hours', 'language', 'requirements', 
                  'learning_objectives', 'published_at']
        read_only_fields = ['slug']


# ==================== ENROLLMENTS ====================

class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer completo para inscripciones"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_details = CourseListSerializer(source='course', read_only=True)
    status_name = serializers.CharField(source='status.status_name', read_only=True)
    current_lesson_title = serializers.CharField(source='current_lesson.title', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'user_username', 'user_full_name', 'course',
                  'course_title', 'course_details', 'status', 'status_name',
                  'progress_percentage', 'enrolled_at', 'completed_at',
                  'last_accessed_at', 'notes', 'current_lesson', 
                  'current_lesson_title']
        read_only_fields = ['enrolled_at', 'last_accessed_at']
    
    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear inscripciones"""
    
    class Meta:
        model = Enrollment
        fields = ['user', 'course']
    
    def validate(self, data):
        """Validar que un usuario no se inscriba dos veces al mismo curso"""
        user = data.get('user')
        course = data.get('course')
        
        if self.instance is None:  # Solo en creación
            if Enrollment.objects.filter(user=user, course=course).exists():
                raise serializers.ValidationError(
                    "El usuario ya está inscrito en este curso."
                )
        
        return data
    
    def create(self, validated_data):
        # Asignar estado inicial automáticamente
        active_status = EnrollmentStatus.objects.filter(
            status_name__iexact='active'
        ).first()
        
        if active_status:
            validated_data['status'] = active_status
        
        return super().create(validated_data)


class EnrollmentListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar inscripciones"""
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_thumbnail = serializers.ImageField(source='course.thumbnail', read_only=True)
    status_name = serializers.CharField(source='status.status_name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'course_title', 'course_thumbnail', 'status_name',
                  'progress_percentage', 'enrolled_at', 'last_accessed_at']


# ==================== COMMENTS ====================

class CommentSerializer(serializers.ModelSerializer):
    """Serializer completo para comentarios"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_username', 'user_full_name', 'course',
                  'course_title', 'content', 'rating', 'is_review',
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
    
    def validate_rating(self, value):
        """Validar que si es review, debe tener rating"""
        if self.initial_data.get('is_review') and not value:
            raise serializers.ValidationError(
                "Las reseñas deben incluir una calificación."
            )
        return value


class CommentListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar comentarios"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user_username', 'content', 'rating', 'is_review', 
                  'created_at']