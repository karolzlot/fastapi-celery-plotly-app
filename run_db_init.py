from sql_app.celery_tasks import db_init

db_init.delay()


