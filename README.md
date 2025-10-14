# LMS Project Using Django REST Framework

This project is a Learning Management System (LMS) built using Django and Django REST Framework. It provides a RESTful API for managing users, profiles, courses, lessons, enrollments, and comments.

## Features

- User registration and authentication
- Profile management
- Course and lesson management
- Enrollment in courses
- Commenting on courses and lessons
- Filtering and searching capabilities
- API documentation with Swagger


## DB Diagrams

```mermaid
erDiagram
  
    ROLES {
        int id PK "Primary Key"
        string role_name "Role name (student, instructor, admin)"
        string description "Description of the role"
        text permissions "JSON field with permissions"
    }

    USERS {
        int id PK "Primary Key"
        string username UK "Unique username"
        string email UK "Unique email address"
        string password_hash "Hashed password"
        string first_name "First name"
        string last_name "Last name"
        string full_name "Full name computed"
        string phone_number "Phone number"
        text bio "Short biography"
        date date_of_birth "Date of birth"
        int role_id FK "Foreign Key to ROLES"
        boolean is_active "Is account active"
        string avatar_url "Avatar image URL"
        datetime created_at "Account creation"
        datetime updated_at "Last update"
    }

    CATEGORIES {
        int id PK "Primary Key"
        string name UK "Category name (Programming, Design, Business, etc)"
        string slug UK "URL-friendly name"
        text description "Category description"
        string icon "Icon identifier"
        boolean is_active "Is category active"
    }

    DIFFICULTY_LEVELS {
        int id PK "Primary Key"
        string level_name UK "Beginner, Intermediate, Advanced, Expert"
        int level_order "Numeric order (1-4)"
        string description "Description"
    }

    STATUS_CHOICES {
        int id PK "Primary Key"
        string status_name UK "Draft, Published, Archived, Under Review"
        string description "Status description"
    }

    COURSES {
        int id PK "Primary Key"
        string title "Course title"
        string slug UK "URL-friendly title"
        text description "Course description"
        int instructor_id FK "Foreign Key to USERS"
        int category_id FK "Foreign Key to CATEGORIES"
        int difficulty_level_id FK "Foreign Key to DIFFICULTY_LEVELS"
        int status_id FK "Foreign Key to STATUS_CHOICES"
        string thumbnail_url "Thumbnail image"
        decimal price "Course price (0 for free)"
        int duration_hours "Total duration estimate"
        string language "Course language (en, es, etc)"
        text requirements "Prerequisites"
        text learning_objectives "What students will learn"
        datetime published_at "Publication date"
        datetime created_at "Creation timestamp"
        datetime updated_at "Last update"
    }

    LESSON_TYPES {
        int id PK "Primary Key"
        string type_name UK "video, article, quiz, assignment, live_session"
        string icon "Icon identifier"
        string description "Type description"
    }

    LESSONS {
        int id PK "Primary Key"
        int course_id FK "Foreign Key to COURSES"
        string title "Lesson title"
        text description "Lesson description"
        int lesson_type_id FK "Foreign Key to LESSON_TYPES"
        text content "Lesson content (HTML/Markdown)"
        string video_url "Video URL if applicable"
        int duration_minutes "Duration in minutes"
        int order_index "Order in course (1,2,3...)"
        boolean is_published "Is published"
        boolean is_free "Free preview"
        text attachments "JSON array of file URLs"
        datetime created_at "Creation timestamp"
        datetime updated_at "Last update"
    }

    ENROLLMENT_STATUS {
        int id PK "Primary Key"
        string status_name UK "active, completed, dropped, suspended, expired"
        string description "Status description"
    }

    ENROLLMENTS {
        int id PK "Primary Key"
        int user_id FK "Foreign Key to USERS"
        int course_id FK "Foreign Key to COURSES"
        int status_id FK "Foreign Key to ENROLLMENT_STATUS"
        decimal progress_percentage "0-100 progress"
        datetime enrolled_at "Enrollment date"
        datetime completed_at "Completion date"
        datetime last_accessed_at "Last access"
        text notes "Student notes"
        int current_lesson_id FK "Current lesson ID"
    }

    LESSON_PROGRESS {
        int id PK "Primary Key"
        int enrollment_id FK "Foreign Key to ENROLLMENTS"
        int lesson_id FK "Foreign Key to LESSONS"
        boolean is_completed "Completed flag"
        int time_spent_minutes "Time spent"
        datetime completed_at "Completion date"
        datetime last_accessed_at "Last access"
    }

    COMMENTS {
        int id PK "Primary Key"
        int user_id FK "Foreign Key to USERS"
        int course_id FK "Foreign Key to COURSES"
        text content "Comment content"
        int rating "Rating 1-5 stars (nullable)"
        boolean is_review "Is this a course review"
        datetime created_at "Creation timestamp"
        datetime updated_at "Last update"
    }

    ROLES ||--o{ USERS : "has role"
    USERS ||--o{ COURSES : "creates (instructor)"
    USERS ||--o{ ENROLLMENTS : "enrolls in"
    USERS ||--o{ COMMENTS : "writes"
  
    CATEGORIES ||--o{ COURSES : "categorizes"
    DIFFICULTY_LEVELS ||--o{ COURSES : "defines difficulty"
    STATUS_CHOICES ||--o{ COURSES : "has status"
  
    COURSES ||--o{ LESSONS : "contains"
    COURSES ||--o{ ENROLLMENTS : "has enrollments"
    COURSES ||--o{ COMMENTS : "receives"
  
    LESSON_TYPES ||--o{ LESSONS : "defines type"
    ENROLLMENT_STATUS ||--o{ ENROLLMENTS : "tracks status"
  
    ENROLLMENTS ||--o{ LESSON_PROGRESS : "tracks lessons"
    LESSONS ||--o{ LESSON_PROGRESS : "has progress"
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/chavarc97/lms.git
   cd lms
   ```
2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```
4. Run Docker-Compose && run the server:

   ```bash
   docker-compose up --build
   ```
5. Apply migrations:

   ```bash
   docker exec -it lms-web-1 python manage.py migrate
   ```
6. Create a superuser:

   ```bash
   docker exec -it lms-web-1 python manage.py createsuperuser
   ```
7. (Optional) Populate the database with initial data:

   ```bash
   # Forma básica
   docker-compose exec web python manage.py populate_db

   # Con salida en color
   docker-compose exec web python manage.py populate_db --no-color

   # Ver la salida en tiempo real
   docker-compose exec web python manage.py populate_db --verbosity 2
   ```
8. Access the application:

   - API: `http://localhost:8000/api/`
   - Admin Panel: `http://localhost:8000/admin/`
   - Swagger Documentation: `http://localhost:8000/swagger/`
   - Redoc Documentation: `http://localhost:8000/redoc/`

![alt text](./public/image.png)
