import os
import tarfile

from celery import shared_task
import docker
from docker.errors import BuildError, APIError, ImageNotFound

from apps.cts.models import Submission

docker_client = docker.from_env()


@shared_task()
def check_submission(submission_id):
    submission = retrieve_submission_from_db(submission_id)

    # определить, решением чего является: тестового задания или внутреннего упражнения
    if (submission.assignment_environment is None) and (submission.assignment_environment is None):
        return 'Error: submission is not bound to any assignment or exercise'
    elif (submission.assignment_environment is not None) and (submission.assignment_environment is not None):
        return 'Error: submission can not be bound both to assignment and exercise'
    elif submission.assignment_environment is not None:
        environment = submission.assignment_environment.environment
        assess_rules = submission.assignment_environment.assessrule_set.all()
    elif submission.assignment_environment is not None:
        environment = submission.exercise.environment
        assess_rules = submission.exercise.assessrule_set.all()

    try:
        create_image_if_not_exists(environment)
    except (TypeError, BuildError, APIError, ImageNotFound) as err:
        return 'During the environment build process an error has occurred : %s' % str(err)

    container = docker_client.containers.create(environment.repository_name + ":" + environment.tag)

    populate_container(container, submission, assess_rules)

    # создать временный образ, содержащий всё необходимое для тестирования
    container.commit(environment.repository_name, 'submission' + str(submission_id))

    container.remove()

    # run it with task_soft_time_limit
    out = docker_client.containers.run(environment.repository_name + ":" + "submission" + str(submission_id),
                                       auto_remove=True)
    # [wait separate task] кстаааа тут фича походу в том, что я раню контейнер асинхронно и дальше иду, отсюда и пустой вывод, и образ удалить не могу
    # docker_client.images.remove(environment.repository_name + ":" + "submission" + str(submission_id))

    return out.decode('utf-8')


def retrieve_submission_from_db(submission_id):
    submission = Submission.objects.filter(id=submission_id).first()
    # ждём сохранения нового решения в БД
    while submission is None:
        submission = Submission.objects.filter(id=submission_id).first()
    return submission


def create_image_if_not_exists(environment):
    if environment.status == 'TO_CREATE':
        dockerfile = open('dockerfiles/environment_' + str(environment.id) + '.Dockerfile', 'wt')
        dockerfile.write(environment.dockerfile)
        dockerfile.close()

        docker_client.images.build(path=os.getcwd() + '/dockerfiles',
                                              dockerfile=os.getcwd() + '/dockerfiles/environment_'
                                                         + str(environment.id) + '.Dockerfile',
                                              tag=environment.repository_name + ':' + environment.tag,
                                              forcerm=True)

        os.remove(os.getcwd() + '/dockerfiles/environment_' + str(environment.id) + '.Dockerfile')
        environment.status = 'CREATED'
        environment.save()

    docker_client.images.get(environment.repository_name + ":" + environment.tag)


def populate_container(container, submission, assess_rules):
    testing_codes = []

    # генерация файлов с исходным кодом, получаемым из БД
    for rule in assess_rules:
        testing_code = rule.testing_code
        if testing_code:
            testing_codes.append(testing_code)
            test_file = open("dockerfiles/tests/" + testing_code.file_name, "wt")
            test_file.write(testing_code.source_code)
            test_file.close()

    submission_file = open("dockerfiles/submissions/solution.py", "wt")
    submission_file.write(submission.source_code)
    submission_file.close()

    # перемещение сгенерированных файлов в контейнер для последующего создания временного образа
    copy_file_to_container(container, os.getcwd() + '/dockerfiles/submissions/solution.py', '/app/solution.py')
    os.remove(os.getcwd() + '/dockerfiles/submissions/solution.py')

    for rule in assess_rules:
        testing_code = rule.testing_code
        if testing_code:
            copy_file_to_container(container, os.getcwd() + '/dockerfiles/tests/' + testing_code.file_name,
                                    "/app/" + testing_code.file_name)
            os.remove(os.getcwd() + '/dockerfiles/tests/' + testing_code.file_name)


def copy_file_to_container(container, src, dst):
    old_wd = os.getcwd()
    os.chdir(os.path.dirname(src))
    file_name = os.path.basename(src)
    tar = tarfile.open(src + '.tar', mode='w')
    try:
        tar.add(file_name)
    finally:
        tar.close()

    data = open(src + '.tar', 'rb').read()
    container.put_archive(os.path.dirname(dst), data)

    os.remove(src + '.tar')
    os.chdir(old_wd)
