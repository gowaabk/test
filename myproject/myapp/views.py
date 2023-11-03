from django.http import HttpResponse

from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import logging
from myapp.forms import (
    RecipeForm,
    LoginForm,
    UserRegistrationForm,
    CategoryForm,
    CoockingForm,
)
from myapp.models import Recipe, Category, CoockingItem


# def index(request):
#     return HttpResponse("Hello, world!")


# def about(request):
#     return HttpResponse("About us")


# def home(request):
#     return HttpResponse("<h1>Welcome to the Recipes home page</h1>")


# def start(request):
#     context = {"title": "first page"}
#     return render(request, "myapp/start.html", context)


# Create your views here.
logger = logging.getLogger(__name__)


def get_home(request):
    title = "Главная страница"
    num_users = User.objects.all().count()
    num_recipes = Recipe.objects.all().count()
    return render(
        request,
        "home.html",
        {"title": title, "num_users": num_users, "num_recipes": num_recipes},
    )


def get_recipes(request):
    title = "Все рецепты"
    coocking_items = CoockingItem.objects.all().order_by("-recipe_id__create_at")
    return render(
        request,
        "coocking_items.html",
        {"title": title, "coocking_items": coocking_items},
    )
def get_recipes_main(request):
    title = "Случайные рецепты"
    coocking_items = CoockingItem.objects.all().order_by("-recipe_id__create_at")
    return render(
        request,
        "home.html",
        {"title": title, "coocking_items": coocking_items},
    )


def get_user_recipe_by_id(request, item_id: int):
    coocking_item = CoockingItem.objects.get(pk=item_id)
    return render(
        request, "user_detail_coocking_item.html", {"coocking_item": coocking_item}
    )


def get_detail_recipe_by_id(request, item_id: int):
    coocking_item = CoockingItem.objects.get(pk=item_id)
    title = coocking_item.recipe_id.name
    return render(
        request,
        "detail_coocking_items.html",
        {"title": title, "coocking_item": coocking_item},
    )


def edit_recipe_by_id(request, item_id: int):
    coocking_item = CoockingItem.objects.get(pk=item_id)
    title = f"Редактировать рецепт"
    if request.method == "GET":
        recipe_form = RecipeForm(instance=coocking_item.recipe_id)
        return render(request, "form.html", {"form": recipe_form, "title": title})
    elif request.method == "POST":
        recipe_form = RecipeForm(request.POST, instance=coocking_item.recipe_id)
        if recipe_form.is_valid():
            recipe_form.save()
            messages.success(request, "recipe saved")
            return redirect("get_user_recipes")
        else:
            messages.error(request, "Please correct the following errors:")
            return render(request, "form.html", {"form": recipe_form, "title": title})


def edit_category_by_id(request, item_id: int):
    coocking_item = CoockingItem.objects.get(pk=item_id)
    title = f"Редактировать категорию"
    if request.method == "GET":
        category_form = CategoryForm(instance=coocking_item.category_id)
        return render(request, "form.html", {"form": category_form, "title": title})
    elif request.method == "POST":
        category_form = CategoryForm(request.POST, instance=coocking_item.category_id)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, "category saved")
            return redirect("get_user_recipes")
        else:
            messages.error(request, "Please correct the following errors:")
            return render(request, "form.html", {"form": category_form, "title": title})


def delete_coocking_item_by_id(request, item_id: id):
    coocking_item = CoockingItem.objects.get(pk=item_id)
    if coocking_item:
        coocking_item.delete()
        messages.success(request, "Рецепт удален")
    else:
        messages.error(request, "Рецепт не найден")
    return redirect("get_user_recipes")


def get_authors(request):
    title = "Список авторов"
    authors = User.objects.all()
    return render(request, "authors.html", {"title": title, "authors": authors})


def get_user_recipes(request):
    title = "Мои рецепты"
    coocking_items = CoockingItem.objects.filter(user_id=request.user).order_by(
        "-recipe_id__create_at"
    )
    if not coocking_items:
        messages.info(request, f"Вы пока не создали ни одного рецепта")
        return redirect("/")
    return render(
        request,
        "user_coocking_items.html",
        {
            "title": title,
            "coocking_items": coocking_items,
            "username": request.user.username,
        },
    )


def add_recipe(request):
    title = "Добавить рецепт"
    head_title = "Добавить рецепт: "
    coocking_form = CoockingForm(request.POST, request.FILES)
    if request.method == "GET":
        return render(
            request,
            "form.html",
            {"form": coocking_form, "title": title, "head_title": head_title},
        )
    elif request.method == "POST":
        if coocking_form.is_valid():
            name = coocking_form.cleaned_data["name"]
            category = coocking_form.cleaned_data["category"]
            description = coocking_form.cleaned_data["description"]
            steps = coocking_form.cleaned_data["steps"]
            coocking_time = coocking_form.cleaned_data["coocking_time"]
            image = coocking_form.cleaned_data["image"]
            recipe = Recipe(
                name=name,
                description=description,
                steps=steps,
                coocking_time=coocking_time,
                image=image,
            )
            category = Category(name=category)
            recipe.save()
            category.save()
            coocking_item = CoockingItem(
                user_id=request.user, recipe_id=recipe, category_id=category
            )
            coocking_item.save()
            messages.success(request, f"Рецепт сохранен. {request.user}")
            return redirect("get_user_recipes")
    else:
        messages.error(request, f"Не удалось сохранить рецепт. {request.user}")
        return render(
            request,
            "form.html",
            {"form": coocking_form, "title": title, "head_title": head_title},
        )
    return render(
        request,
        "form.html",
        {"form": coocking_form, "title": title, "head_title": head_title},
    )


def sign_in(request):
    title = "Вход"

    if request.method == "GET":
        form = LoginForm()
        return render(
            request, "registration/login.html", {"form": form, "title": title}
        )
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(
                    request, f"Привет, {username.title()}, добро пожаловать!"
                )
                return redirect("home")

    # form is not valid or user is not authenticated
    messages.error(request, f"Некорректное имя пользователя или пароль")
    return render(request, "registration/login.html", {"form": form, "title": title})


def register(request):
    title = "Регистрация"
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            messages.success(request, f"Пользователь сохранен. Можете авторизоваться")
            return redirect("login")
    else:
        user_form = UserRegistrationForm()
    return render(
        request, "registration/register.html", {"user_form": user_form, "title": title}
    )


def sign_out(request):
    title = "Выход"
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, f"Вы вышли из аккаунта")
        return render(request, "registration/logout.html", {"title": title})
    else:
        return redirect("login")


# Create your views here.
# def start(request):
#     context = {"recipes": recipes}
#     return render(request, "myapp/start.html", context)
