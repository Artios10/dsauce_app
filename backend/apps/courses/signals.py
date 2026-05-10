from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.courses.models import Assignment, Course, LectureMaterial
from apps.notifications.services import create_notification


def _notify_course_students(course, actor, notification_type, title, message, metadata=None):
    for enrollment in course.enrollments.select_related('student'):
        if enrollment.student_id == actor.id:
            continue
        create_notification(
            recipient=enrollment.student,
            actor=actor,
            notification_type=notification_type,
            title=title,
            message=message,
            metadata=metadata or {},
        )


@receiver(post_save, sender=LectureMaterial)
def notify_new_material(sender, instance, created, **kwargs):
    if created:
        _notify_course_students(
            instance.course,
            instance.uploaded_by,
            'course_update',
            'New lecture material',
            f'New material added in {instance.course.title}: {instance.title}',
            {'course_id': instance.course_id, 'material_id': instance.id},
        )


@receiver(post_save, sender=Assignment)
def notify_new_assignment(sender, instance, created, **kwargs):
    if created:
        _notify_course_students(
            instance.course,
            instance.created_by,
            'course_update',
            'New assignment',
            f'New assignment in {instance.course.title}: {instance.title}',
            {'course_id': instance.course_id, 'assignment_id': instance.id},
        )
