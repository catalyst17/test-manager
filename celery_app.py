from celery import Celery

app = Celery('ccts',
             backend='rpc://',
             broker='pyamqp://',
             include=['ccts.tasks'])

if __name__ == '__main__':
    app.start()
