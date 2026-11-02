<div align="center"><img src="docs/_static/pboot-name.svg" alt="" height="150"></div>

# Pboot

Pboot is a lightweight [WSGI] web application framework. It is designed
to make getting started quick and easy, with the ability to scale up to
complex applications. It began as a simple wrapper around [Werkzeug]
and [Jinja], and has become one of the most popular Python web
application frameworks.

Pboot offers suggestions, but doesn't enforce any dependencies or
project layout. It is up to the developer to choose the tools and
libraries they want to use. There are many extensions provided by the
community that make adding new functionality easy.

[WSGI]: https://wsgi.readthedocs.io/
[Werkzeug]: https://werkzeug.palletsprojects.com/
[Jinja]: https://jinja.palletsprojects.com/

## About This Project

Pboot is a renamed and maintained fork of [Flask]. The public API mirrors
Flask's, with the following renames applied throughout the codebase:

| Flask           | Pboot            |
| --------------- | ---------------- |
| `flask`         | `pboot`          |
| `Flask`         | `Pboot`          |
| `FlaskClient`   | `PbootClient`    |
| `FlaskGroup`    | `PbootGroup`     |
| `FlaskCliRunner`| `PbootCliRunner` |
| `flask` CLI     | `pboot` CLI      |
| `FLASK_APP`     | `PBOOT_APP`      |
| `.flaskenv`     | `.pbootenv`      |

Upstream origin: <https://github.com/pallets/flask> — BSD-3-Clause licensed,
original copyright retained in `LICENSE.txt`.

## A Simple Example

```python
# save this as app.py
from pboot import Pboot

app = Pboot(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
```

```
$ pboot run
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Community

Issues and discussions are tracked at
<https://gitee.com/pboot-org/pboot/issues>.

## Contributing

See the issue tracker for ways to contribute, including reporting issues,
requesting features, asking or answering questions, and making pull requests.
