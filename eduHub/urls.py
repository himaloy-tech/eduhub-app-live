from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("contact", views.contact, name="contact"),
    path("search", views.search, name="search"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("enroll/<int:id>", views.enroll, name="enroll"),
    path("viewMaterial/<int:id>", views.viewMaterial, name="viewMaterial"),
    path("ViewChapter/<int:courseId>/<int:postId>", views.ViewChapter, name="ViewChapter"),
    path("PostComment", views.PostComment, name="comment"),
    path("GivemeComment/<int:postId>", views.comment, name="comment")
]