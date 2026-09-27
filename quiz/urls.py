"""URL-маршруты приложения quiz."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChoiceViewSet, QuestionViewSet, UserAnswerViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'choices', ChoiceViewSet, basename='choice')
router.register(r'my-answers', UserAnswerViewSet, basename='my-answer')

urlpatterns = [
    path('', include(router.urls)),
]
