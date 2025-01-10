#1. Создадим структуру проекта

mkdir polls_analytics
cd polls_analytics
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows

pip install django djangorestframework
django-admin startproject polls_analytics .
python manage.py startapp stats
python manage.py startapp filters

#2. Добавим приложения в settings.py:

# polls_analytics/settings.py

INSTALLED_APPS = [
    ...
    'rest_framework',
    'stats',
    'filters',
]

#3. Создадим модели:

# stats/models.py
from django.db import models

class Poll(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.title

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text

#4. Создадим сериализаторы:

# stats/serializers.py
from rest_framework import serializers
from .models import Poll, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes', 'percentage']

    def get_percentage(self, obj):
        total_votes = sum(choice.votes for choice in obj.poll.choice_set.all())
        if total_votes > 0:
            return round((obj.votes / total_votes) * 100, 2)
        return 0

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source='choice_set')
    total_votes = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ['id', 'title', 'pub_date', 'choices', 'total_votes']

    def get_total_votes(self, obj):
        return sum(choice.votes for choice in obj.choice_set.all())

#5. Создадим представления для статистики:

# stats/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Poll
from .serializers import PollSerializer

class StatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    @action(detail=False, methods=['get'])
    def summary(self, request):
        total_polls = Poll.objects.count()
        total_votes = sum(poll.choice_set.aggregate(total=models.Sum('votes'))['total'] or 0 
                         for poll in Poll.objects.all())
        
        return Response({
            'total_polls': total_polls,
            'total_votes': total_votes,
        })

#6. Создадим представления для фильтрации:

# filters/views.py
from rest_framework import viewsets
from rest_framework import filters
from django_filters import rest_framework as django_filters
from stats.models import Poll
from stats.serializers import PollSerializer

class PollFilter(django_filters.FilterSet):
    min_votes = django_filters.NumberFilter(method='filter_min_votes')
    max_votes = django_filters.NumberFilter(method='filter_max_votes')
    
    class Meta:
        model = Poll
        fields = ['pub_date']

    def filter_min_votes(self, queryset, name, value):
        return queryset.annotate(
            total_votes=models.Sum('choice__votes')
        ).filter(total_votes__gte=value)

    def filter_max_votes(self, queryset, name, value):
        return queryset.annotate(
            total_votes=models.Sum('choice__votes')
        ).filter(total_votes__lte=value)

class FilterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PollFilter
    ordering_fields = ['pub_date', 'choice__votes']
 
#7. Настроим URL-маршруты:

# polls_analytics/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stats.views import StatsViewSet
from filters.views import FilterViewSet

router = DefaultRouter()
router.register(r'stats', StatsViewSet)
router.register(r'filters', FilterViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

#8. Добавим необходимые настройки для DRF в settings.py:

# polls_analytics/settings.py

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

