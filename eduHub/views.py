from django.shortcuts import render, HttpResponseRedirect
from .models import Course, Contact, Post, User, Comment
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.

def index(request):
    return render(request, "index.html", {
        "Course":Course.objects.all()
    })

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid Credentials")
            return HttpResponseRedirect(reverse("login"))
    else:
        return render(request, "login.html")

def logout(request):
    auth_logout(request)
    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        auth_login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        message = request.POST.get('message')
        email = request.POST.get('email')
        obj = Contact.objects.create(name=name, message=message, email=email, user=request.user)
        obj.save()
        messages.success(request, "Your Query has been Successfully Submitted")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "contact.html")

def search(request):
    if request.method == "GET":
        query = request.GET.get('query')
        object1 = Course.objects.filter(desc__icontains=query)
        object2 = Course.objects.filter(title__icontains=query)
        object3 = Course.objects.filter(category__icontains=query)
        result = object1.union(object2, object3)
        return render(request, "search.html", {
            "results": result
        })

def profile(request, username):
    if request.user.username == username:
        user = User.objects.get(username=username)
        return render(request, "profile.html", {
            "courses":user.enrolled_courses.all()
        })
@login_required(login_url='/login')
def enroll(request, id):
    course = Course.objects.get(id=id)
    if not request.user in course.enrolled_users.all():
        if not course in request.user.enrolled_courses.all():
            request.user.enrolled_courses.add(course)   
            course.enrolled_users.add(request.user)
            messages.success(request, "Enrolled Successfully")
            return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login')
def viewMaterial(request, id):
    course = Course.objects.get(id=id)
    user = request.user
    if user in course.enrolled_users.all():
        if course in user.enrolled_courses.all():
            return render(request, "CourseIndexPage.html", {
                "Posts" : course.posts.all(),
                "courseId": course.id
            })

@login_required(login_url='/login')
def ViewChapter(request, courseId, postId):
    course = Course.objects.get(id=courseId)
    post = Post.objects.get(id=postId)
    user = request.user
    if user in course.enrolled_users.all():
        if course in user.enrolled_courses.all():
            return render(request, "ViewChapter.html", {
                "Post": post,
                "postId" : postId
            })

def PostComment(request):
    if request.method == "POST":
        response_data = {}
        text = request.POST.get('text')
        id = request.POST.get('postId')
        user = request.POST.get('user')
        response_data['text'] = text
        response_data['postId'] = id
        response_data['username'] = user
        user = User.objects.get(username=user)
        comment = Comment(user=user, post=Post.objects.get(id=id), comment=text)
        comment.save()
        return JsonResponse({
            "message" : "Comment Successfully posted."
        })

def comment(request, postId):
    comments = Comment.objects.filter(post__id=postId).order_by('-time')
    return JsonResponse([comment.serialize() for comment in comments], safe=False)