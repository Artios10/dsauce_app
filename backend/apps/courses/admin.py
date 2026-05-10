from django.contrib import admin

from apps.courses.models import Assignment, AssignmentSubmission, Course, CourseEnrollment, LectureMaterial


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code', 'lecturer', 'is_active', 'created_at')
    search_fields = ('title', 'code', 'lecturer__username')


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'student', 'created_at')


@admin.register(LectureMaterial)
class LectureMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'title', 'uploaded_by', 'created_at')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'title', 'created_by', 'due_date', 'created_at')


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'assignment', 'student', 'submitted_at')
