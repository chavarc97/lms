from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import (
    Profile, Course_Category, DifficultyLevel, CourseStatus,
    Course, LessonType, Lesson, EnrollmentStatus, Enrollment,
    LessonProgress, Comment
)
from django.utils import timezone


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creando datos de prueba...\n')
        
        # ==================== CREAR CATÁLOGOS ====================
        
        self.stdout.write(self.style.WARNING('Creando catálogos...'))
        
        # Categorías
        categories_data = [
            {'name': 'Programación', 'description': 'Cursos de programación y desarrollo', 'icon': 'code'},
            {'name': 'Diseño', 'description': 'Cursos de diseño gráfico y UX/UI', 'icon': 'palette'},
            {'name': 'Marketing', 'description': 'Cursos de marketing digital', 'icon': 'bullhorn'},
            {'name': 'Negocios', 'description': 'Cursos de administración y negocios', 'icon': 'briefcase'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = Course_Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon']
                }
            )
            categories[cat_data['name']] = cat
            if created:
                self.stdout.write(f'  ✓ Categoría creada: {cat.name}')
        
        # Niveles de dificultad
        levels_data = [
            {'level_name': 'Principiante', 'level_order': 1, 'description': 'Para personas sin experiencia previa'},
            {'level_name': 'Intermedio', 'level_order': 2, 'description': 'Para personas con conocimientos básicos'},
            {'level_name': 'Avanzado', 'level_order': 3, 'description': 'Para personas con experiencia'},
        ]
        
        levels = {}
        for level_data in levels_data:
            level, created = DifficultyLevel.objects.get_or_create(
                level_name=level_data['level_name'],
                defaults={
                    'level_order': level_data['level_order'],
                    'description': level_data['description']
                }
            )
            levels[level_data['level_name']] = level
            if created:
                self.stdout.write(f'  ✓ Nivel creado: {level.level_name}')
        
        # Estados de curso
        course_statuses_data = [
            {'status_name': 'Borrador', 'description': 'Curso en desarrollo'},
            {'status_name': 'Publicado', 'description': 'Curso disponible públicamente'},
            {'status_name': 'Archivado', 'description': 'Curso no disponible'},
        ]
        
        course_statuses = {}
        for status_data in course_statuses_data:
            status, created = CourseStatus.objects.get_or_create(
                status_name=status_data['status_name'],
                defaults={'description': status_data['description']}
            )
            course_statuses[status_data['status_name']] = status
            if created:
                self.stdout.write(f'  ✓ Estado de curso creado: {status.status_name}')
        
        # Tipos de lección
        lesson_types_data = [
            {'type_name': 'Video', 'icon': 'play-circle', 'description': 'Lección en video'},
            {'type_name': 'Lectura', 'icon': 'book', 'description': 'Contenido textual'},
            {'type_name': 'Quiz', 'icon': 'question-circle', 'description': 'Evaluación'},
            {'type_name': 'Ejercicio', 'icon': 'edit', 'description': 'Práctica guiada'},
        ]
        
        lesson_types = {}
        for lt_data in lesson_types_data:
            lt, created = LessonType.objects.get_or_create(
                type_name=lt_data['type_name'],
                defaults={
                    'icon': lt_data['icon'],
                    'description': lt_data['description']
                }
            )
            lesson_types[lt_data['type_name']] = lt
            if created:
                self.stdout.write(f'  ✓ Tipo de lección creado: {lt.type_name}')
        
        # Estados de inscripción
        enrollment_statuses_data = [
            {'status_name': 'Active', 'description': 'Inscripción activa'},
            {'status_name': 'Completed', 'description': 'Curso completado'},
            {'status_name': 'Cancelled', 'description': 'Inscripción cancelada'},
        ]
        
        enrollment_statuses = {}
        for es_data in enrollment_statuses_data:
            es, created = EnrollmentStatus.objects.get_or_create(
                status_name=es_data['status_name'],
                defaults={'description': es_data['description']}
            )
            enrollment_statuses[es_data['status_name']] = es
            if created:
                self.stdout.write(f'  ✓ Estado de inscripción creado: {es.status_name}')
        
        # ==================== CREAR USUARIOS ====================
        
        self.stdout.write(self.style.WARNING('\nCreando usuarios...'))
        
        users_data = [
            {
                'username': 'instructor1',
                'email': 'instructor1@example.com',
                'password': 'password123',
                'first_name': 'María',
                'last_name': 'García',
                'is_instructor': True,
                'bio': 'Desarrolladora Full Stack con 10 años de experiencia'
            },
            {
                'username': 'instructor2',
                'email': 'instructor2@example.com',
                'password': 'password123',
                'first_name': 'Carlos',
                'last_name': 'Rodríguez',
                'is_instructor': True,
                'bio': 'Experto en marketing digital y estrategia de contenidos'
            },
            {
                'username': 'student1',
                'email': 'student1@example.com',
                'password': 'password123',
                'first_name': 'Ana',
                'last_name': 'Martínez',
                'is_instructor': False,
                'bio': 'Estudiante de programación'
            },
            {
                'username': 'student2',
                'email': 'student2@example.com',
                'password': 'password123',
                'first_name': 'Luis',
                'last_name': 'López',
                'is_instructor': False,
                'bio': 'Profesional en transición de carrera'
            },
        ]
        
        users = {}
        for user_data in users_data:
            # Crear usuario
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'  ✓ Usuario creado: {user.username}')
            
            # Crear o actualizar perfil
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': user_data['bio'],
                    'is_instructor': user_data['is_instructor']
                }
            )
            
            if not created:
                profile.bio = user_data['bio']
                profile.is_instructor = user_data['is_instructor']
                profile.save()
            
            users[user_data['username']] = user
        
        # ==================== CREAR CURSOS ====================
        
        self.stdout.write(self.style.WARNING('\nCreando cursos...'))
        
        courses_data = [
            {
                'title': 'Python para Principiantes',
                'description': 'Aprende Python desde cero hasta nivel intermedio. Curso completo con ejercicios prácticos.',
                'instructor': users['instructor1'],
                'category': categories['Programación'],
                'difficulty_level': levels['Principiante'],
                'status': course_statuses['Publicado'],
                'price': 49.99,
                'duration_hours': 20,
                'language': 'es',
                'requirements': 'Ninguno. Solo ganas de aprender.',
                'learning_objectives': 'Dominar la sintaxis de Python\nCrear programas funcionales\nEntender programación orientada a objetos',
                'published_at': timezone.now(),
                'lessons': [
                    {
                        'title': 'Introducción a Python',
                        'description': 'Conoce qué es Python y por qué aprenderlo',
                        'lesson_type': lesson_types['Video'],
                        'content': 'Python es un lenguaje de programación de alto nivel...',
                        'video_url': 'https://youtube.com/watch?v=example1',
                        'duration_minutes': 45,
                        'order_index': 1,
                        'is_published': True,
                        'is_free': True
                    },
                    {
                        'title': 'Variables y Tipos de Datos',
                        'description': 'Aprende sobre variables, strings, números y booleanos',
                        'lesson_type': lesson_types['Video'],
                        'content': 'Las variables en Python son contenedores para almacenar datos...',
                        'video_url': 'https://youtube.com/watch?v=example2',
                        'duration_minutes': 60,
                        'order_index': 2,
                        'is_published': True,
                        'is_free': False
                    },
                    {
                        'title': 'Control de Flujo',
                        'description': 'If, else, elif y loops en Python',
                        'lesson_type': lesson_types['Video'],
                        'content': 'Las estructuras de control nos permiten tomar decisiones...',
                        'video_url': 'https://youtube.com/watch?v=example3',
                        'duration_minutes': 75,
                        'order_index': 3,
                        'is_published': True,
                        'is_free': False
                    },
                    {
                        'title': 'Ejercicio Práctico 1',
                        'description': 'Pon en práctica lo aprendido',
                        'lesson_type': lesson_types['Ejercicio'],
                        'content': 'Crea un programa que calcule el promedio de calificaciones...',
                        'duration_minutes': 30,
                        'order_index': 4,
                        'is_published': True,
                        'is_free': False
                    },
                ]
            },
            {
                'title': 'Django REST Framework Avanzado',
                'description': 'Construye APIs profesionales con Django y DRF',
                'instructor': users['instructor1'],
                'category': categories['Programación'],
                'difficulty_level': levels['Avanzado'],
                'status': course_statuses['Publicado'],
                'price': 99.99,
                'duration_hours': 40,
                'language': 'es',
                'requirements': 'Conocimientos de Python y Django básico',
                'learning_objectives': 'Crear APIs RESTful profesionales\nImplementar autenticación y permisos\nDocumentar con Swagger',
                'published_at': timezone.now(),
                'lessons': [
                    {
                        'title': 'Configuración del proyecto',
                        'description': 'Setup inicial de DRF',
                        'lesson_type': lesson_types['Video'],
                        'content': 'Comenzaremos configurando nuestro entorno de desarrollo...',
                        'video_url': 'https://youtube.com/watch?v=example4',
                        'duration_minutes': 30,
                        'order_index': 1,
                        'is_published': True,
                        'is_free': True
                    },
                    {
                        'title': 'Serializers avanzados',
                        'description': 'Técnicas avanzadas de serialización',
                        'lesson_type': lesson_types['Video'],
                        'content': 'Los serializers son fundamentales en DRF...',
                        'video_url': 'https://youtube.com/watch?v=example5',
                        'duration_minutes': 90,
                        'order_index': 2,
                        'is_published': True,
                        'is_free': False
                    },
                ]
            },
            {
                'title': 'Marketing Digital para Emprendedores',
                'description': 'Estrategias de marketing digital para hacer crecer tu negocio',
                'instructor': users['instructor2'],
                'category': categories['Marketing'],
                'difficulty_level': levels['Intermedio'],
                'status': course_statuses['Publicado'],
                'price': 69.99,
                'duration_hours': 25,
                'language': 'es',
                'requirements': 'Conocimientos básicos de redes sociales',
                'learning_objectives': 'Crear estrategias de marketing\nGestionar campañas publicitarias\nAnalizar métricas',
                'published_at': timezone.now(),
                'lessons': [
                    {
                        'title': 'Introducción al Marketing Digital',
                        'description': 'Fundamentos del marketing en la era digital',
                        'lesson_type': lesson_types['Video'],
                        'content': 'El marketing digital ha revolucionado la forma de hacer negocios...',
                        'video_url': 'https://youtube.com/watch?v=example6',
                        'duration_minutes': 40,
                        'order_index': 1,
                        'is_published': True,
                        'is_free': True
                    },
                ]
            },
            {
                'title': 'Diseño UX/UI desde Cero',
                'description': 'Aprende a diseñar interfaces de usuario efectivas',
                'instructor': users['instructor2'],
                'category': categories['Diseño'],
                'difficulty_level': levels['Principiante'],
                'status': course_statuses['Borrador'],
                'price': 79.99,
                'duration_hours': 30,
                'language': 'es',
                'requirements': 'Ninguno',
                'learning_objectives': 'Principios de diseño UX\nCrear wireframes y prototipos\nHerramientas como Figma',
                'published_at': None,
                'lessons': []
            },
        ]
        
        courses = []
        for course_data in courses_data:
            # Crear curso
            lessons = course_data.pop('lessons')
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults=course_data
            )
            courses.append(course)
            
            if created:
                self.stdout.write(f'  ✓ Curso creado: {course.title}')
                
                # Crear lecciones
                for lesson_data in lessons:
                    lesson = Lesson.objects.create(
                        course=course,
                        **lesson_data
                    )
                    self.stdout.write(f'    ✓ Lección creada: {lesson.title}')
        
        # ==================== CREAR INSCRIPCIONES ====================
        
        self.stdout.write(self.style.WARNING('\nCreando inscripciones...'))
        
        enrollments_data = [
            {
                'user': users['student1'],
                'course': courses[0],
                'status': enrollment_statuses['Active'],
                'progress_percentage': 60.00
            },
            {
                'user': users['student1'],
                'course': courses[2],
                'status': enrollment_statuses['Completed'],
                'progress_percentage': 100.00,
                'completed_at': timezone.now()
            },
            {
                'user': users['student2'],
                'course': courses[0],
                'status': enrollment_statuses['Active'],
                'progress_percentage': 30.00
            },
            {
                'user': users['student2'],
                'course': courses[1],
                'status': enrollment_statuses['Active'],
                'progress_percentage': 15.00
            },
        ]
        
        for enr_data in enrollments_data:
            # Crear inscripción
            enrollment, created = Enrollment.objects.get_or_create(
                user=enr_data['user'],
                course=enr_data['course'],
                defaults={
                    'status': enr_data['status'],
                    'progress_percentage': enr_data['progress_percentage'],
                    'completed_at': enr_data.get('completed_at')
                }
            )
            
            if created:
                self.stdout.write(f'  ✓ Inscripción creada: {enrollment.user.username} en {enrollment.course.title}')
                
                # Crear progreso de lecciones
                lessons = enrollment.course.lessons.all()
                lessons_completed = int(len(lessons) * (enrollment.progress_percentage / 100))
                
                for i, lesson in enumerate(lessons):
                    is_completed = i < lessons_completed
                    progress = LessonProgress.objects.create(
                        enrollment=enrollment,
                        lesson=lesson,
                        is_completed=is_completed,
                        time_spent_minutes=lesson.duration_minutes if is_completed else 0,
                        completed_at=timezone.now() if is_completed else None
                    )
                    if is_completed:
                        self.stdout.write(f'    ✓ Progreso creado: {progress.lesson.title} (Completado)')
        
        # ==================== CREAR COMENTARIOS ====================
        
        self.stdout.write(self.style.WARNING('\nCreando comentarios...'))
        
        comments_data = [
            {
                'user': users['student1'],
                'course': courses[0],
                'content': 'Excelente curso para principiantes. Las explicaciones son muy claras y los ejercicios ayudan mucho a reforzar los conceptos.',
                'rating': 5,
                'is_review': True
            },
            {
                'user': users['student1'],
                'course': courses[2],
                'content': 'Muy buen contenido sobre marketing digital. Me ayudó a estructurar mejor mi estrategia de contenidos.',
                'rating': 4,
                'is_review': True
            },
            {
                'user': users['student2'],
                'course': courses[0],
                'content': 'Voy a la mitad del curso y estoy aprendiendo mucho. El instructor explica muy bien y los ejemplos son prácticos.',
                'rating': 5,
                'is_review': True
            },
            {
                'user': users['student2'],
                'course': courses[1],
                'content': 'Contenido avanzado pero bien estructurado. Requiere conocimientos previos sólidos de Django.',
                'rating': 4,
                'is_review': True
            },
            {
                'user': users['student1'],
                'course': courses[0],
                'content': 'Tengo una duda sobre la lección de control de flujo. ¿Alguien puede ayudarme?',
                'rating': None,
                'is_review': False
            },
        ]
        
        for comment_data in comments_data:
            comment, created = Comment.objects.get_or_create(
                user=comment_data['user'],
                course=comment_data['course'],
                content=comment_data['content'],
                defaults={
                    'rating': comment_data['rating'],
                    'is_review': comment_data['is_review']
                }
            )
            if created:
                self.stdout.write(f'  ✓ Comentario creado: {comment.user.username} en {comment.course.title}')
        
        # ==================== RESUMEN FINAL ====================
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('¡Datos de prueba creados exitosamente!'))
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS(f'📊 Usuarios: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'👤 Perfiles: {Profile.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'📚 Categorías: {Course_Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'📈 Niveles de dificultad: {DifficultyLevel.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'🎓 Cursos: {Course.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'📝 Lecciones: {Lesson.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'✍️  Inscripciones: {Enrollment.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'📊 Progreso de lecciones: {LessonProgress.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'💬 Comentarios: {Comment.objects.count()}'))
        self.stdout.write('='*60)
        self.stdout.write('\n📌 Credenciales de prueba:')
        self.stdout.write('   Instructores: instructor1/instructor2 - password: password123')
        self.stdout.write('   Estudiantes: student1/student2 - password: password123')
        self.stdout.write('\n🌐 Accede a:')
        self.stdout.write('   Admin: http://localhost:8000/admin/')
        self.stdout.write('   Swagger: http://localhost:8000/swagger/')
        self.stdout.write('   ReDoc: http://localhost:8000/redoc/')
        self.stdout.write('='*60 + '\n')