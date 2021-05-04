from .celery_app import app
import docker

docker_client = docker.from_env()


@app.task
def check_submission():
    out = docker_client.containers.run("python-ts", auto_remove=True)
    return out.decode('utf-8')
