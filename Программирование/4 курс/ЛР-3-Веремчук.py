# ЧАСТЬ 1: Requests and responses

# Создаем проект:

django-admin startproject mysite
cd mysite

# Создаем приложение polls:

python manage.py startapp polls

# В polls/views.py:

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# В polls/urls.py (создать файл):

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

# В mysite/urls.py:

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]

# ЧАСТЬ 2: Models and admin site

# В polls/models.py:

from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text

# В settings.py добавляем 'polls' в INSTALLED_APPS
# Выполняем миграции:

python manage.py makemigrations polls
python manage.py migrate

# В polls/admin.py:

from django.contrib import admin
from .models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)

# ЧАСТЬ 3: Views and templates
# В polls/views.py добавляем:

from django.shortcuts import render, get_object_or_404
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

# Создаем templates/polls/index.html:

{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}

# Создаем templates/polls/detail.html:

<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>

# ЧАСТЬ 4: Forms and generic views
# Обновляем polls/views.py:

from django.views import generic

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# Обновляем polls/urls.py:

from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

# ЧАСТЬ 5: Testing
# В polls/tests.py:

import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

# ЧАСТЬ 6: Static files
# Создаем polls/static/polls/style.css:

li a {
    color: green;
}

body {
    background: white url("images/background.png") no-repeat;
}

# Обновляем templates для использования статических файлов:

{% load static %}
<link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}">

# ЧАСТЬ 7: Customizing admin site
# В polls/admin.py:

from django.contrib import admin
from .models import Choice, Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)

