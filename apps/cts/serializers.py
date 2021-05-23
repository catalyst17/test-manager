from rest_framework import serializers
from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('source_code', 'status', 'stdout', 'stderr', 'total_time_spent')
