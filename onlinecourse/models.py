from django.db import models
from django.contrib.auth.models import User

# ------------------------
# Existing Models (assumed)
# ------------------------

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    pub_date = models.DateField()

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

# ------------------------
# New Exam Models
# ------------------------

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    grade = models.IntegerField()

    def __str__(self):
        return self.question_text

    # Check if user selected all correct answers
    def is_get_score(self, selected_ids):
        correct_choices = self.choice_set.filter(is_correct=True)
        selected_correct = correct_choices.filter(id__in=selected_ids)

        return correct_choices.count() == selected_correct.count()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)


# One enrollment could have multiple submission
# One submission could have multiple choices
# One choice could belong to multiple submissions
#class Submission(models.Model):
#    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
#    choices = models.ManyToManyField(Choice)
