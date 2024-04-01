from django.urls import path
from django.conf import settings
from .views import UserRegisterationView, UserLoginView,UserPersonalInfoView, UserEducationView, UserExperienceView, UserSkillsView, UserProfileView,TokenRefreshView

from django.conf.urls.static import static

urlpatterns = [
    path('register/', UserRegisterationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('personalinfo/', UserPersonalInfoView.as_view(), name='personalinfo'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('personalinfo/<int:id>',UserPersonalInfoView.as_view(), name='personalinfo'),
    path('education/', UserEducationView.as_view(), name='education'),
    path('education/<int:id>',UserEducationView.as_view(), name='education'),
    path('experience/', UserExperienceView.as_view(), name='experience'),
    path('experience/<int:id>',UserExperienceView.as_view(), name='experience'),
    path('skills/', UserSkillsView.as_view(), name='skills'),
    path('skills/<int:id>',UserSkillsView.as_view(), name='skills'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)