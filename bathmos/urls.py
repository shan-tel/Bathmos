"""
URL configuration for bathmos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from talmidin import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login_select/', views.login_select, name='Select log in '),
    path( 'teacher_login/', views.teacher_login, name='log in as teacher'),
    path('student_login/', views.student_login, name='log in as student'),
    path('teacher_login_select/', views.teacher_login_select, name='choose as teacher'),
    path('subject_select/', views.subject_select, name='choose as subject'),
    path('score_entry/', views.score_entry, name='score entry'),
    path('save_scores/', views.save_scores, name='save scores'),
    path('student_scoresheet/', views.student_scoresheet, name='student scoresheet'),
    path('student_scoresheet_pdf/', views.student_scoresheet_pdf, name='pdf'),
   # path('setup-admin/', views.setup_admin, name='setup admin'),
    path('logout/', views.logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)