from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.authentication.models import User, UserRole
from apps.courses.models import Assignment, Course, CourseEnrollment, LectureMaterial
from apps.friendships.models import FriendRequest, FriendRequestStatus, Friendship
from apps.messaging.models import Message
from apps.messaging.services import get_or_create_conversation
from apps.notifications.models import Notification
from apps.posts.models import Comment, Post, PostLike


class Command(BaseCommand):
    help = 'Seed sample data for local development.'

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(email='admin@dsauce.app', defaults={'username': 'admin', 'role': UserRole.ADMIN, 'is_verified': True, 'is_staff': True})
        admin.set_password('AdminPass123!')
        admin.save()

        merchant, _ = User.objects.get_or_create(
            email='merchant@dsauce.app',
            defaults={'username': 'merchant1', 'role': UserRole.MERCHANT, 'is_verified': True},
        )
        merchant.set_password('MerchantPass123!')
        merchant.save()

        customer, _ = User.objects.get_or_create(
            email='customer@dsauce.app',
            defaults={'username': 'customer1', 'role': UserRole.CUSTOMER, 'is_verified': True},
        )
        customer.set_password('CustomerPass123!')
        customer.save()

        FriendRequest.objects.get_or_create(
            sender=customer,
            receiver=merchant,
            defaults={'status': FriendRequestStatus.ACCEPTED, 'responded_at': timezone.now()},
        )
        first_id, second_id = Friendship.canonical_pair(customer.id, merchant.id)
        Friendship.objects.get_or_create(requester_id=first_id, receiver_id=second_id)

        post, _ = Post.objects.get_or_create(user=customer, content='Welcome to dsauce backend!')
        PostLike.objects.get_or_create(post=post, user=merchant)
        Comment.objects.get_or_create(post=post, user=merchant, content='Looks great!')

        course, _ = Course.objects.get_or_create(
            code='DSC-101',
            defaults={'lecturer': merchant, 'title': 'Backend Fundamentals', 'description': 'Intro to backend architecture'},
        )
        CourseEnrollment.objects.get_or_create(course=course, student=customer)
        assignment, _ = Assignment.objects.get_or_create(
            course=course,
            title='API Basics',
            defaults={
                'created_by': merchant,
                'description': 'Build CRUD APIs',
                'due_date': timezone.now() + timedelta(days=7),
            },
        )

        conversation, _ = get_or_create_conversation(customer, [merchant.id])
        Message.objects.get_or_create(conversation=conversation, sender=customer, content='Hello from seed data!')

        Notification.objects.get_or_create(
            recipient=merchant,
            actor=customer,
            notification_type='friend_request',
            title='Welcome notification',
            message='Sample notification from seed command.',
        )

        self.stdout.write(self.style.SUCCESS('Sample data seeded successfully.'))
