from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
UserModel = get_user_model()

class IDAuthBackend(ModelBackend):
    def authenticate(self, request, id=None, password=None, **kwargs):
        if id is None or password is None:
            return
        try:
            user = UserModel.objects.get(id=id)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except UserModel.DoesNotExist:
            logger.warning(f"Login attempt for non-existent user ID: {id}")

    
    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None