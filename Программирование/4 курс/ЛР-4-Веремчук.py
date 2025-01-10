#1. Создадим формы для создания опросов и регистрации пользователей:

# polls/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question

class QuestionForm(forms.Form):
    question_text = forms.CharField(
        label='Вопрос',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    choices = forms.CharField(
        label='Варианты ответов (каждый с новой строки)',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

#2. Обновим views.py

# polls/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, UserRegistrationForm
from .models import Question, Choice

@login_required
def create_poll(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Создаем новый вопрос
            question = Question.objects.create(
                question_text=form.cleaned_data['question_text'],
                author=request.user
            )
            # Создаем варианты ответов
            choices = form.cleaned_data['choices'].split('\n')
            for choice_text in choices:
                if choice_text.strip():
                    Choice.objects.create(
                        question=question,
                        choice_text=choice_text.strip()
                    )
            return redirect('polls:detail', pk=question.id)
    else:
        form = QuestionForm()
    return render(request, 'polls/create_poll.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'polls/register.html', {'form': form})


#3. Создадим необходимые шаблоны:

<!-- polls/templates/polls/create_poll.html -->
{% extends 'polls/base.html' %}

{% block content %}
<h2>Создать новый опрос</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Создать</button>
</form>
{% endblock %}

<!-- polls/templates/polls/register.html -->
{% extends 'polls/base.html' %}

{% block content %}
<h2>Регистрация</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Зарегистрироваться</button>
</form>
{% endblock %}

<!-- polls/templates/registration/login.html -->
{% extends 'polls/base.html' %}

{% block content %}
<h2>Вход</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Войти</button>
</form>
<p>Нет аккаунта? <a href="{% url 'polls:register' %}">Зарегистрируйтесь</a></p>
{% endblock %}


#4. Обновим urls.py:

# polls/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.create_poll, name='create_poll'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='polls:index'), name='logout'),
    # ... остальные URL-паттерны
]


#5. Обновим модель Question, добавив поле автора:

# polls/models.py
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # ... остальные поля и методы


#6. Обновим базовый шаблон:

<!-- polls/templates/polls/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Polls App</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="{% url 'polls:index' %}">Polls</a>
            <div class="navbar-nav">
                {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'polls:create_poll' %}">Создать опрос</a>
                    <a class="nav-link" href="{% url 'polls:logout' %}">Выйти</a>
                {% else %}
                    <a class="nav-link" href="{% url 'polls:login' %}">Войти</a>
                    <a class="nav-link" href="{% url 'polls:register' %}">Регистрация</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>

#7. Добавим настройки аутентификации в settings.py:

LOGIN_REDIRECT_URL = 'polls:index'
LOGIN_URL = 'polls:login'
