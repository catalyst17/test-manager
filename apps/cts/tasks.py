import os
import tarfile

from celery import shared_task
import docker

from apps.cts.models import Submission

docker_client = docker.from_env()


@shared_task()
def check_submission(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
    except Exception as e:
        print(e, flush=True)
        return e            # todo

    assignment = submission.assignment_environment.assignment
    environment = submission.assignment_environment.environment
    assess_rules = submission.assignment_environment.assessrule_set.all()    # ?
    testing_codes = []

    # create files from the source code
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

    container = docker_client.containers.create(environment.repository_name + ":" + environment.tag)

    # copy files to a new environment(image)
    # короче копировать мб придётся, динамически заполняя докерфайл ЛОЛ, if not this:
    # убрать абсолютные пути
    copy_to(container, "/home/arsen/thesis/proj/test-manager/dockerfiles/submissions/solution.py", "/app/solution.py")

    os.remove("/home/arsen/thesis/proj/test-manager/dockerfiles/submissions/solution.py")
    for rule in assess_rules:
        testing_code = rule.testing_code
        copy_to(container, "/home/arsen/thesis/proj/test-manager/dockerfiles/tests/" + testing_code.file_name, "/app/" + testing_code.file_name)
        if testing_code:
            os.remove("/home/arsen/thesis/proj/test-manager/dockerfiles/tests/" + testing_code.file_name)

    # commit to a new image
    container.commit(environment.repository_name, "submission" + str(submission_id))

    container.remove()

    # run it
    out = docker_client.containers.run(environment.repository_name + ":" + "submission" + str(submission_id),
                                       auto_remove=True)
    # кстаааа тут фича походу в том, что я раню контейнер асинхронно и дальше иду, отсюда и пустой вывод, и образ удалить не могу
    # docker_client.images.remove(environment.repository_name + ":" + "submission" + str(submission_id))

    return out.decode('utf-8')


def copy_to(container, src, dst):
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
