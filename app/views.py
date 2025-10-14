from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render

from .models import (
    Profile, Course_Category, DifficultyLevel, CourseStatus,
    Course, LessonType, Lesson, EnrollmentStatus, Enrollment,
    LessonProgress, Comment
)
from .serializers import (
    ProfileSerializer, UserSerializer, UserCreateSerializer, UserListSerializer,
    CourseCategorySerializer, DifficultyLevelSerializer, CourseStatusSerializer,
    LessonTypeSerializer, EnrollmentStatusSerializer,
    CourseSerializer, CourseListSerializer, CourseCreateUpdateSerializer,
    LessonSerializer, LessonListSerializer, LessonProgressSerializer,
    EnrollmentSerializer, EnrollmentCreateSerializer, EnrollmentListSerializer,
    CommentSerializer, CommentListSerializer
)

# =================== HOME ===================
def index(request):
    return render(request, 'index.html')

# ==================== USER & PROFILE ====================

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios.
    
    list: Listar todos los usuarios
    create: Crear un nuevo usuario
    retrieve: Obtener detalles de un usuario
    update: Actualizar un usuario
    destroy: Eliminar un usuario
    """
    queryset = User.objects.select_related('profile').all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'list':
            return UserListSerializer
        return UserSerializer
    
    @swagger_auto_schema(
        operation_description="Obtener el perfil del usuario",
        responses={200: ProfileSerializer()}
    )
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """Obtener el perfil del usuario"""
        user = self.get_object()
        serializer = ProfileSerializer(user.profile)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Actualizar el perfil del usuario",
        request_body=ProfileSerializer,
        responses={200: ProfileSerializer()}
    )
    @action(detail=True, methods=['patch'])
    def update_profile(self, request, pk=None):
        """Actualizar el perfil del usuario"""
        user = self.get_object()
        serializer = ProfileSerializer(user.profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Obtener los cursos donde el usuario es instructor",
        responses={200: CourseListSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def courses_taught(self, request, pk=None):
        """Obtener los cursos que enseña el usuario"""
        user = self.get_object()
        courses = user.courses.all()
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Obtener las inscripciones del usuario",
        responses={200: EnrollmentListSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """Obtener las inscripciones del usuario"""
        user = self.get_object()
        enrollments = user.enrollments.select_related('course', 'status').all()
        serializer = EnrollmentListSerializer(enrollments, many=True)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar perfiles de usuario.
    """
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_instructor']
    search_fields = ['user__username', 'bio']


# ==================== LOOKUPS (Categorías, Niveles, Estados, etc.) ====================

class CourseCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar categorías de cursos.
    """
    queryset = Course_Category.objects.all()
    serializer_class = CourseCategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    lookup_field = 'slug'
    
    @swagger_auto_schema(
        operation_description="Obtener cursos de una categoría",
        responses={200: CourseListSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def courses(self, request, slug=None):
        """Obtener cursos de una categoría específica"""
        category = self.get_object()
        courses = category.course_set.all()
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)


class DifficultyLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para niveles de dificultad.
    """
    queryset = DifficultyLevel.objects.all()
    serializer_class = DifficultyLevelSerializer


class CourseStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para estados de curso.
    """
    queryset = CourseStatus.objects.all()
    serializer_class = CourseStatusSerializer


class LessonTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para tipos de lección.
    """
    queryset = LessonType.objects.all()
    serializer_class = LessonTypeSerializer


class EnrollmentStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para estados de inscripción.
    """
    queryset = EnrollmentStatus.objects.all()
    serializer_class = EnrollmentStatusSerializer


# ==================== COURSES ====================

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar cursos.
    
    list: Listar todos los cursos
    create: Crear un nuevo curso
    retrieve: Obtener detalles de un curso
    update: Actualizar un curso
    destroy: Eliminar un curso
    """
    queryset = Course.objects.select_related(
        'instructor', 'category', 'difficulty_level', 'status'
    ).prefetch_related('lessons').all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty_level', 'status', 'instructor', 'language']
    search_fields = ['title', 'description', 'requirements', 'learning_objectives']
    ordering_fields = ['created_at', 'price', 'title', 'published_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CourseCreateUpdateSerializer
        return CourseSerializer
    
    @swagger_auto_schema(
        operation_description="Listar solo cursos publicados",
        responses={200: CourseListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def published(self, request):
        """Obtener solo cursos publicados"""
        courses = self.queryset.filter(published_at__isnull=False)
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Obtener las lecciones de un curso",
        responses={200: LessonListSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def lessons(self, request, slug=None):
        """Obtener las lecciones de un curso"""
        course = self.get_object()
        lessons = course.lessons.select_related('lesson_type').all()
        serializer = LessonListSerializer(lessons, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Obtener los comentarios/reseñas de un curso",
        responses={200: CommentListSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def comments(self, request, slug=None):
        """Obtener los comentarios de un curso"""
        course = self.get_object()
        comments = course.comments.select_related('user').all()
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Obtener las inscripciones de un curso",
        responses={200: EnrollmentListSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def enrollments(self, request, slug=None):
        """Obtener las inscripciones de un curso"""
        course = self.get_object()
        enrollments = course.enrollments.select_related('user', 'status').all()
        serializer = EnrollmentListSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Obtener estadísticas del curso",
        responses={200: openapi.Response('Estadísticas del curso')}
    )
    @action(detail=True, methods=['get'])
    def stats(self, request, slug=None):
        """Obtener estadísticas del curso"""
        course = self.get_object()
        
        # Calcular estadísticas
        total_enrollments = course.enrollments.count()
        active_enrollments = course.enrollments.filter(
            status__status_name__iexact='active'
        ).count()
        completed_enrollments = course.enrollments.filter(
            status__status_name__iexact='completed'
        ).count()
        
        reviews = course.comments.filter(is_review=True, rating__isnull=False)
        avg_rating = None
        if reviews.exists():
            avg_rating = round(sum(r.rating for r in reviews) / reviews.count(), 2)
        
        stats = {
            'total_enrollments': total_enrollments,
            'active_enrollments': active_enrollments,
            'completed_enrollments': completed_enrollments,
            'total_lessons': course.lessons.count(),
            'total_reviews': reviews.count(),
            'average_rating': avg_rating,
            'total_duration_hours': course.duration_hours,
        }
        
        return Response(stats)


# ==================== LESSONS ====================

class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar lecciones.
    """
    queryset = Lesson.objects.select_related('course', 'lesson_type').all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson_type', 'is_published', 'is_free']
    search_fields = ['title', 'description', 'content']
    ordering_fields = ['order_index', 'created_at', 'duration_minutes']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return LessonListSerializer
        return LessonSerializer


class LessonProgressViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar el progreso de lecciones.
    """
    queryset = LessonProgress.objects.select_related('enrollment__user', 'lesson').all()
    serializer_class = LessonProgressSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['enrollment', 'lesson', 'is_completed']
    
    @swagger_auto_schema(
        operation_description="Marcar lección como completada",
        responses={200: LessonProgressSerializer()}
    )
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Marcar una lección como completada"""
        progress = self.get_object()
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()
        
        # Actualizar progreso del enrollment
        enrollment = progress.enrollment
        total_lessons = enrollment.course.lessons.count()
        completed_lessons = enrollment.lesson_progress.filter(is_completed=True).count()
        
        if total_lessons > 0:
            enrollment.progress_percentage = (completed_lessons / total_lessons) * 100
            enrollment.save()
        
        serializer = LessonProgressSerializer(progress)
        return Response(serializer.data)


# ==================== ENROLLMENTS ====================

class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar inscripciones.
    """
    queryset = Enrollment.objects.select_related(
        'user', 'course', 'status', 'current_lesson'
    ).all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'course', 'status']
    search_fields = ['user__username', 'course__title']
    ordering_fields = ['enrolled_at', 'progress_percentage', 'last_accessed_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EnrollmentCreateSerializer
        elif self.action == 'list':
            return EnrollmentListSerializer
        return EnrollmentSerializer
    
    def perform_create(self, serializer):
        """Al crear inscripción, crear progreso para cada lección"""
        enrollment = serializer.save()
        
        # Crear registros de progreso para todas las lecciones
        lessons = enrollment.course.lessons.all()
        for lesson in lessons:
            LessonProgress.objects.get_or_create(
                enrollment=enrollment,
                lesson=lesson
            )
    
    @swagger_auto_schema(
        operation_description="Actualizar el progreso de una inscripción",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'progress_percentage': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Porcentaje de progreso (0-100)'
                ),
            }
        ),
        responses={200: EnrollmentSerializer()}
    )
    @action(detail=True, methods=['patch'])
    def update_progress(self, request, pk=None):
        """Actualizar el progreso de una inscripción manualmente"""
        enrollment = self.get_object()
        progress = request.data.get('progress_percentage')
        
        if progress is not None:
            try:
                progress = float(progress)
                if 0 <= progress <= 100:
                    enrollment.progress_percentage = progress
                    
                    # Si llega a 100%, marcar como completado
                    if progress == 100:
                        completed_status = EnrollmentStatus.objects.filter(
                            status_name__iexact='completed'
                        ).first()
                        if completed_status:
                            enrollment.status = completed_status
                        enrollment.completed_at = timezone.now()
                    
                    enrollment.save()
                    serializer = EnrollmentSerializer(enrollment)
                    return Response(serializer.data)
                else:
                    return Response(
                        {'error': 'El progreso debe estar entre 0 y 100'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {'error': 'El progreso debe ser un número'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            {'error': 'Se requiere el campo progress_percentage'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @swagger_auto_schema(
        operation_description="Obtener el progreso detallado de lecciones",
        responses={200: LessonProgressSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def lesson_progress(self, request, pk=None):
        """Obtener el progreso de todas las lecciones de la inscripción"""
        enrollment = self.get_object()
        progress = enrollment.lesson_progress.select_related('lesson').all()
        serializer = LessonProgressSerializer(progress, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Actualizar lección actual",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'lesson_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='ID de la lección'
                ),
            }
        ),
        responses={200: EnrollmentSerializer()}
    )
    @action(detail=True, methods=['patch'])
    def update_current_lesson(self, request, pk=None):
        """Actualizar la lección actual del usuario"""
        enrollment = self.get_object()
        lesson_id = request.data.get('lesson_id')
        
        if lesson_id:
            try:
                lesson = Lesson.objects.get(id=lesson_id, course=enrollment.course)
                enrollment.current_lesson = lesson
                enrollment.save()
                serializer = EnrollmentSerializer(enrollment)
                return Response(serializer.data)
            except Lesson.DoesNotExist:
                return Response(
                    {'error': 'Lección no encontrada o no pertenece al curso'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(
            {'error': 'Se requiere el campo lesson_id'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @swagger_auto_schema(
        operation_description="Cancelar inscripción",
        responses={200: EnrollmentSerializer()}
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancelar una inscripción"""
        enrollment = self.get_object()
        cancelled_status = EnrollmentStatus.objects.filter(
            status_name__iexact='cancelled'
        ).first()
        
        if cancelled_status:
            enrollment.status = cancelled_status
            enrollment.save()
            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Estado de cancelación no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )


# ==================== COMMENTS ====================

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar comentarios y reseñas.
    
    list: Listar todos los comentarios
    create: Crear un nuevo comentario
    retrieve: Obtener detalles de un comentario
    update: Actualizar un comentario
    destroy: Eliminar un comentario
    """
    queryset = Comment.objects.select_related('user', 'course').all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'course', 'rating', 'is_review']
    search_fields = ['content', 'user__username', 'course__title']
    ordering_fields = ['created_at', 'rating']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CommentListSerializer
        return CommentSerializer
    
    @swagger_auto_schema(
        operation_description="Listar solo reseñas con calificación",
        responses={200: CommentListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def reviews(self, request):
        """Obtener solo reseñas (comentarios con rating)"""
        reviews = self.queryset.filter(is_review=True, rating__isnull=False)
        serializer = CommentListSerializer(reviews, many=True)
        return Response(serializer.data)