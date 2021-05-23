from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from apps.general.models import Company, Skill


class Environment(models.Model):
    repository_name = models.CharField(max_length=100)
    tag = models.CharField(default="latest", max_length=100)
    friendly_name = models.CharField(max_length=30)
    dockerfile = models.TextField()
    status = models.CharField(max_length=30, default='TO_CREATE', blank=True)

    class Meta:
        db_table = "t_environment"

    def __str__(self):
        return '%s environment (%s:%s)' % (self.friendly_name, self.repository_name, self.tag)


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    environments = models.ManyToManyField(Environment, through='AssignmentEnvironment')

    class Meta:
        db_table = "t_assignment"

    def __str__(self):
        return 'Assignment "%s" from company "%s"' % (self.title, self.company.name)


class AssignmentEnvironment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment,  on_delete=models.CASCADE)
    solution_canvas = models.TextField()

    class Meta:
        db_table = "t_assignment_environment"


class Exercise(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    solution_canvas = models.TextField()
    environment = models.ForeignKey(Environment, on_delete=models. CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "t_exercise"

    def __str__(self):
        return 'Exercise "%s" for skill %s' % (self.title, self.skill.name)


class TestingCode(models.Model):
    description = models.CharField(blank=True, max_length=300)
    source_code = models.TextField()
    file_name = models.CharField(max_length=30)
    is_internal = models.BooleanField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = "t_testing_code"

    def __str__(self):
        return 'Testing code of company %s' % self.company.name


class AssessRule(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(blank=True, max_length=300)
    cmd = models.CharField(max_length=300)
    is_crucial = models.BooleanField(default=True)
    execution_order = models.PositiveSmallIntegerField()
    assignment_environment = models.ForeignKey(AssignmentEnvironment, null=True, blank=True, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, null=True, blank=True, on_delete=models.CASCADE)
    testing_code = models.ForeignKey(TestingCode, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "t_assess_rule"

    def __str__(self):
        return 'Asses rule "%s" for some assignment or exercise' % self.title


class Submission(models.Model):
    source_code = models.TextField()
    status = models.CharField(max_length=30)
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    date_time = models.DateTimeField(default=datetime.now, blank=True)
    total_time_spent = models.PositiveSmallIntegerField(null=True, blank=True)
    time_used = models.DecimalField(null=True, blank=True, max_digits=7, decimal_places=2)
    memory_used = models.DecimalField(null=True, blank=True, max_digits=7, decimal_places=2)
    assignment_environment = models.ForeignKey(AssignmentEnvironment, null=True, blank=True, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        db_table = "t_submission"

    def __str__(self):
        return 'Submission of %s' % self.user
