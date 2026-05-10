import secrets

from django.conf import settings
from django.core.mail import send_mail

from apps.authentication.models import EmailVerificationToken, PasswordResetToken, User


def generate_email_verification_token(user: User) -> EmailVerificationToken:
    token = secrets.token_urlsafe(32)
    entity = EmailVerificationToken.objects.create(user=user, token=token)
    send_mail(
        subject='Verify your email',
        message=f'Use this token to verify your account: {token}',
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@dsauce.app'),
        recipient_list=[user.email],
        fail_silently=True,
    )
    return entity


def generate_password_reset_token(user: User) -> PasswordResetToken:
    token = secrets.token_urlsafe(32)
    entity = PasswordResetToken.objects.create(user=user, token=token)
    send_mail(
        subject='Password reset',
        message=f'Use this token to reset your password: {token}',
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@dsauce.app'),
        recipient_list=[user.email],
        fail_silently=True,
    )
    return entity
