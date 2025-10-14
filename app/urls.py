from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProfileViewSet,
    CourseCategoryViewSet, DifficultyLevelViewSet, CourseStatusViewSet,
    LessonTypeViewSet, EnrollmentStatusViewSet,
    CourseViewSet, LessonViewSet, LessonProgressViewSet,
    EnrollmentViewSet, CommentViewSet
)

# Crear el router y registrar los ViewSets
router = DefaultRouter()

# Users & Profiles
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', ProfileViewSet, basename='profile')

# Lookups (Catálogos)
router.register(r'categories', CourseCategoryViewSet, basename='category')
router.register(r'difficulty-levels', DifficultyLevelViewSet, basename='difficulty-level')
router.register(r'course-statuses', CourseStatusViewSet, basename='course-status')
router.register(r'lesson-types', LessonTypeViewSet, basename='lesson-type')
router.register(r'enrollment-statuses', EnrollmentStatusViewSet, basename='enrollment-status')

# Courses & Lessons
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'lesson-progress', LessonProgressViewSet, basename='lesson-progress')

# Enrollments & Comments
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]