from django.db import models
from django.contrib.auth import get_user_model


class Company(models.Model):
    name = models.CharField()
    description = models.CharField(blank=True)

    def __str__(self):
        return 'Company "%s"' % self.name


class Skill(models.Model):
    name = models.CharField()
    description = models.CharField(blank=True)

    def __str__(self):
        return 'Skill "%s"' % self.name


class Environment(models.Model):
    name = models.CharField()
    tag = models.CharField(default="latest")
    dockerfile = models.TextField()
    status = models.CharField()     # maybe enum?

    class Meta:
        db_table = "environment"

    def __str__(self):
        return 'Environment %s:%s' % (self.name, self.tag)


class Assignment(models.Model):
    title = models.CharField()
    description = models.CharField(blank=True)
    solution_canvas = models.TextField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    environments = models.ManyToManyField(Environment, through='assignment_environment')

    class Meta:
        db_table = "assignment"

    def __str__(self):
        return 'Assignment "%s" from company %s' % (self.title, self.company.name)


class AssignmentEnvironment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment,  on_delete=models.CASCADE)

    class Meta:
        db_table = "assignment_environment"


class Exercise(models.Model):
    title = models.CharField()
    # todo
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        db_table = "exercise"

    def __str__(self):
        return 'Exercise "%s" for skill %s' % (self.title, self.skill.name)


class AssessRule(models.Model):
    title = models.CharField()
    description = models.CharField(blank=True)
    cmd = models.CharField()
    is_crucial = models.BooleanField(default=True)
    execution_order = models.PositiveSmallIntegerField()                                    # do I need it?
    assignment_environment = models.ForeignKey(AssignmentEnvironment, null=True, blank=True, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "assess_rule"

    def __str__(self):
        return 'Asses rule "%s" for some assignment or exercise' % self.title
