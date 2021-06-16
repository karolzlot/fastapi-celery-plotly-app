from celery import Celery

app = Celery('sql_app',
             broker="redis://redis:6379",
             include=['sql_app.celery_tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)




if __name__ == '__main__':
    app.start()