from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator

class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def __init__(self, max_similarity=0.7):
        super().__init__(max_similarity=max_similarity)

    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except ValidationError:
            raise ValidationError(
                _('Tu contraseña no debe ser similar a tu información personal.'),
                code='password_too_similar',
            )
