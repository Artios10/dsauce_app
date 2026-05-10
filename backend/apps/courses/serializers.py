from rest_framework import serializers

from apps.courses.models import Assignment, AssignmentSubmission, Course, CourseEnrollment, LectureMaterial


class CourseSerializer(serializers.ModelSerializer):
    lecturer_username = serializers.CharField(source='lecturer.username', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'lecturer', 'lecturer_username', 'title', 'description', 'code', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'lecturer', 'created_at', 'updated_at']


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)

    class Meta:
        model = CourseEnrollment
        fields = ['id', 'course', 'student', 'student_username', 'created_at']
        read_only_fields = ['id', 'student', 'created_at']


class LectureMaterialSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)

    class Meta:
        model = LectureMaterial
        fields = ['id', 'course', 'uploaded_by', 'uploaded_by_username', 'title', 'file', 'created_at']
        read_only_fields = ['id', 'uploaded_by', 'created_at']


class AssignmentSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'course', 'created_by', 'created_by_username', 'title', 'description', 'due_date', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.username', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'student', 'student_username', 'file', 'comment', 'submitted_at']
        read_only_fields = ['id', 'student', 'submitted_at']
