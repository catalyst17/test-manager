from celery import shared_task
import docker

docker_client = docker.from_env()


@shared_task()
def check_submission():
    out = docker_client.containers.run("python-ts", auto_remove=True)
    return out.decode('utf-8')
