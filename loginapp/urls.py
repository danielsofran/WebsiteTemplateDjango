from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
    path("admin", views.admin_, name="admin"),
    path('admin/test', views.test, name="test"),
    path('admin/reset', views.reset, name="reset"),
    path('admin/modify', views.modify, name="modify"),
    # path('register_user', views.register_user, name='register_user'),
]
