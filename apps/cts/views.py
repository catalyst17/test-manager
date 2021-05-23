from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Submission, Environment, Assignment, AssignmentEnvironment, Exercise
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

    solution_code = request_data.get('solution_code')

    if request_data.get('task_type') == 'assignment':
        try:
            assignment = Assignment.objects.get(id=request_data.get('assignment_id'))
        except Assignment.DoesNotExist:
            response_data = {'error': 'assignment with specified id does not exist'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        try:
            environment = Environment.objects.get(friendly_name=request_data.get('environment_name'))
        except Environment.DoesNotExist:
            response_data = {'error': 'specified environment does not exist'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        assignment_environment = AssignmentEnvironment.objects.get(assignment=assignment.id, environment=environment.id)

        submission = Submission.objects.create(source_code=solution_code, status='TO_TEST',
                                               assignment_environment=assignment_environment, user_id=user.id)
    elif request_data.get('task_type') == 'exercise':
        try:
            exercise = Exercise.objects.get(id=request_data.get('exercise_id'))
        except Exercise.DoesNotExist:
            response_data = {'error': 'exercise with specified id does not exist'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        submission = Submission.objects.create(source_code=solution_code, status='TO_TEST',
                                               exercise=exercise.id, user_id=user.id)
    else:
        response_data = {'error': 'task_type should be assignment or exercise'}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    check_submission.delay(submission.id)

    response_data = {'status': 'OK', 'message': 'submission has been queued to the testing system'}

    return Response(response_data, status=status.HTTP_201_CREATED)
