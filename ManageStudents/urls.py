"""ManageStudents URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.contrib.auth import views as auth_views
from app import views
from ManageStudents import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('register/', views.register_view),
    path('main/', views.main_page_view),
    # url for users
    path('user/list', views.user_list_page),
    path('user/<int:user_id>', views.user_page_view),
    path('user/<int:user_id>/settings', views.user_page_changes_view),

    # task
    path('task/list', views.task_list_view),
    path('task/<int:task_id>', views.task_view),
    # course
    path('course/list', views.course_list_view),
    path('course/<int:course_id>', views.course_view),
    path('course/<int:course_id>/<int:lesson_id>', views.lesson_view),
    path('course/<int:course_id>/<int:lesson_id>/<int:block_id>', views.lesson_block_view),
    path('course/add', views.add_course)

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)