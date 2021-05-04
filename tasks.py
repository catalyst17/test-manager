from .celery import app
import docker

docker_client = docker.from_env()

@app.task
def echo_from_buster():
    out = docker_client.containers.run("python:3.8-slim-buster", 'ls -la root', auto_remove=True)
    return out.decode('utf-8')