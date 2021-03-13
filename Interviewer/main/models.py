from django.db import models


# Create your models here.
class Test(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=200)
    is_active = models.BooleanField()


class Question(models.Model):
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    type = models.CharField(max_length=1000, default='')
    text = models.CharField(max_length=1000)


class Answer(models.Model):
    q_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)


class UserAnswer(models.Model):
    ques=models.ForeignKey(Question, on_delete=models.CASCADE, default=None)
    u_name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
