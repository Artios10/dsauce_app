from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from apps.courses.models import Assignment, AssignmentSubmission, Course, CourseEnrollment, LectureMaterial
from apps.courses.permissions import IsLecturer, IsStudent
from apps.courses.serializers import (
    AssignmentSerializer,
    AssignmentSubmissionSerializer,
    CourseEnrollmentSerializer,
    CourseSerializer,
    LectureMaterialSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('lecturer').all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['lecturer', 'is_active']
    search_fields = ['title', 'description', 'code']
    ordering_fields = ['created_at', 'title']

    def perform_create(self, serializer):
        if self.request.user.role not in ('merchant', 'admin'):
            raise permissions.PermissionDenied('Only merchants can create courses.')
        serializer.save(lecturer=self.request.user)


class CourseEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = CourseEnrollment.objects.select_related('course', 'student').all()
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    filterset_fields = ['course', 'student']

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class LectureMaterialViewSet(viewsets.ModelViewSet):
    queryset = LectureMaterial.objects.select_related('course', 'uploaded_by').all()
    serializer_class = LectureMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['course']

    def perform_create(self, serializer):
        if self.request.user.role not in ('merchant', 'admin'):
            raise permissions.PermissionDenied('Only merchants can upload materials.')
        serializer.save(uploaded_by=self.request.user)


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related('course', 'created_by').all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['course']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        if self.request.user.role not in ('merchant', 'admin'):
            raise permissions.PermissionDenied('Only merchants can create assignments.')
        serializer.save(created_by=self.request.user)


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.select_related('assignment', 'student').all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    filterset_fields = ['assignment', 'student']

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
