from django.db import models
from sitetree.models import TreeItemBase


class Settings(models.Model):

    last_generation_date = models.DateTimeField(null=True, blank=True)


class Task(models.Model):

    name = models.CharField(max_length=100)
    order_task = models.IntegerField(null=True, blank=True)
    order_today = models.IntegerField(null=True, blank=True)
    estimated = models.DateTimeField(null=True, blank=True)
    finished = models.DateTimeField(null=True, blank=True)
    done = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    working = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HabitFrecuency(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Habit(models.Model):

    name = models.CharField(max_length=100)
    order_habit = models.IntegerField(null=True, blank=True)
    working = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HabitSchedule(models.Model):

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    frecuency = models.ForeignKey(HabitFrecuency, on_delete=models.CASCADE)
    number_days = models.PositiveIntegerField(null=True, blank=True)
    week_day = models.PositiveIntegerField(null=True, blank=True)
    day = models.PositiveIntegerField(null=True, blank=True)
    month = models.PositiveIntegerField(null=True, blank=True)


class HabitTask(models.Model):

    name = models.CharField(max_length=100)
    habit = models.ForeignKey('Habit', on_delete=models.CASCADE)
    order_today = models.IntegerField(null=True, blank=True)
    archived = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    estimated = models.DateTimeField(null=True, blank=True)
    finished = models.DateTimeField(null=True, blank=True)


class MyTreeItem(TreeItemBase):

    icon = models.CharField('icon', max_length=50, blank=True)


class TodayItem():

    def __str__(self):
        return self.name

    def __init__(self, id, name, done, order_today, item_type):
        self.id = id
        self.name = name
        self.done = done
        self.order_today = order_today
        self.item_type = item_type
