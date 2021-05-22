from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Submission, Environment, Assignment, AssignmentEnvironment
from ..general.models import User
from .tasks import check_submission


@api_view(http_method_names=['POST'])
def submit_solution(request):
    request_data = request.data

    try:
        user = User.objects.get(id=request_data.get("user_id"))
    except User.DoesNotExist:
        response_data = {'error': 'user with specified id does not exist'}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    try:
        environment = Environment.objects.get(repository_name__contains=request_data.get('environment_name'))
    except Environment.DoesNotExist:
        response_data = {'error': 'specified environment does not exist'}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    try:
        assignment = Assignment.objects.get(id=request_data.get('assignment_id'))
    except Environment.DoesNotExist:
        response_data = {'error': 'assignment with specified id does not exist'}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    assignment_environment = AssignmentEnvironment.objects.get(assignment=assignment.id, environment=environment.id)
    solution_code = request_data.get('solution_code')

    submission = Submission.objects.create(source_code=solution_code, status='TO_TEST',
                                           assignment_environment=assignment_environment, user_id=user.id)

    check_submission.delay(submission.id)

    response_data = {'status': 'OK', 'message': 'submission has been queued to the testing system'}

    return Response(response_data, status=status.HTTP_201_CREATED)
