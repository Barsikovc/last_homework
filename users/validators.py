import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomPasswordValidator:
    """Валидатор пароля.

    Проверяет:
    - минимум 8 символов;
    - хотя бы одна заглавная буква;
    - хотя бы одна цифра.
    """

    def validate(self, password, user=None):
        """Проверяет пароль на соответствие требованиям."""
        if len(password) < 8:
            raise ValidationError(
                _("Пароль должен содержать минимум 8 символов."),
                code='password_too_short',
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну заглавную букву."),
                code='password_no_upper',
            )
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну цифру."),
                code='password_no_number',
            )

    def get_help_text(self):
        """Возвращает текст подсказки для пользователя."""
        return _(
            "Пароль должен содержать минимум 8 символов, "
            "хотя бы одну заглавную букву и хотя бы одну цифру."
        )
