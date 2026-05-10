from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.authentication.models import User, UserRole
from apps.courses.models import Assignment, Course, CourseEnrollment, LectureMaterial
from apps.friendships.models import FriendRequest, FriendRequestStatus, Friendship
from apps.messaging.models import Conversation, ConversationParticipant, Message
from apps.notifications.models import Notification
from apps.posts.models import Comment, Post, PostLike


class Command(BaseCommand):
    help = 'Seed sample data for local development.'

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(email='admin@dsauce.app', defaults={'username': 'admin', 'role': UserRole.ADMIN, 'is_verified': True, 'is_staff': True})
        admin.set_password('AdminPass123!')
        admin.save()

        lecturer, _ = User.objects.get_or_create(email='lecturer@dsauce.app', defaults={'username': 'lecturer1', 'role': UserRole.LECTURER, 'is_verified': True})
        lecturer.set_password('LecturerPass123!')
        lecturer.save()

        student, _ = User.objects.get_or_create(email='student@dsauce.app', defaults={'username': 'student1', 'role': UserRole.STUDENT, 'is_verified': True})
        student.set_password('StudentPass123!')
        student.save()

        normal, _ = User.objects.get_or_create(email='user@dsauce.app', defaults={'username': 'user1', 'role': UserRole.NORMAL_USER, 'is_verified': True})
        normal.set_password('UserPass123!')
        normal.save()

        FriendRequest.objects.get_or_create(sender=normal, receiver=student, defaults={'status': FriendRequestStatus.ACCEPTED, 'responded_at': timezone.now()})
        first_id, second_id = Friendship.canonical_pair(normal.id, student.id)
        Friendship.objects.get_or_create(requester_id=first_id, receiver_id=second_id)

        post, _ = Post.objects.get_or_create(user=normal, content='Welcome to dsauce backend!')
        PostLike.objects.get_or_create(post=post, user=student)
        Comment.objects.get_or_create(post=post, user=student, content='Looks great!')

        course, _ = Course.objects.get_or_create(code='DSC-101', defaults={'lecturer': lecturer, 'title': 'Backend Fundamentals', 'description': 'Intro to backend architecture'})
        CourseEnrollment.objects.get_or_create(course=course, student=student)
        assignment, _ = Assignment.objects.get_or_create(course=course, title='API Basics', defaults={'created_by': lecturer, 'description': 'Build CRUD APIs', 'due_date': timezone.now() + timedelta(days=7)})

        conversation, _ = Conversation.objects.get_or_create()
        ConversationParticipant.objects.get_or_create(conversation=conversation, user=normal)
        ConversationParticipant.objects.get_or_create(conversation=conversation, user=student)
        Message.objects.get_or_create(conversation=conversation, sender=normal, content='Hello from seed data!')

        Notification.objects.get_or_create(
            recipient=student,
            actor=normal,
            notification_type='friend_request',
            title='Welcome notification',
            message='Sample notification from seed command.',
        )

        self.stdout.write(self.style.SUCCESS('Sample data seeded successfully.'))
