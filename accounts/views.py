from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "successfully login")
            return redirect("home")
        else:
            messages.error(request, "Invalid email address or password.")

    return render(request, "accounts/login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not email or not password or not confirm_password:
            messages.error(request, "Please fill in all fields.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
        elif User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
            )
            login(request, user)
            messages.success(request, "successfully created an account")
            return redirect("home")

    return render(request, "accounts/register.html")


@login_required
def home_view(request):
    return render(request, "accounts/home.html")


def logout_view(request):
    logout(request)
    return redirect("login")