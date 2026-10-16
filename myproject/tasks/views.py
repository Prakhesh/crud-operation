from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Task


def form(request, title, fields, url):
    inputs = ""

    for name in fields:
        input_type = "password" if name == "password" else "text"
        inputs += f'<input type="{input_type}" name="{name}" placeholder="{name}" required><br><br>'

    return HttpResponse(f"""
        <h2>{title}</h2>
        <form method="post" action="{url}">
            <input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">
            {inputs}
            <button type="submit">Submit</button>
        </form>
    """)


# Register
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")

        User.objects.create_user(
            username=username,
            password=password
        )

        return HttpResponse("Registered Successfully")

    return form(request, "Register", ["username", "password"], "/Register/")


# Login
def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            return HttpResponse('Login Success. <a href="/Read/">View Tasks</a>')

        return HttpResponse("Invalid Username or Password")

    return form(request, "Login", ["username", "password"], "/Login/")


# Create
@login_required
def create(request):
    if request.method == 'POST':
        Task.objects.create(
            user=request.user,
            title=request.POST['title']
        )
        return HttpResponse('Task Created. <a href="/Read/">View Tasks</a>')

    return form(request, "Create Task", ["title"], "/Create/")


# Read
@login_required
def read(request):
    tasks = Task.objects.filter(user=request.user)
    result = "<h2>My Tasks</h2>"

    for t in tasks:
        result += f"""
            <p>
                {t.id}: {t.title}
                <a href="/Update/{t.id}/">Update</a>

                <form method="post" action="/Delete/{t.id}/">
                    <input type="hidden" name="csrfmiddlewaretoken"
                           value="{get_token(request)}">
                    <button type="submit">Delete</button>
                </form>
            </p>
            <hr>
        """

    if not tasks.exists():
        result += "No Tasks Found"

    result += f"""
        <p><a href="/Create/">Create Task</a></p>

        <form method="post" action="/Logout/">
            <input type="hidden" name="csrfmiddlewaretoken"
                   value="{get_token(request)}">
            <button type="submit">Logout</button>
        </form>
    """

    return HttpResponse(result)


# Update
@login_required
def update(request, id):
    task = get_object_or_404(
        Task,
        id=id,
        user=request.user
    )

    if request.method == 'POST':
        task.title = request.POST['title']
        task.save()
        return HttpResponse('Task Updated. <a href="/Read/">View Tasks</a>')

    return form(
        request,
        "Update Task",
        ["title"],
        f"/Update/{id}/"
    )


# Delete
@login_required
@require_POST
def delete(request, id):
    task = get_object_or_404(
        Task,
        id=id,
        user=request.user
    )
    task.delete()

    return HttpResponse('Task Deleted. <a href="/Read/">View Tasks</a>')


# Logout
@login_required
@require_POST
def user_logout(request):
    logout(request)
    return HttpResponse("Logout Success")