FLASK_ENV=development
FLASK_APP=cloudm.app:create_app
SECRET_KEY=changeme
DATABASE_URI=sqlite:////tmp/cloudm.db
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=amqp://guest:guest@localhost/
