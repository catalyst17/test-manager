# ccts
Testing system for recruiting service (as a module to the web-aplication)

- run rabbitmq locally
docker run -d -p 5672:5672 rabbitmq

- start celery worker
celery -A ccts.celery_app worker --loglevel=INFO

- make calls
from ccts.tasks import check_submission
res = check_submission.delay() # for now rpc is used as a result backend
