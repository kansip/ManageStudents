from app.models import Task, TaskTrueAnswers, TaskAnswers, User
from django.utils import timezone


def record_answer(task_id, user_id, score, answer):
    ans = TaskAnswers()
    # ans.task_id = Task.objects.get(id=task_id)
    ans.answer = answer
    ans.score = score
    ans.user = User.objects.get(id=user_id)
    ans.time = timezone.now()
    ans.save()
    task = Task.objects.get(id=task_id)
    task.answers.add(ans)


def score(task_id, user_id):
    pass
    # return TaskAnswers.objects.filter(task_id=task_id).filter(user_id=user_id)[len]


def string_cheker(user_id, task_id, answer):
    task = Task.objects.get(id=task_id)
    true_answers = TaskTrueAnswers.objects.filter(task_id=task_id)
    res = 0
    if task.accuracy == 0:
        answer = answer.lower()
        for true_answer in true_answers:
            if answer == true_answer.true_flags.lower():
                res = task.cost
                break
        record_answer(task_id, user_id, res, answer)
    else:
        for true_answer in true_answers:
            if answer == true_answer.true_flags:
                res = task.cost
                break
        record_answer(task_id, user_id, res, answer)
    return res


def allocation(task_id, user_id, answer):
    if Task.objects.get(id=task_id).format_flag == 0 or Task.objects.get(id=task_id).format_flag == 1:
        res = string_cheker(user_id, task_id, answer)
    return res
