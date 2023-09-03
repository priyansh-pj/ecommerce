from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as Login, logout as Logout
from django.contrib.auth.decorators import login_required
from .models import Profile


def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin_dashboard")
        return redirect("home")

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = Profile.objects.get(email=email)
        except:
            messages.warning(request, "Username Doesn't exist")
            return redirect("login")

        profile = authenticate(request, username=email, password=password)

        if profile is not None:
            Login(request, profile)
            if profile.is_superuser:
                return redirect("admin_dashboard")
            return redirect("home")
    return render(request, "authentication/login.html")


def register(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin_dashboard")
        return redirect("home")

    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        contact_number = request.POST["contact_number"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            try:
                profile = Profile.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    contact_number=contact_number,
                    password=password,
                )
                login(request, profile)
                return redirect("login")
            except Exception as e:
                messages.warning(request, "Unable to create account")
        else:
            messages.warning(request, "Passwords do not match")

        return render(request, "authentication/register.html")


@login_required(login_url="login")
def logout(request):
    Logout(request)
    return redirect("login")
