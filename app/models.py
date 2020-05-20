from django.db import models
from django.contrib.auth.models import User, Group


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)


class TaskFiles(models.Model):
    files = models.FileField(upload_to='uploads/')


class Task(models.Model):
    name = models.CharField(max_length=120)
    desc = models.TextField()
    cost = models.IntegerField()
    category = models.CharField(max_length=20)
    files = models.ManyToManyField(TaskFiles)
    char_format_flag = models.NullBooleanField()
    string_format_flag = models.NullBooleanField()
    programmin_format_flag = models.NullBooleanField()
    revizion_format_flag = models.NullBooleanField()


class TaskTrueAnswers(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    true_flags = models.TextField()


class TaskAnswers(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    answer = models.TextField()
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    time = models.DateTimeField()
    score = models.IntegerField()
    accuracy = models.BooleanField(default=0)
    revizion = models.BooleanField(default=0)


class TaskGroup(models.Model):
    name = models.CharField(max_length=100)
    author = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    data_open = models.DateTimeField()
    data_part_close = models.DateTimeField()
    data_close = models.DateTimeField()
    open = models.BooleanField()


class GroupIDTask(models.Model):
    group_id = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)
    task_id = models.ManyToManyField(Task)


class Lesson(models.Model):
    teacher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    data_open = models.DateTimeField()
    open = models.BooleanField(default=0)
    blocks = models.ManyToManyField(TaskGroup)


class Course(models.Model):
    lessons = models.ManyToManyField(Lesson)
    teacher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='media/%Y/%m/%d')



class StudentGroup(models.Model):
    course_id = models.OneToOneField(Course, on_delete=models.CASCADE)
    user_id = models.ManyToManyField(User)
