import logging
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import timedelta
from django.apps import apps

logger = logging.getLogger('password_reset')

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
    
    def create_password_reset_token(self, user):
        PasswordReset = apps.get_model('users', 'PasswordReset')
        token = get_random_string(length=32)
        expiration_time = timezone.now() + timedelta(minutes=30)
        PasswordReset.objects.create(user=user, token=token, expiration=expiration_time)
        user.save()
        logger.info("Password reset token generated for user %s", user.email)
        return token
    
    def reset_password(self, user, token, new_password):
        """
        Reset the user's password if the provided token is correct.
        """
        PasswordReset = apps.get_model('users', 'PasswordReset')
        try:
            password_reset = PasswordReset.objects.get(user=user, token=token)
            if password_reset and not password_reset.is_expired():
                user.set_password(new_password)
                user.save()
                password_reset.delete()  # delete the token after it's used
                logger.info("Password reset for user %s", user.email)
                return True
        except ObjectDoesNotExist:
            logger.warning("Password reset failed for user %s", user.email)

        logger.warning("Password reset failed for user %s", user.email)
        return False