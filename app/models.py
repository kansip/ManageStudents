from django.db import models
from django.contrib.auth.models import User, Group


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)


class TaskFiles(models.Model):
    files = models.FileField(upload_to='uploads/')


class TaskAnswers(models.Model):
    answer = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    time = models.DateTimeField()
    score = models.IntegerField()
    revizion = models.BooleanField(default=0)


class Grades(models.Model):
    grade = models.IntegerField()
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    weight = models.IntegerField()


class Task(models.Model):
    name = models.CharField(max_length=120)
    desc = models.TextField()
    cost = models.IntegerField()
    category = models.CharField(max_length=20)
    files = models.ManyToManyField(TaskFiles)
    file = models.NullBooleanField()
    format_flag = models.IntegerField()
    accuracy = models.BooleanField(default=1)
    revizion_format_flag = models.BooleanField(default=0)
    answers = models.ManyToManyField(TaskAnswers)
    correct_answer = models.ManyToManyField(User)


class TaskTrueAnswers(models.Model):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    true_flags = models.TextField()


class TaskGroup(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    local = models.IntegerField()
    data_open = models.DateTimeField()
    data_part_close = models.DateTimeField()
    data_close = models.DateTimeField()
    open = models.BooleanField()
    tasks = models.ManyToManyField(Task)


class Lesson(models.Model):
    teacher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(null=True)
    blocks = models.ManyToManyField(TaskGroup)
    name = models.CharField(max_length=30)
    open = models.BooleanField(default=False)
    grades = models.ManyToManyField(Grades)


class MiniSubject(models.Model):
    name = models.CharField(max_length=30)


class MethodicalInstructionsGlobal(models.Model):
    name = models.CharField(max_length=30)
    mini_subject = models.ManyToManyField(MiniSubject)


class Course(models.Model):
    lessons = models.ManyToManyField(Lesson)
    teacher = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='course/', blank=True)
    description = models.CharField(max_length=100)
    open = models.BooleanField(default=False)
    methodical_instructions = models.ManyToManyField(MethodicalInstructionsGlobal)


class StudentGroup(models.Model):
    course_id = models.OneToOneField(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    user_id = models.ManyToManyField(User)
