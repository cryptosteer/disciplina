from .models import *
from rest_framework import serializers


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'done', 'name', 'description', 'creation')


class HabitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Habit
        fields = ('id', 'working', 'name', 'description', 'creation')

class TodayItemsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_today = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False, allow_blank=True,
                                 max_length=100)
    done = serializers.BooleanField(required=False)
    item_type = serializers.CharField(required=True)
