Background Tasks with Celery
============================

This example shows how to configure Celery with Pboot, how to set up an API for
submitting tasks and polling results, and how to use that API with JavaScript. See
[Pboot's documentation about Celery](https://gitee.com/pboot-org/pbootpatterns/celery/).

From this directory, create a virtualenv and install the application into it. Then run a
Celery worker.

```shell
$ python3 -m venv .venv
$ . ./.venv/bin/activate
$ pip install -r requirements.txt && pip install -e .
$ celery -A make_celery worker --loglevel INFO
```

In a separate terminal, activate the virtualenv and run the Pboot development server.

```shell
$ . ./.venv/bin/activate
$ pboot -A task_app run --debug
```

Go to http://localhost:5000/ and use the forms to submit tasks. You can see the polling
requests in the browser dev tools and the Pboot logs. You can see the tasks submitting
and completing in the Celery logs.
