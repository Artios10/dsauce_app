from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.courses.views import AssignmentSubmissionViewSet, AssignmentViewSet, CourseEnrollmentViewSet, CourseViewSet, LectureMaterialViewSet
from apps.friendships.views import FriendRequestViewSet
from apps.messaging.views import ConversationViewSet, MessageViewSet
from apps.notifications.views import NotificationViewSet
from apps.posts.views import CommentViewSet, PostViewSet
from apps.uploads.views import FileUploadViewSet
from apps.users.views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('friendships', FriendRequestViewSet, basename='friendships')
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')
router.register('conversations', ConversationViewSet, basename='conversations')
router.register('messages', MessageViewSet, basename='messages')
router.register('notifications', NotificationViewSet, basename='notifications')
router.register('courses', CourseViewSet, basename='courses')
router.register('materials', LectureMaterialViewSet, basename='materials')
router.register('assignments', AssignmentViewSet, basename='assignments')
router.register('submissions', AssignmentSubmissionViewSet, basename='submissions')
router.register('enrollments', CourseEnrollmentViewSet, basename='enrollments')
router.register('uploads', FileUploadViewSet, basename='uploads')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
