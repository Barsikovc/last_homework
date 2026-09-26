from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import QuestionViewSet, ChoiceViewSet, UserAnswerViewSet

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'choices', ChoiceViewSet, basename='choice')
router.register(r'my-answers', UserAnswerViewSet, basename='my-answer')

urlpatterns = [
    path('', include(router.urls)),
]