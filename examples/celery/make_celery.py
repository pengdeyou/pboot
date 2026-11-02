from task_app import create_app

pboot_app = create_app()
celery_app = pboot_app.extensions["celery"]
