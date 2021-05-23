from django.contrib import admin
from .models import Environment, Assignment, Exercise, TestingCode, AssessRule, Submission, AssignmentEnvironment

admin.site.register(Exercise)
admin.site.register(Environment)
admin.site.register(Assignment)
admin.site.register(TestingCode)
admin.site.register(AssessRule)
admin.site.register(Submission)
admin.site.register(AssignmentEnvironment)
